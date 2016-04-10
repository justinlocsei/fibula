from digitalocean import SSHKey

from fibula.actions.base import BaseAction
from fibula.data import load_data


class SSHKeys(BaseAction):
    """A collection of actions for SSH keys.

    Each of these actions only operates on the set of keys associated with the
    current user account.
    """

    log_prefix = 'ssh'

    def add(self):
        """Add all SSH keys that are present in the manifest to Digital Ocean."""
        remote_keys = self.do.manager.get_all_sshkeys()
        local_keys = self._get_local_keys()

        for local_key in local_keys:
            ui = self.ui.group(local_key['name'])
            on_server = any([self._match_keys(local_key, r) for r in remote_keys])

            if on_server:
                ui.skip('Remote key already exists')
            else:
                ssh_key = SSHKey(
                    name=local_key['name'],
                    public_key=local_key['key'],
                    token=self.token
                )
                ssh_key.create()
                ui.create('Created remote key %s' % ssh_key.id)


    def sync(self):
        """Ensure that the values for Digital Ocean SSH keys match the manifest."""
        remote_keys = self.do.manager.get_all_sshkeys()
        local_keys = self._get_local_keys()

        for remote_key in remote_keys:
            ui = self.ui.group(remote_key.name)
            updated = False
            is_local = False

            for local_key in local_keys:
                if remote_key.public_key == local_key['key']:
                    is_local = True
                    if remote_key.name != local_key['name']:
                        remote_key.name = local_key['name']
                        remote_key.edit()
                        ui.update('Updated the remote name to "%s"' % remote_key.name)
                        updated = True
                elif remote_key.name == local_key['name']:
                    is_local = True
                    if remote_key.public_key != local_key['key']:
                        remote_key.public_key = local_key['key']
                        remote_key.edit()
                        ui.update('Updated the remote key "%s"' % remote_key.public_key)
                        updated = True

            if not is_local:
                ui.warn('Key not present in the local manifest')
            elif not updated:
                ui.skip('Remote and local configurations match')

    def prune(self):
        """Remove any Digital Ocean SSH keys that are not present in the manifest."""
        remote_keys = self.do.manager.get_all_sshkeys()
        local_keys = self._get_local_keys()

        for remote_key in remote_keys:
            ui = self.ui.group(remote_key.name)
            on_server = any([self._match_keys(l, remote_key) for l in local_keys])

            if on_server:
                ui.skip('Remote key is present in the manifest')
            else:
                if ui.confirm('Are you sure you want to delete the "%s" key?' % remote_key.name):
                    remote_key.destroy()
                    ui.delete('Removed remote key')
                else:
                    ui.skip('Not removing remote key')

    def _get_local_keys(self):
        """Get all local SSH keys for the current Digital Ocean user.

        Returns:
            list: A list of dicts describing SSH keys
        """
        email = self.do.manager.get_account().email
        ssh_keys = load_data('ssh_keys')
        return [k for k in ssh_keys if k['email'] == email]

    def _match_keys(self, local, remote):
        """Determine if a local key describes a remote key's data.

        Args:
            local (dict): A local SSH key
            remote (digitalocean.SSHKey): A remote SSH key

        Returns:
            bool: Whether the keys describe the same data
        """
        return local['name'] == remote.name or local['key'] == remote.public_key
