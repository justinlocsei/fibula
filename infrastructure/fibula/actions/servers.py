import click
from digitalocean import DataReadError, Droplet

from fibula.actions.base import BaseAction
from fibula.data import load_data


class Servers(BaseAction):
    """A collection of actions for servers.

    These actions use a local server manifest as the source of truth, with each
    server being assigned a unique name that will match the name of a droplet.
    """

    log_prefix = 'servers'

    def create(self):
        """Create droplets that appear in the manifest but not on Digital Ocean."""
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
            self.ui.create('Created a "%s" droplet' % server['name'])

        for droplet_name in droplet_names:
            self.ui.info('A "%s" droplet already exists' % droplet_name)

    def sync(self):
        """Update all droplets to match the manifest."""
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
            ui = self.ui.group(droplet.name)
            divergent = False

            # Sync backups
            if droplet.backups != server['backups']:
                divergent = True
                if server['backups']:
                    droplet.enable_backups()
                    ui.create('Enabled backups')
                else:
                    if ui.confirm('Are you sure you want to disable backups on this droplet?', destructive=True):
                        droplet.disable_backups()
                        ui.delete('Disabled backups')
                    else:
                        ui.skip('Not disabling backups')

            # Sync droplet size
            if droplet.size_slug != server['size']:
                divergent = True
                if ui.confirm('Are you sure you want to change this droplet\'s size from %s to %s?' % (droplet.size_slug, server['size']), destructive=True):
                    try:
                        resize = droplet.resize(server['size'])
                    except DataReadError as e:
                        ui.error('Could not resize the droplet: %s' % e)
                    else:
                        ui.create('Started the resize process')
                else:
                    ui.skip('Not resizing the droplet')

            # Warn about different regions
            if droplet.region['slug'] != server['region']:
                divergent = True
                ui.warn('This droplet is in the "%s" region, but it should be in "%s"' % (droplet.region['slug'], server['region']))
                ui.warn('To change regions, you must spin up a new droplet')

            # Warn about different images
            if droplet.image['id'] != server['image']:
                divergent = True
                ui.warn('This droplet uses the "%s" image, but it should use "%s"' % (droplet.image['id'], server['image']))
                ui.warn('To change the image, you must spin up a new droplet')

            if not divergent:
                ui.info('Droplet configuration matches the manifest')

        for droplet_name in to_skip:
            self.ui.warn('The "%s" droplet is absent from the manifest' % droplet_name)

    def prune(self):
        """Remove any remote servers that do not appear in the manifest."""
        droplets = self.do.get_all_droplets()
        servers = load_data('servers')

        server_names = [s['name'] for s in servers]
        to_prune = [d for d in droplets if d.name not in server_names]
        to_skip = [d.name for d in droplets if d.name in server_names]

        # Remove unused droplets
        for droplet in to_prune:
            if self.ui.confirm('Are you sure you want to destroy the "%s" droplet?' % droplet.name, destructive=True):
                droplet.destroy()
                self.ui.delete('Destroyed the "%s" droplet' % droplet.name)
            else:
                self.ui.skip('Not destroying the "%s" droplet' % droplet.name)

        for droplet_name in to_skip:
            self.ui.skip('This droplet is present in the manifest')
