# CYB Development

The `Vagrantfile` in this directory defines a virtual machine for working on
the back-end and front-end code for Cover Your Basics.

## SSH Access

Using `ssh development-www.coveryourbasics.dev` command will access this machine
as the `vagrant` user, which is suitable for inspecting the state of the
provisioned VM.  However, for development, you will want to run the `develop`
script in this directory.  Calling this script with the name of an application
as its first and only argument will SSH in to the VM as the application user,
allowing you to interact with the application and its source code.

## Provisioning

To provision this VM, run the `provision` script in this directory, which is a
thin wrapper around `ansible-playbook` that uses a development playbook.
