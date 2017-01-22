from fibula.actions.base import BaseAction


class IPs(BaseAction):
    """A collection of actions for manipulating IP addresses."""

    log_prefix = 'ips'

    def prune(self):
        """Remove any unbound floating IPs."""
        floating_ips = self.do.manager.get_all_floating_ips()

        for floating_ip in floating_ips:
            ui = self.ui.group(floating_ip.ip)

            if self._floating_ip_is_bound(floating_ip):
                ui.skip('Floating IP is bound to droplet %s' % floating_ip.droplet['id'])
            else:
                if ui.confirm('Are you sure you want to delete the %s floating IP?' % floating_ip.ip):
                    floating_ip.destroy()
                    ui.delete('Removed floating IP')
                else:
                    ui.skip('Not removing floating IP')

    def _floating_ip_is_bound(self, ip):
        """Determine whether a floating IP is bound to a droplet.

        Args:
            ip (digitalocean.FloatingIP): A floating IP

        Returns:
            bool: Whether the IP is bound to a droplet
        """
        droplet_names = [d.name for d in self.do.manager.get_all_droplets()]
        return ip.droplet is not None and ip.droplet['name'] in droplet_names
