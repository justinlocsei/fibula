import click
from digitalocean import DataReadError, Droplet

from fibula.actions.base import BaseAction
from fibula.data import load_data


class Servers(BaseAction):
    """A collection of actions for servers.

    These actions work off of a local manifest of servers that uses a unique
    name for each server.  This name is used to compare the local servers to the
    list of created droplets.
    """

    def create(self):
        """Create droplets that appear in the local list but not in Digital Ocean."""
        ssh_keys = self.do.get_all_sshkeys()
        droplets = self.do.get_all_droplets()

        servers = load_data('servers')
        droplet_names = [d.name for d in droplets]
        to_create = [s for s in servers if s['name'] not in droplet_names]

        # Create all missing droplets
        for server in to_create:
            droplet = Droplet(
                backups=server['backups'],
                image=server['image'],
                name=server['name'],
                region=server['region'],
                size_slug=server['size'],
                ssh_keys=[k.id for k in ssh_keys],
                token=self.token
            )
            droplet.create()
            self.log('Created droplet %s for the "%s" server' % (droplet.id, server['name']), created=True)

        for droplet_name in droplet_names:
            self.log('A droplet already exists for the "%s" server' % droplet_name)

    def sync(self):
        """Update all droplets to match the local server configuration."""
        droplets = self.do.get_all_droplets()

        servers = load_data('servers')
        server_names = [s['name'] for s in servers]

        to_skip = [d.name for d in droplets if d.name not in server_names]

        to_edit = []
        for droplet in droplets:
            for server in servers:
                if droplet.name == server['name']:
                    to_edit.append((droplet, server))

        for droplet, server in to_edit:

            # Sync backups
            if droplet.backups != server['backups']:
                if server['backups']:
                    droplet.enable_backups()
                    self.log('Enabled backups for the "%s" server' % droplet.name, created=True)
                else:
                    if click.confirm('Are you sure you want to disable backups for the "%s" server?' % droplet.name):
                        droplet.disable_backups()
                        self.log('Disabled backups for the "%s" server' % droplet.name, deleted=True)
                    else:
                        self.log('Not disabling backups for the "%s" server' % droplet.name)

            # Sync droplet size
            if droplet.size_slug != server['size']:
                if click.confirm('Are you sure you want to change the "%s" server from %s to %s?' % (droplet.name, droplet.size_slug, server['size'])):
                    try:
                        resize = droplet.resize(server['size'])
                    except DataReadError as e:
                        self.log('Could not resize the "%s" server: %s' % (droplet.name, e), deleted=True)
                    else:
                        self.log('Started the resize process for the "%s" server' % droplet.name, created=True)
                else:
                    self.log('Not resizing the "%s" server' % droplet.name)

            # Warn about different regions
            if droplet.region['slug'] != server['region']:
                self.warn('The "%s" droplet is in the "%s" region, but it should be in "%s"' % (droplet.name, droplet.region['slug'], server['region']))
                self.warn('To relocate this droplet, you must spin up a new droplet')

            # Warn about different images
            if droplet.image['id'] != server['image']:
                self.warn('The "%s" droplet uses the "%s" image, but it should use "%s"' % (droplet.name, droplet.image['id'], server['image']))
                self.warn('To change the image for this droplet, you must spin up a new droplet')

        for droplet_name in to_skip:
            self.log('The droplet for the "%s" server does not exist locally' % droplet_name)

    def prune(self):
        """Remove any remote servers that do not appear in the local list."""
        droplets = self.do.get_all_droplets()

        servers = load_data('servers')
        server_names = [s['name'] for s in servers]

        to_prune = [d for d in droplets if d.name not in server_names]
        to_skip = [d.name for d in droplets if d.name in server_names]

        for droplet in to_prune:
            if click.confirm('Are you sure you want to destroy the "%s" droplet?' % droplet.name):
                droplet.destroy()
                self.log('Destroyed the "%s" droplet' % droplet.name, deleted=True)
            else:
                self.log('Not destroying the "%s" droplet' % droplet.name)

        for droplet_name in to_skip:
            self.log('Not removing the "%s" droplet' % droplet_name)
