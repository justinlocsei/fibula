def domain(hostname):
    """Extract the domain from a hostname.

    Args:
        hostname (str): A full hostname

    Returns:
        str: The domain component of the hostname
    """
    parts = hostname.split('.')
    return parts[1:-1].join('.')


class FilterModule(object):
    """Custom Jinja2 filters for networking logic."""

    def filters(self):
        return {
            'domain': domain
        }
