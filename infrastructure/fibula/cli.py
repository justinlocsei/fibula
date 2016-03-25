import click

from fibula import actions


@click.group()
def cli():
    pass


@cli.group()
def keys():
    """Modify remote SSH keys."""
    pass


@keys.command()
def sync():
    """Sync remote SSH keys with the local list."""
    ssh_keys = actions.SSHKeys()
    ssh_keys.sync()
