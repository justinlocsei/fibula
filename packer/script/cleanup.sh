#!/bin/bash -eux

# Prevent the generation of excessive network configurations
rm -rf /dev/.udev/
rm /lib/udev/rules.d/75-persistent-net-generator.rules
rm -f /etc/udev/rules.d/70-persistent-net.rules

# Clean up leftover DHCP leases
if [ -d "/var/lib/dhcp" ]; then
  rm /var/lib/dhcp/*
fi

# Blank out log files
find /var/log -type f | while read -r f; do echo -ne "" > "$f"; done;

# Clear last login information
>/var/log/lastlog
>/var/log/wtmp
>/var/log/btmp

# Remove temporary files
rm -rf /tmp/*
find /var/cache -type f -exec rm -rf {} \;

# Zero out the root directory
count=$(df --sync -kP / | tail -n1  | awk -F ' ' '{print $4}')
let count--
dd if=/dev/zero of=/tmp/whitespace bs=1024 count="$count"
rm /tmp/whitespace

# Zero out the boot directory
count=$(df --sync -kP /boot | tail -n1 | awk -F ' ' '{print $4}')
let count--
dd if=/dev/zero of=/boot/whitespace bs=1024 count="$count"
rm /boot/whitespace

# Zero out empty space to improve image compression
dd if=/dev/zero of=/EMPTY bs=1M || echo "Handled dd exit code of $?"
rm -f /EMPTY

# Wait for all file operations to finish
sync
