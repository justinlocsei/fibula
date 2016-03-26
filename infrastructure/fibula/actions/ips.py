from fibula.actions.base import BaseAction
from fibula.data import load_data


class IPs(BaseAction):
    """A collection of actions for manipulating IP addresses."""

    log_prefix = 'ips'

    def prune(self):
        """Remove any unbound floating IPs."""
        floating_ips = self.do.get_all_floating_ips()

        for floating_ip in floating_ips:
            ui = self.ui.group(floating_ip.ip)

            if floating_ip.droplet:
                ui.skip('Floating IP is bound to droplet %s' % floating_ip.droplet['id'])
            else:
                if ui.confirm('Are you sure you want to delete the %s floating IP?' % floating_ip.ip):
                    floating_ip.destroy()
                    ui.delete('Removed floating IP')
                else:
                    ui.skip('Not removing floating IP')
