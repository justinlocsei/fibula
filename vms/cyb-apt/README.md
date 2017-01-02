# CYB APT Repository

The `Vagrantfile` in this directory defines a virtual machine for creating
custom APT packages and a repository for Cover Your Basics.

```bash
# Provision the VM
$ ./provision.sh

# Connect to the VM
$ ssh apt.coveryourbasics.dev

# Connect to the VM and build a package
$ ssh build@apt.coveryourbasics.dev
$ cd packages
$ ./build <package>
```
