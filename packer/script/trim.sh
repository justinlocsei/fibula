#!/bin/bash -eux

# Remove system languages
apt-get -y purge ruby ri doc
apt-get -y purge python-dbus libnl1 python-smartpm python-twisted-core libiw30 python-twisted-bin libdbus-glib-1-2 python-pexpect python-pycurl python-serial python-gobject python-pam python-openssl libffi5

# Remove X11
apt-get -y purge libx11-data xauth libxmuu1 libxcb1 libx11-6 libxext6

# Remove unnecessary packages
apt-get -y purge ppp pppconfig pppoeconf
apt-get -y purge popularity-contest installation-report landscape-common wireless-tools wpasupplicant ubuntu-serverguide

# Clean up the apt cache
apt-get -y autoremove --purge
apt-get -y autoclean
apt-get -y clean

# Remove documentation
rm -rf /usr/share/man/*
rm -rf /usr/share/doc/*
