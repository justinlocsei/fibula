#!/bin/bash -eux

USER=$CYB_SSH_USERNAME
HOME_DIR=/home/$USER

# Install the VirtualBox guest additions
mount -o loop "$HOME_DIR/$CYB_GUEST_ADDITIONS_PATH" /mnt
sh /mnt/VBoxLinuxAdditions.run
umount /mnt
rm -rf "${HOME_DIR:?}/$CYB_GUEST_ADDITIONS_PATH"
rm -f "$HOME_DIR/.vbox_version"
