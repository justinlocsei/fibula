from ansible import errors
from itertools import chain
from jinja2.runtime import Undefined


def flatten(value):
    """Flatten a list"""
    return chain.from_iterable(value)


class FilterModule(object):
    """Custom Jinja2 filters for Ansible lists"""

    def filters(self):
        return {
            'flatten': flatten
        }
