import os

import digitalocean


class API:
    """An interface to the Digital Ocean API."""

    def __init__(self):
        self._manager = None
        self._token = None

    def get_droplet_floating_ip(self, droplet):
        """Get the floating IP for a droplet.

        Args:
            droplet (digitalocean.Droplet): A droplet instance

        Returns:
            digitalocean.FloatingIP: The droplet's floating IP
        """
        floating_ips = self.manager.get_all_floating_ips()

        matches = [f for f in floating_ips if f.droplet and f.droplet['id'] == droplet.id]
        if len(matches) > 1:
            self.ui.abort('Multiple floating IPs are bound to the "%s" droplet' % droplet.name)
        elif not len(matches):
            self.ui.abort('No floating IP is bound to the "%s" droplet' % droplet.name)

        return matches[0]

    def get_named_droplet(self, name):
        """Get a single named droplet.

        Args:
            name (str): The name of a droplet

        Returns:
            digitalocean.Droplet: The named droplet
        """
        droplets = self.manager.get_all_droplets()

        matches = [d for d in droplets if d.name == name]
        if len(matches) > 1:
            self.ui.abort('Multiple droplets named "%s" exist' % name)
        elif not len(matches):
            self.ui.abort('No droplet found named "%s"' % name)

        return matches[0]

    @property
    def manager(self):
        """A manager instance for the Digital Ocean API.

        Returns:
            digitalocean.Manager
        """
        if self._manager is None:
            self._manager = digitalocean.Manager(token=self.token)
        return self._manager

    @property
    def token(self):
        """The Digital Ocean API token.

        Returns:
            str

        Raises:
            KeyError: When the token is not specified
        """
        if self._token is None:
            self._token = os.environ['CYB_DO_API_TOKEN']
        return self._token
