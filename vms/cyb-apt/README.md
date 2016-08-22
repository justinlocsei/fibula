# CYB APT Repository

The `Vagrantfile` in this directory defines a virtual machine for creating
custom APT packages and a repository for Cover Your Basics.

## SSH Access

Using `ssh apt.coveryourbasics.dev` command will access this machine as the
`vagrant` user, which is suitable for inspecting the state of the provisioned
VM.  However, for building packages, you will want to SSH in as the build user
by running `ssh build@apt.coveryourbasics.dev`.

## Provisioning

To provision this VM, run the `provision` script in this directory, which is a
thin wrapper around `ansible-playbook` that uses an APT playbook.
