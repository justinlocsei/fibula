import click

from fibula import actions


@click.group()
def cli():
    pass


@cli.group()
def keys():
    """Manage remote SSH keys."""
    pass


@keys.command('add')
def keys_add():
    """Add missing SSH keys to the remote."""
    actions.SSHKeys().add()


@keys.command('sync')
def keys_sync():
    """Sync the configuration of remote SSH keys with the manifest."""
    actions.SSHKeys().sync()


@keys.command('prune')
def keys_prune():
    """Remove remote SSH keys not present in the manifest."""
    actions.SSHKeys().prune()


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


@cli.group()
def domains():
    """Manage network domains."""
    pass


@domains.command('sync')
def domains_sync():
    """Sync domains with the manifest."""
    actions.Domains().sync()
