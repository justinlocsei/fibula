import os.path
import re

from ansible import errors

def trailing_slash_fs(value):
    """Ensure that a value ends with a single filesystem-appropriate slash.

    Args:
        value (str): A filesystem path

    Returns:
        str: The path with a trailing slash
    """
    return _trailing_character(value, os.path.sep)


def trailing_slash_url(value):
    """Ensure that a URL ends with a trailing slash.

    Args:
        value (str): A URL

    Returns:
        str: The URL with a trailing slash
    """
    return _trailing_character(value, '/')


def _trailing_character(value, terminator):
    """Ensure that a string ends with a single terminating character.

    Args:
        value (str): The value to modify
        terminator (str): The terminal character to use

    Returns:
        str: A string that ends with the terminal character
    """
    base_path = re.sub(r'%s+$' % re.escape(terminator), '', value)
    return "%s%s" % (base_path, terminator)


class FilterModule(object):
    """Custom Jinja2 filters for working with paths."""

    def filters(self):
        return {
            'trailing_slash_fs': trailing_slash_fs,
            'trailing_slash_url': trailing_slash_url
        }
