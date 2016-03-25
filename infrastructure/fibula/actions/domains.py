from digitalocean import Domain

from fibula.actions.base import BaseAction
from fibula.data import load_data


class Domains(BaseAction):
    """A collection of actions for network domains."""

    log_prefix = 'domains'

    def sync(self):
        """Ensure that the Digital Ocean domains match the manifest.

        This ensures that Digital Ocean has an IP address bound to each
        top-level domain, and then ensures that any server subdomains are
        properly associated with an IP address.
        """
        cloud = load_data('cloud')
        local_servers = cloud['servers']
        local_domains = cloud['domains']
        local_domain_names = [d['fqdn'] for d in local_domains]

        remote_domains = self.do.get_all_domains()
        droplets = self.do.get_all_droplets()
        floating_ips = self.do.get_all_floating_ips()

        remote_domain_names = [d.name for d in remote_domains]
        missing_domains = [d for d in local_domains if d['fqdn'] not in remote_domain_names]
        orphan_domains = [d for d in remote_domains if d.name not in local_domain_names]

        existing_domains = []
        for local_domain in local_domains:
            for remote_domain in remote_domains:
                if local_domain['fqdn'] == remote_domain.name:
                    existing_domains.append((local_domain, remote_domain))

        # Create all missing domains and associate them with their root server
        for domain in missing_domains:
            droplet = self._get_named_droplet(domain['root_server'], droplets)
            floating_ip = self._get_floating_ip_for_droplet(droplet, floating_ips)

            remote_domain = Domain(
                name=domain['fqdn'],
                ip_address=floating_ip.ip,
                token=self.token
            )
            remote_domain.create()
            remote_domains.append(remote_domain)
            self.ui.create('Created the "%s" domain bound to the "%s" server' % (domain['fqdn'], domain['root_server']))

        # Ensure that the A record of each existing domain points to the right IP
        for local_domain, remote_domain in existing_domains:
            a_record = [r for r in remote_domain.get_records() if r.type == 'A'][0]
            droplet = self._get_named_droplet(local_domain['root_server'], droplets)
            floating_ip = self._get_floating_ip_for_droplet(droplet, floating_ips)

            if a_record.data != floating_ip.ip:
                previous_ip = a_record.data
                a_record.data = floating_ip.ip
                a_record.save()
                self.ui.update('Changed the floating IP of the "%s" domain\'s "%s" root server from "%s" to "%s"' % (
                    local_domain['fqdn'],
                    local_domain['root_server'],
                    previous_ip,
                    floating_ip.ip
                ))
            else:
                self.ui.skip('The floating IP for the "%s" domain\'s "%s" root server is correct' % (local_domain['fqdn'], local_domain['root_server']))

        # Remove any remote domains that do not exist locally
        for domain in orphan_domains:
            if self.ui.confirm('Are you sure you want to destroy the "%s" domain?' % domain.name):
                domain.destroy()
                self.ui.delete('Destroyed the "%s" domain' % domain.name)
            else:
                self.ui.skip('Not destroying the "%s" domain' % domain.name)

    def _get_named_droplet(self, name, droplets):
        """Get a named droplet from a collection of droplets.

        Args:
            name (str): The name of a droplet
            droplets (list): A collection of `digitalocean.Droplet` instances

        Returns:
            digitalocean.Droplet: The named droplet
        """
        matches = [d for d in droplets if d.name == name]
        if len(matches) > 1:
            self.ui.abort('Multiple servers named "%s" exist' % name)
        elif not len(matches):
            self.ui.abort('No server found named "%s"' % name)
        return matches[0]

    def _get_floating_ip_for_droplet(self, droplet, floating_ips):
        """Get the floating IP for a droplet from a collection of IPs.

        Args:
            droplet (digitalocean.Droplet): A single droplet
            floating_ips (list): A collection of `digitalocean.FloatingIP` instances

        Returns:
            digitalocean.FloatingIP: The droplet's floating IP
        """
        matches = [f for f in floating_ips if f.droplet['id'] == droplet.id]
        if len(matches) > 1:
            self.ui.abort('Multiple floating IPs bound to the "%s" server exist' % droplet.name)
        elif not len(matches):
            self.ui.abort('No floating IP is bound to the "%s" server' % droplet.name)
        return matches[0]
