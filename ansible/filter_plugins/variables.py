from ansible import errors
from jinja2.runtime import Undefined


def require_value(value):
    """Require a non-empty value for a variable"""
    if isinstance(value, Undefined):
        raise errors.AnsibleFilterError("Variable must be defined.")
    if value is None:
        raise errors.AnsibleFilterError("Variable must not be null.")
    return value


class FilterModule(object):
    """Custom Jinja2 filters for Ansible variables"""

    def filters(self):
        return {
            "require_value": require_value
        }
