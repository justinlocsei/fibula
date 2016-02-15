#!/usr/bin/python

DOCUMENTATION = """
---
module: postgresql_user_setting
short_description: Sets a value for a session setting for a PostgreSQL user.
description:
   - Set a value for a session setting for a PostgreSQL user.
options:
  user:
    description:
      - The user that should receive the updated setting
    required: true
    default: null
  password:
    description:
      - The password for the user who should receive the updated setting
    required: false
    default: null
  setting:
    description:
      - The name of the session setting
    required: true
    default: null
  value:
    description:
      - The value for the session setting
    required: true
    default: null
  admin_user:
    description:
      - The admin user used to authenticate with PostgreSQL
    required: false
    default: postgres
  admin_password:
    description:
      - The password for the admin PostgreSQL admin user
    required: false
    default: null
  login_host:
    description:
      - The host running PostgreSQL
    required: false
    default: localhost
  port:
    description:
      - The database port to connect to
    required: false
    default: 5432
requirements:
  - psycopg2
"""

EXAMPLES = """
# Set the default time zone to UTC for the "test" user
- postgresql_user_setting:
    user: test
    setting: timezone
    value: UTC
"""

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    psycopg2_found = False
else:
    psycopg2_found = True


def setting_matches(cursor, setting, value):
    query = "SELECT current_setting(%(setting)s)"
    cursor.execute(query, {"setting": setting})
    record = cursor.fetchone()
    return record is not None and record[0] == value


def setting_update(admin_cursor, user_cursor, user, setting, value):
    if setting_matches(user_cursor, setting, value):
        return False

    query = ["ALTER ROLE %s" % pg_quote_identifier(user, "role")]
    query.append("SET %s" % setting)
    query.append("TO %(value)s")
    admin_cursor.execute(" ".join(query), {"value": value})
    return True


def extract_params(params, mapping):
    return dict((mapping[k], v) for (k, v) in params.iteritems() if k in mapping and v != "")


def main():
    module = AnsibleModule(
        argument_spec=dict(
            admin_password=dict(default=""),
            admin_user=dict(default="postgres"),
            login_host=dict(default=""),
            password=dict(default=""),
            port=dict(default="5432"),
            setting=dict(required=True),
            user=dict(required=True),
            value=dict(required=True)
        ),
        supports_check_mode=False
    )

    if not psycopg2_found:
        module.fail_json(msg="the python psycopg2 module is required")

    setting = module.params["setting"]
    value = module.params["value"]
    changed = False

    admin_kwargs = extract_params(module.params, {
        "login_host": "host",
        "admin_user": "user",
        "admin_password": "password",
        "port": "port"
    })
    user_kwargs = extract_params(module.params, {
        "login_host": "host",
        "user": "user",
        "password": "password",
        "port": "port"
    })

    try:
        admin_connection = psycopg2.connect(database="postgres", **admin_kwargs)
        admin_cursor = admin_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    except Exception, e:
        module.fail_json(msg="unable to connect to database as %s: %s" % (admin_kwargs["user"], e))

    try:
        user_connection = psycopg2.connect(database="postgres", **user_kwargs)
        user_cursor = user_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    except Exception, e:
        module.fail_json(msg="unable to connect to database as %s: %s" % (user_kwargs["user"], e))

    try:
        changed = setting_update(admin_cursor, user_cursor, user_kwargs["user"], setting, value)
    except Exception, e:
        module.fail_json(msg="database query failed: %s" % e)

    if changed:
        admin_connection.commit()

    module.exit_json(changed=changed)

from ansible.module_utils.basic import *
from ansible.module_utils.database import *

if __name__ == "__main__":
    main()
