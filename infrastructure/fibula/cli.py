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
    ssh_keys = actions.SSHKeys()
    ssh_keys.sync()


@cli.group()
def servers():
    """Manage remote servers."""
    pass


@servers.command()
def create():
    """Create remote servers to match the server manifest."""
    servers = actions.Servers()
    servers.create()


@servers.command()
def sync():
    """Sync the configuration of existing remote servers with the manifest."""
    servers = actions.Servers()
    servers.sync()


@servers.command()
def prune():
    """Remove any remote servers that do not appear in the manifest."""
    servers = actions.Servers()
    servers.prune()
