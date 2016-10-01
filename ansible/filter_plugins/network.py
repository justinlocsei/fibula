def domain(hostname):
    """Extract the domain from a hostname.

    Args:
        hostname (str): A full hostname

    Returns:
        str: The domain component of the hostname
    """
    parts = hostname.split('.')
    return '.'.join(parts[1:])


def host(hostname):
    """Extract the host from a full hostname.

    Args:
        hostname (str): A full hostname

    Returns:
        str: The host component of the hostname
    """
    return hostname.split('.')[0]


class FilterModule(object):
    """Custom Jinja2 filters for networking logic."""

    def filters(self):
        return {
            'domain': domain,
            'host': host
        }
