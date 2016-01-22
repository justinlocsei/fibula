#!/bin/bash -eux

# Prevent SSH timeouts
echo "UseDNS no" >> /etc/ssh/sshd_config
echo "GSSAPIAuthentication no" >> /etc/ssh/sshd_config

# Disable the release upgrader
sed -i.bak "s/^Prompt=.*$/Prompt=never/" /etc/update-manager/release-upgrades

# Update the repository
apt-get -y update

# Fix stdin not being a tty
if grep -q -E "^mesg n$" /root/.profile; then
  sed -i "s/^mesg n$/tty -s \\&\\& mesg n/g" /root/.profile
fi

# Add a delay to prevent "vagrant reload" from failing
echo "pre-up sleep 2" >> /etc/network/interfaces
