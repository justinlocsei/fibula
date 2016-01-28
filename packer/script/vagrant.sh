#!/bin/bash -eux

USER=$CYB_SSH_USERNAME
SSH_DIR=/home/$USER/.ssh

# Grant the Vagrant user passwordless sudo
echo "$USER  ALL=(ALL)  NOPASSWD: ALL" >> /etc/sudoers

# Add the custom Vagrant key
mkdir -pm 700 "$SSH_DIR"
cat "$CYB_SSH_KEY_PATH" > "$SSH_DIR/authorized_keys"
rm "$CYB_SSH_KEY_PATH"
chmod 0600 "$SSH_DIR/authorized_keys"
chown -R "$USER:$USER" "$SSH_DIR"

# Install NFS packages to use NFS on the guest or host for synced folders
apt-get -y install bindfs nfs-common nfs-kernel-server

# Enable SSH agent forwarding for the root user
echo "Defaults>root  env_keep+=SSH_AUTH_SOCK" >> /etc/sudoers
