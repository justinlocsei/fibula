def certbot_webroot_args(domains):
    """Create --webroot args for the certbot-auto command for domains.

    Args:
        domains (list): A list of domain dicts

    Returns:
        str: The request arguments
    """
    return ' '.join(['-w %s -d %s' % (d['webroot'], d['domain]']) for d in domains])


class FilterModule(object):
    """Custom Jinja2 filters for the certbot role."""

    def filters(self):
        return {
            'certbot_webroot_args': certbot_webroot_args
        }
