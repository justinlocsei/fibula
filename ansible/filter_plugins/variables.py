from ansible import errors
from jinja2.runtime import Undefined


def require_value(value):
    """Require a non-empty value for a variable.

    Args:
        value: Any valid Jinja2 value

    Returns:
        value: The original value

    Raises:
        ansible.errors.AnsibleFilterError: When the variable lacks a value
    """
    if isinstance(value, Undefined):
        raise errors.AnsibleFilterError('Variable must be defined.')
    if value is None:
        raise errors.AnsibleFilterError('Variable must not be null.')
    return value


class FilterModule(object):
    """Custom Jinja2 filters for working with variables."""

    def filters(self):
        return {
            'require_value': require_value
        }
