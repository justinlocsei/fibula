from fibula.actions.base import BaseAction
from fibula.data import load_data


class DNS(BaseAction):
    """A collection of actions for manipulating DNS records."""

    log_prefix = 'dns'

    def add(self):
        """Create DNS entries for each server's subdomains."""
        local_servers = load_data('cloud')['servers']
        remote_domains = self.do.manager.get_all_domains()

        for domain in remote_domains:
            subdomains = [s.name for s in self._get_subdomains(domain)]

            for server in local_servers:
                ui = self.ui.group(domain.name, server['name'])
                droplet = self.do.get_named_droplet(server['name'])
                floating_ip = self.do.get_droplet_floating_ip(droplet)

                for fqdn in server['fqdns']:
                    subdomain_name, domain_name = fqdn.split(".", 1)
                    if domain_name != domain.name:
                        continue

                    if subdomain_name not in subdomains:
                        domain.create_new_domain_record(
                            type='A',
                            name=subdomain_name,
                            data=floating_ip.ip
                        )
                        ui.create('Added DNS record for "%s"' % fqdn)
                    else:
                        ui.skip('DNS record for "%s" already present' % fqdn)

    def sync(self):
        """Ensure that the subdomains for servers match the DNS records."""
        local_servers = load_data('cloud')['servers']
        remote_domains = self.do.manager.get_all_domains()

        for domain in remote_domains:
            subdomains = self._get_subdomains(domain)
            subdomain_names = [s.name for s in subdomains]

            for server in local_servers:
                ui = self.ui.group(domain.name, server['name'])
                droplet = self.do.get_named_droplet(server['name'])
                floating_ip = self.do.get_droplet_floating_ip(droplet)

                for fqdn in server['fqdns']:
                    subdomain_name, domain_name = fqdn.split(".", 1)
                    if domain_name != domain.name:
                        continue

                    remote_subdomains = [s for s in subdomains if s.name == subdomain_name]
                    for remote_subdomain in remote_subdomains:
                        if remote_subdomain.data != floating_ip.ip:
                            remote_subdomain.data = floating_ip.ip
                            remote_subdomain.save()
                            ui.update('Changed the IP address for "%s" to %s' % (fqdn, floating_ip.ip))
                        else:
                            ui.skip('The IP address for "%s" is correct' % fqdn)

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
