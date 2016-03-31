from fibula.actions.base import BaseAction
from fibula.data import load_data


class Email(BaseAction):
    """A collection of actions for manipulating email information."""

    log_prefix = 'email'

    def whitelabel(self):
        """Create DNS entries to whitelabel all email-sending domains."""
        for email_domain, remote_domain, domain_records in self._each_domain_group():
            ui = self.ui.group(remote_domain.name)

            for cname in email_domain['whitelabels']:
                final_name = str(cname['name'])
                final_data = '%s.' % cname['data']
                match = [r for r in domain_records if r.name == final_name and r.type == 'CNAME']

                if not len(match):
                    remote_domain.create_new_domain_record(
                        type='CNAME',
                        name=final_name,
                        data=final_data
                    )
                    ui.create('Added CNAME "%s" pointing to "%s"' % (cname['name'], cname['data']))
                else:
                    remote_record = match[0]
                    if remote_record.data == cname['data']:
                        ui.skip('CNAME "%s" has accurate data' % cname['name'])
                    else:
                        remote_record.data = final_data
                        remote_record.save()
                        ui.update('Updated CNAME "%s" to point to "%s"' % (cname['name'], cname['data']))

    def forward(self):
        """Set up MX records to forward email."""
        for email_domain, remote_domain, domain_records in self._each_domain_group():
            ui = self.ui.group(remote_domain.name)

            mx = email_domain['mx']
            final_data = '%s.' % mx['data']
            match = [r for r in domain_records if r.name == mx['hostname'] and r.type == 'MX']

            if not len(match):
                remote_domain.create_new_domain_record(
                    type='MX',
                    name=mx['hostname'],
                    priority=mx['priority'],
                    data=final_data
                )
                ui.create('Added MX record "%s" pointing to "%s"' % (mx['hostname'], mx['data']))
            else:
                remote_mx = match[0]

                if remote_mx.data == mx['data']:
                    ui.skip('MX record "%s" has accurate data' % mx['hostname'])
                else:
                    remote_mx.data = final_data
                    remote_mx.save()
                    ui.update('Updated MX record "%s" to point to "%s"' % (mx['hostname'], mx['data']))

                if remote_mx.priority == mx['priority']:
                    ui.skip('MX record "%s" has accurate priority' % mx['hostname'])
                else:
                    remote_mx.priority = mx['priority']
                    remote_mx.save()
                    ui.update('Updated the priority of MX record "%s" to %d' % (mx['hostname'], mx['priority']))

    def _each_domain_group(self):
        """Yield a three-tuple of a local domain, remote domain, and domain records."""
        email_domains = load_data('email')
        remote_domains = self.do.get_all_domains()

        for remote_domain in remote_domains:
            domain_records = remote_domain.get_records()

            for email_domain in email_domains:
                if email_domain['domain'] == remote_domain.name:
                    yield (email_domain, remote_domain, domain_records)
