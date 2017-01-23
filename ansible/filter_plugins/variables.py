from jinja2.runtime import Undefined


def has_value(value):
    """Determine if a variable has a value.

    Args:
        value: Any valid Jinja2 value

    Returns:
        bool: Whether the variable has a value
    """
    if isinstance(value, Undefined):
        return False
    else:
        return value is not None or value


class FilterModule(object):
    """Custom Jinja2 filters for working with variables."""

    def filters(self):
        return {
            'has_value': has_value
        }
