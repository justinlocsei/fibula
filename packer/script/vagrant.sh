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

# Install NFS and bindfs in order to use NFS synced folders
apt-get -y install bindfs nfs-common

# Use cachefilesd to improve synced-folder performance over NFS
apt-get -y install cachefilesd
sed -i "s/^#RUN=yes/RUN=yes/" /etc/default/cachefilesd
update-rc.d cachefilesd enable
