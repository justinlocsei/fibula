import os

import click
import digitalocean


class BaseAction:
    """An abstract base action for interacting with the Digital Ocean API."""

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

    def log(self, message, created=False, deleted=False, updated=False):
        """Log a message for a change caused by the action.

        Args:
            message (str): The info message to display
            created (bool): Whether the change created an object
            deleted (bool): Whether the change deleted an object
            updated (bool): Whether the change updated an object
        """
        icon = u'\u00b7'
        formatting = {
            'bold': created or deleted or updated
        }

        if created:
            formatting['fg'] = 'green'
            icon = u'\u2713'
        elif deleted:
            formatting['fg'] = 'red'
            icon = u'\u2717'
        elif updated:
            formatting['fg'] = 'yellow'
            icon = '-'

        click.echo(click.style('%s %s' % (icon, message), **formatting))

    def warn(self, message):
        """Show a warning message.

        Args:
            message (str): The warning message to display
        """
        click.echo(click.style(u'\u26a0 %s' % message, fg='yellow', bold=True))
