from digitalocean import SSHKey

from fibula.actions.base import BaseAction
from fibula.data import load_data


class SSHKeys(BaseAction):
    """A collection of actions for SSH keys."""

    log_prefix = 'ssh'

    def sync(self):
        """Ensure that the Digital Ocean SSH keys match the local keys.

        This adds any local keys that are not registered with Digital Ocean, and
        updates the name and public key of any matching remote keys to match
        the local values.  If a key is found on Digital Ocean that does not
        exist in the local list, it will be removed.

        Each local key is associated with a Digital Ocean account, so all keys
        associated with another email address will be ignored.
        """
        server_keys = self.do.get_all_sshkeys()
        account_email = self.do.get_account().email

        all_keys = load_data('ssh_keys')
        local_keys = [key for key in all_keys if key['email'] == account_email]

        for local_key in local_keys:
            ui = self.ui.group(local_key['name'])
            on_server = False
            updated = False

            for server_key in server_keys:

                # Sync the remote name with the local one for identical keys
                if server_key.public_key == local_key['key']:
                    on_server = True
                    if server_key.name != local_key['name']:
                        server_key.name = local_key['name']
                        server_key.edit()
                        ui.update('Updated the remote name to "%s"' % server_key.name)
                        updated = True

                # Sync the remote key with the local one when the name has changed
                elif server_key.name == local_key['name']:
                    on_server = True
                    if server_key.public_key != local_key['key']:
                        server_key.public_key = local_key['key']
                        server_key.edit()
                        ui.update('Updated the remote key "%s"' % server_key.public_key)
                        updated = True

            # Create a new remote key if the local key is not on the server
            if not on_server:
                ssh_key = SSHKey(
                    name=local_key['name'],
                    public_key=local_key['key'],
                    token=self.token
                )
                ssh_key.create()
                ui.create('Created a remote key')
            elif not updated:
                ui.skip('Not modifying the remote key')

        # Remove any remote keys that no longer appear locally
        server_keys = self.do.get_all_sshkeys()
        for server_key in server_keys:
            matches_name = False
            matches_key = False
            for local_key in local_keys:
                matches_name = matches_name or local_key['name'] == server_key.name
                matches_key = matches_key or local_key['key'] == server_key.public_key
            if not matches_name and not matches_key:
                server_key.destroy()
                self.ui.delete('Removed remote SSH key "%s"' % server_key.name)
