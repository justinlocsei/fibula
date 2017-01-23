from itertools import chain


def flatten(value):
    """Flatten a list.

    Args:
        value (list): A potentially nested list

    Retruns:
        list: A flattened list
    """
    return chain.from_iterable(value)


def newline_list(value):
    """Build an array of all newline-separated items in a string.

    Args:
        value (str): A string containing newlines

    Returns:
        list: The newline-separated items in the string
    """
    return value.strip().splitlines()


def str_map(values, formatting):
    """Map each element in a list to a formatted string.

    Args:
        value (list[str]): A list of strings

    Retruns:
        list[str]: The mapped strings
    """
    return [formatting % v for v in values]


class FilterModule(object):
    """Custom Jinja2 filters for working with lists."""

    def filters(self):
        return {
            'flatten': flatten,
            'newline_list': newline_list,
            'str_map': str_map
        }
