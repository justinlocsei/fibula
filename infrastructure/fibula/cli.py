import click

from fibula import actions
from fibula.actions.deploy import ENVIRONMENTS


@click.group()
def cli():
    pass


@cli.command()
@click.pass_context
def build(ctx):
    """Build out all infrastructure components."""
    ctx.forward(keys_add)
    ctx.forward(servers_create)
    ctx.forward(domains_create)
    ctx.forward(dns_add)
    ctx.forward(email_forward)
    ctx.forward(email_whitelabel)
    ctx.forward(backups_configure)


@cli.command()
@click.pass_context
def sync(ctx):
    """Update all infrastructure components."""
    ctx.forward(keys_sync)
    ctx.forward(servers_sync)
    ctx.forward(domains_sync)
    ctx.forward(dns_sync)
    ctx.forward(email_forward)
    ctx.forward(email_whitelabel)
    ctx.forward(backups_configure)


@cli.command()
@click.pass_context
def prune(ctx):
    """Remove all unused infrastructure components."""
    ctx.forward(keys_prune)
    ctx.forward(servers_prune)
    ctx.forward(domains_prune)
    ctx.forward(ips_prune)


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


@cli.group()
def domains():
    """Manage network domains."""
    pass


@domains.command('create')
def domains_create():
    """Add missing remote domains from the manifest."""
    actions.Domains().create()


@domains.command('sync')
def domains_sync():
    """Sync domain configuration with the manifest."""
    actions.Domains().sync()


@domains.command('prune')
def domains_prune():
    """Remove unused remote domains."""
    actions.Domains().prune()


@cli.group()
def dns():
    """Manage DNS records."""
    pass


@dns.command('add')
def dns_add():
    """Add missing DNS records from the manifest."""
    actions.DNS().add()


@dns.command('sync')
def dns_sync():
    """Sync the DNS configuration with the manifest."""
    actions.DNS().sync()


@cli.group()
def ips():
    """Manage IP addresses."""
    pass


@ips.command('prune')
def ips_prune():
    """Remove unbound floating IPs."""
    actions.IPs().prune()


@cli.group()
def images():
    """Manage images."""
    pass


@images.command('list')
def images_list():
    """List all available images."""
    actions.Images().list()


@cli.group()
def email():
    """Manage email settings."""
    pass


@email.command('forward')
def email_forward():
    """Add DNS records to forward email."""
    actions.Email().forward()


@email.command('whitelabel')
def email_whitelabel():
    """Add DNS records to whitelabel email domains."""
    actions.Email().whitelabel()


@cli.group()
def backups():
    """Manage backup settings."""
    pass


@backups.command('configure')
def backups_configure():
    """Configure remote resources for backups."""
    actions.Backups().configure()


@cli.group()
def deploy():
    """Manage deployments."""
    pass


@deploy.command('to')
@click.argument('environment', type=click.Choice(ENVIRONMENTS))
@click.option('--inventory', type=click.Choice(ENVIRONMENTS), default=ENVIRONMENTS[0])
def deploy_to(environment, inventory):
    """Deploy application code to an environment."""
    actions.Deploy().deploy(environment, inventory)


@deploy.command('rollback')
@click.argument('environment', type=click.Choice(ENVIRONMENTS))
@click.option('--inventory', type=click.Choice(ENVIRONMENTS), default=ENVIRONMENTS[0])
def deploy_rollback(environment, inventory):
    """Roll back deployed code in an environment."""
    actions.Deploy().roll_back(environment, inventory)
