import os

import click
import digitalocean

from fibula.communicator import Communicator


class BaseAction:
    """An abstract base action for interacting with the Digital Ocean API."""

    log_prefix = None

    def __init__(self):
        """Create a new action."""
        self.ui = Communicator(label=self.log_prefix)

    @property
    def do(self):
        """The connection to Digital Ocean.

        Returns:
            digitalocean.Manager
        """
        if not hasattr(self, '_do'):
            self._do = digitalocean.Manager(token=self.token)
        return self._do

    @property
    def token(self):
        """Load the Digital Ocean API token from the environment.

        Returns:
            str: The Digital Ocean API token

        Raises:
            KeyError: When the token is not specified
        """
        if not hasattr(self, '_token'):
            self._token = os.environ['CYB_DO_API_TOKEN']
        return self._token
