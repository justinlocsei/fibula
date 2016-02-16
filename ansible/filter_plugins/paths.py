import os.path
import re

from ansible import errors

def trailing_slash_fs(value):
    """Ensure that the value ends with a single filesystem-appropriate slash."""
    return _trailing_character(value, os.path.sep)


def trailing_slash_url(value):
    """Ensure that the URL ends with a trailing slash."""
    return _trailing_character(value, "/")


def _trailing_character(value, terminator):
    """Ensure that a string ends with a single terminating character."""
    base_path = re.sub(r"%s+$" % re.escape(terminator), "", value)
    return "%s%s" % (base_path, terminator)


class FilterModule(object):
    """Custom Jinja2 filters for Ansible paths"""

    def filters(self):
        return {
            "trailing_slash_fs": trailing_slash_fs,
            "trailing_slash_url": trailing_slash_url
        }
