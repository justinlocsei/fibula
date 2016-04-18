from contextlib import contextmanager
import time

from digitalocean import DataReadError, Droplet, FloatingIP

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
        ssh_keys = self.do.manager.get_all_sshkeys()
        droplets = self.do.manager.get_all_droplets()

        servers = load_data('cloud')['servers']
        droplet_names = [d.name for d in droplets]
        missing_servers = [s for s in servers if s['name'] not in droplet_names]

        for server in missing_servers:
            ui = self.ui.group(server['name'])
            config = server['config']
            droplet = Droplet(
                backups=config['backups'],
                image=self._get_image_by_slug(config['image']).id,
                name=server['name'],
                region=config['region'],
                size_slug=config['size'],
                ssh_keys=[k.id for k in ssh_keys],
                token=self.do.token
            )
            droplet.create()
            ui.create('Created droplet %s' % droplet.id)

            # Attach a floating IP to the droplet
            with self._wait_for_droplet(droplet, ui):
                ip = FloatingIP(droplet_id=droplet.id, token=self.do.token)
                ip.create()
                ui.create('Added a floating IP of %s' % ip.ip)

        for droplet_name in droplet_names:
            ui = self.ui.group(droplet_name)
            ui.skip('A droplet already exists')

    def sync(self):
        """Update all droplets to match the manifest.

        This changes any mutable server properties, and emits a warning when
        differences are detected for properties that cannot be changed for an
        existing instance, such as the region.
        """
        droplets = self.do.manager.get_all_droplets()
        servers = load_data('cloud')['servers']

        to_edit = []
        for droplet in droplets:
            for server in servers:
                if droplet.name == server['name']:
                    to_edit.append((droplet, server))

        for droplet, server in to_edit:
            config = server['config']
            ui = self.ui.group(droplet.name)
            divergent = False

            # Sync backups
            if droplet.backups != config['backups']:
                divergent = True
                if config['backups']:
                    droplet.enable_backups()
                    ui.create('Enabled backups')
                else:
                    if ui.confirm('Are you sure you want to disable backups on the "%s" droplet?' % droplet.name):
                        droplet.disable_backups()
                        ui.delete('Disabled backups')
                    else:
                        ui.skip('Not disabling backups')

            # Sync droplet size
            if droplet.size_slug != config['size']:
                divergent = True
                if ui.confirm('Are you sure you want to change the "%s" droplet\'s size from %s to %s?' % (droplet.name, droplet.size_slug, config['size'])):
                    try:
                        droplet.resize(config['size'])
                    except DataReadError as e:
                        ui.error('Could not resize the droplet: %s' % e)
                    else:
                        ui.create('Started the resize process')
                else:
                    ui.skip('Not resizing the droplet')

            # Warn about different regions
            if droplet.region['slug'] != config['region']:
                divergent = True
                ui.warn('This droplet is in the "%s" region, but it should be in "%s"' % (droplet.region['slug'], config['region']))
                ui.warn('To change regions, you must spin up a new droplet')

            # Warn about different images
            if droplet.image['slug'] != config['image']:
                divergent = True
                ui.warn('This droplet uses the "%s" image, but it should use "%s"' % (droplet.image['slug'], config['image']))
                ui.warn('To change the image, you must spin up a new droplet')

            if not divergent:
                ui.skip('Droplet configuration matches the manifest')

        server_names = [s['name'] for s in servers]
        missing_servers = [d.name for d in droplets if d.name not in server_names]

        for droplet_name in missing_servers:
            ui = self.ui.group(droplet_name)
            ui.warn('Droplet not present in the manifest')

    def prune(self):
        """Remove any remote servers that do not appear in the manifest."""
        droplets = self.do.manager.get_all_droplets()
        servers = load_data('cloud')['servers']

        server_names = [s['name'] for s in servers]
        orphan_servers = [d for d in droplets if d.name not in server_names]
        local_servers = [d.name for d in droplets if d.name in server_names]

        for droplet in orphan_servers:
            ui = self.ui.group(droplet.name)
            if ui.confirm('Are you sure you want to destroy the "%s" droplet?' % droplet.name):
                droplet.destroy()
                ui.delete('Droplet destroyed')
            else:
                ui.skip('Droplet not destroyed')

        for droplet_name in local_servers:
            ui = self.ui.group(droplet_name)
            ui.skip('Droplet present in the manifest')

    @contextmanager
    def _wait_for_droplet(self, droplet, ui):
        """Run code once a droplet has been created.

        Args:
            droplet (digitalocean.Droplet): A droplet
            ui (fibula.communicator.Communicator): A communicator instance for logging
        """
        is_available = False
        while not is_available:
            actions = droplet.get_actions()
            [a.load() for a in actions]
            is_available = any([a.type == 'create' and a.status == 'completed' for a in actions])

            if not is_available:
                ui.info('Waiting for droplet...')
                time.sleep(5)

        yield

    def _get_image_by_slug(self, slug):
        """Return the image associated with a slug.

        Args:
            slug (str): The slug for an image

        Returns:
            digitalocean.Image: The image matching the slug
        """
        images = self.do.manager.get_distro_images()
        matches = [i for i in images if i.slug == slug]

        if len(matches):
            return matches[0]
        else:
            self.ui.abort('No image found with the slug "%s"' % slug)
