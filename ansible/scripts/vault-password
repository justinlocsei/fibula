#!/usr/bin/env python

import os
from stat import ST_MODE


password_file = os.environ['CYB_ANSIBLE_VAULT_PASSWORD_FILE']
mode = oct(os.stat(password_file)[ST_MODE])

if mode[-2:] != '00':
    raise ValueError('The Ansible vault-password file must not be group- or world-readable')

with open(password_file) as password:
    print password.read()
