from fibula.actions.base import BaseAction
from fibula.data import load_data


class Email(BaseAction):
    """A collection of actions for manipulating email information."""

    log_prefix = 'email'

    def whitelabel(self):
        """Create DNS entries to whitelabel all email-sending domains."""
        whitelabels = load_data('email')['whitelabels']
        remote_domains = self.do.get_all_domains()

        for remote_domain in remote_domains:
            domain_records = remote_domain.get_records()

            for whitelabel in whitelabels:
                if whitelabel['domain'] != remote_domain.name:
                    continue

                ui = self.ui.group(remote_domain.name)
                for cname in whitelabel['cnames']:
                    target = '%s.' % cname['data']
                    match = [r for r in domain_records if r.name == cname['host']]

                    if not len(match):
                        remote_domain.create_new_domain_record(
                            type='CNAME',
                            name=cname['host'],
                            data=target
                        )
                        ui.create('Added CNAME for "%s" pointing to "%s"' % (cname['host'], cname['data']))
                    else:
                        remote_record = match[0]
                        if remote_record.data == cname['data']:
                            ui.skip('CNAME for "%s" has accurate data' % cname['host'])
                        else:
                            remote_record.data = target
                            remote_record.save()
                            ui.update('Updated CNAME for "%s" to point to "%s"' % (cname['host'], cname['data']))
