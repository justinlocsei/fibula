def domain(host):
    """Extract the domain from a host.

    Args:
        host (str): A full host

    Returns:
        str: The domain component of the host
    """
    parts = host.split('.')
    return '.'.join(parts[1:])


def hostname(host):
    """Extract the hostname from a full host.

    Args:
        host (str): A full host

    Returns:
        str: The host component of the host
    """
    return host.split('.')[0]


class FilterModule(object):
    """Custom Jinja2 filters for networking logic."""

    def filters(self):
        return {
            'domain': domain,
            'hostname': hostname
        }
