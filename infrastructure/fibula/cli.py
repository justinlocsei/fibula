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


@cli.group()
def servers():
    """Modify remote servers."""
    pass


@servers.command()
def create():
    """Create servers to match the local list."""
    servers = actions.Servers()
    servers.create()


@servers.command()
def sync():
    """Sync the remote servers with the local configuration."""
    servers = actions.Servers()
    servers.sync()


@servers.command()
def prune():
    """Remove any remote servers that do not appear locally."""
    servers = actions.Servers()
    servers.prune()
