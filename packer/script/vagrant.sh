#!/bin/bash -eux

USER=$CYB_SSH_USERNAME
SSH_DIR=/home/$USER/.ssh

# Grant the Vagrant user passwordless sudo
echo "$USER  ALL=(ALL)  NOPASSWD: ALL" >> /etc/sudoers

# Add the custom Vagrant key
mkdir -pm 700 "$SSH_DIR"
echo "$FIBULA_VAGRANT_SSH_KEY" > "$SSH_DIR/authorized_keys"
chmod 0600 "$SSH_DIR/authorized_keys"
chown -R "$USER:$USER" "$SSH_DIR"
