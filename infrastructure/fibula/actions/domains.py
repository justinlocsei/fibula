from digitalocean import Domain

from fibula.actions.base import BaseAction
from fibula.data import load_data


class Domains(BaseAction):
    """A collection of actions for network domains."""

    log_prefix = 'domains'

    def create(self):
        """Create domains on Digital Ocean from the manifest."""
        local_domains = load_data('cloud')['domains']
        remote_domains = self.do.get_all_domains()

        remote_domain_names = [d.name for d in remote_domains]
        missing_domains = [d for d in local_domains if d['fqdn'] not in remote_domain_names]

        for domain in missing_domains:
            ui = self.ui.group(domain['fqdn'])
            droplet = self.get_named_droplet(domain['root_server'])
            floating_ip = self.get_droplet_floating_ip(droplet)

            remote_domain = Domain(
                name=domain['fqdn'],
                ip_address=floating_ip.ip,
                token=self.token
            )
            remote_domain.create()
            ui.create('Bound domain to the "%s" server' % domain['root_server'])

            remote_domain.create_new_domain_record(
                type='CNAME',
                name='*',
                data='@'
            )
            ui.create('Created a root CNAME record')

        for domain in remote_domains:
            ui = self.ui.group(domain.name)
            ui.skip('Domain already exists')

    def sync(self):
        """Ensure that the Digital Ocean domains match the manifest."""
        local_domains = load_data('cloud')['domains']
        remote_domains = self.do.get_all_domains()

        existing_domains = []
        for local_domain in local_domains:
            for remote_domain in remote_domains:
                if local_domain['fqdn'] == remote_domain.name:
                    existing_domains.append((local_domain, remote_domain))

        for local_domain, remote_domain in existing_domains:
            ui = self.ui.group(remote_domain.name)
            a_record = [r for r in remote_domain.get_records() if r.type == 'A'][0]
            droplet = self.get_named_droplet(local_domain['root_server'])
            floating_ip = self.get_droplet_floating_ip(droplet)

            if a_record.data != floating_ip.ip:
                previous_ip = a_record.data
                a_record.data = floating_ip.ip
                a_record.save()
                ui.update('Changed the floating IP of the "%s" root server from "%s" to "%s"' % (
                    local_domain['root_server'],
                    previous_ip,
                    floating_ip.ip
                ))
            else:
                ui.skip('The floating IP for the "%s" root server is correct' % local_domain['root_server'])

    def prune(self):
        """Remove unused remote domains."""
        local_domains = load_data('cloud')['domains']
        remote_domains = self.do.get_all_domains()

        local_domain_names = [d['fqdn'] for d in local_domains]
        remote_domain_names = [d.name for d in remote_domains]

        orphan_domains = [d for d in remote_domains if d.name not in local_domain_names]
        existing_domains = [d for d in local_domains if d['fqdn'] in remote_domain_names]

        for domain in orphan_domains:
            ui = self.ui.group(domain.name)
            if ui.confirm('Are you sure you want to delete the "%s" domain?' % domain.name):
                domain.destroy()
                ui.delete('Domain destroyed')
            else:
                ui.skip('Not destroying the domain')

        for domain in existing_domains:
            ui = self.ui.group(domain['fqdn'])
            ui.skip('Domain present in the manifest')
