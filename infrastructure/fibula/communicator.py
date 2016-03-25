import click


class Communicator:
    """A utility for displaying messages to the user and receiving input."""

    def __init__(self, label=None):
        """Create a new logger.

        Keyword Args:
            label (str): An optional label for the logger
        """
        self.label = label

    def group(self, name):
        """Create a new communicator with a group label.

        Args:
            name (str): The label for the subgroup

        Returns:
            fibula.communicator.Communicator
        """
        if self.label:
            label = '%s/%s' % (self.label, name)
        else:
            label = name

        return Communicator(label=label)

    def info(self, message):
        """Show an informational message."""
        click.echo(self._format(message, u'\u00b7'))

    def create(self, message):
        """Show a message for an action that created an object."""
        output = self._format(message, '+')
        click.echo(click.style(output, fg='green', bold=True))

    def delete(self, message):
        """Show a message for an action that deleted an object."""
        output = self._format(message, '-')
        click.echo(click.style(output, fg='red', bold=True))

    def update(self, message):
        """Show a message for an action that updated an object."""
        output = self._format(message, '=')
        click.echo(click.style(output, fg='yellow', bold=True))

    def skip(self, message):
        """Show a message indicating a skipped action."""
        output = self._format(message, '#')
        click.echo(click.style(output, fg='yellow'))

    def error(self, message):
        """Show an error message."""
        output = self._format(message, '!')
        click.echo(click.style(output, fg='white', bg='red'))

    def warn(self, message):
        """Show a warning."""
        output = self._format(message, '!')
        click.echo(click.style(output, fg='black', bg='yellow'))

    def confirm(self, prompt, destructive=False):
        """Request confirmation from the user for an action.

        Args:
            prompt (str): The confirmation prompt

        Keyword Args:
            destructive (bool): Whether the action is destructive

        Returns:
            bool: Whether the user accepted
        """
        message = self._format(prompt, '?')
        if destructive:
            message = click.style(message, fg='red', bold=True)

        return click.confirm(message)

    def _format(self, message, icon=' '):
        """Return a message formatted for display.

        Args:
            message (str): The message to show

        Keyword Args:
            icon (str): The icon to use with the message

        Returns:
            str: The formatted message
        """
        if self.label:
            return '%s [%s] %s' % (icon, self.label, message)
        else:
            return '%s %s' % (icon, message)
