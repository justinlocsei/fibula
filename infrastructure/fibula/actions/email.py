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
                    final_name = str(cname['name'])
                    final_data = '%s.' % cname['data']
                    match = [r for r in domain_records if r.name == final_name]

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
