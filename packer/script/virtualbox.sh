#!/bin/bash -eux

USER=$CYB_SSH_USERNAME
HOME_DIR=/home/$USER

# Install the VirtualBox guest additions
VBOX_VERSION=$(cat "$HOME_DIR/.vbox_version")
mount -o loop "$HOME_DIR/VBoxGuestAdditions_$VBOX_VERSION.iso" /mnt
sh /mnt/VBoxLinuxAdditions.run
umount /mnt
rm -rf "$HOME_DIR/VBoxGuestAdditions_$VBOX_VERSION.iso"
rm -f "$HOME_DIR/.vbox_version"
