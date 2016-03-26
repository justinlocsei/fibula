from urlparse import urlparse

from fibula.actions.base import BaseAction
from fibula.data import load_data


class DNS(BaseAction):
    """A collection of actions for manipulating DNS records."""

    log_prefix = 'dns'

    def add(self):
        """Create DNS entries for each server's subdomains."""
        local_servers = load_data('cloud')['servers']
        remote_domains = self.do.get_all_domains()

        for domain in remote_domains:
            subdomains = [s.name for s in self._get_subdomains(domain)]

            for server in local_servers:
                ui = self.ui.group(domain.name, server['name'])
                droplet = self.get_named_droplet(server['name'])
                floating_ip = self.get_droplet_floating_ip(droplet)

                for hostname in server['hostnames']:
                    parsed = urlparse(hostname)
                    subdomain, host = parsed.path.split(".", 1)
                    if host != domain.name:
                        continue

                    if subdomain not in subdomains:
                        domain.create_new_domain_record(
                            type='A',
                            name=subdomain,
                            data=floating_ip.ip
                        )
                        ui.create('Added hostname "%s"' % hostname)
                    else:
                        ui.skip('Hostname "%s" already present' % hostname)

    def sync(self):
        """Ensure that the subdomains for servers match the DNS records."""
        local_servers = load_data('cloud')['servers']
        remote_domains = self.do.get_all_domains()

        for domain in remote_domains:
            subdomains = self._get_subdomains(domain)
            subdomain_names = [s.name for s in subdomains]

            for server in local_servers:
                ui = self.ui.group(domain.name, server['name'])
                droplet = self.get_named_droplet(server['name'])
                floating_ip = self.get_droplet_floating_ip(droplet)

                for hostname in server['hostnames']:
                    parsed = urlparse(hostname)
                    subdomain, host = parsed.path.split(".", 1)
                    if host != domain.name:
                        continue

                    remote_subdomains = [s for s in subdomains if s.name == subdomain]
                    for remote_subdomain in remote_subdomains:
                        if remote_subdomain.data != floating_ip.ip:
                            remote_subdomain.data = floating_ip.ip
                            remote_subdomain.save()
                            ui.update('Changed the IP address for "%s" to %s' % (hostname, floating_ip.ip))
                        else:
                            ui.skip('The IP address for "%s" is correct' % hostname)

    def _get_subdomains(self, domain):
        """Get the subdomain names associated with a domain.

        Args:
            domain (digitalocean.Domain): A domain instance

        Returns:
            list: A list of subdomain names as strings
        """
        return [
            record for record in domain.get_records()
            if record.type == 'A' and record.name != '@'
        ]
