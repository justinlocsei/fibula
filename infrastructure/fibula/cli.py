import click

from fibula import actions


@click.group()
def cli():
    pass


@cli.group()
def keys():
    """Manage remote SSH keys."""
    pass


@keys.command('sync')
def keys_sync():
    """Sync remote SSH keys with the key manifest."""
    actions.SSHKeys().sync()


@cli.group()
def servers():
    """Manage remote servers."""
    pass


@servers.command('create')
def servers_create():
    """Create remote servers to match the server manifest."""
    actions.Servers().create()


@servers.command('sync')
def servers_sync():
    """Sync the configuration of existing remote servers with the manifest."""
    actions.Servers().sync()


@servers.command('prune')
def servers_prune():
    """Remove any remote servers that do not appear in the manifest."""
    actions.Servers().prune()


@servers.command('destroy')
@click.argument('name', type=str)
def servers_destroy(name):
    """Destroy a single remote server."""
    actions.Servers().destroy(name)
