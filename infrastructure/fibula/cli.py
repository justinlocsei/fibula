import click

from fibula import actions


@click.group()
def cli():
    pass


@cli.group()
def keys():
    """Manage remote SSH keys."""
    pass


@keys.command()
def sync():
    """Sync remote SSH keys with the key manifest."""
    actions.SSHKeys().sync()


@cli.group()
def servers():
    """Manage remote servers."""
    pass


@servers.command()
def create():
    """Create remote servers to match the server manifest."""
    actions.Servers().create()


@servers.command()
def sync():
    """Sync the configuration of existing remote servers with the manifest."""
    actions.Servers().sync()


@servers.command()
def prune():
    """Remove any remote servers that do not appear in the manifest."""
    actions.Servers().prune()
