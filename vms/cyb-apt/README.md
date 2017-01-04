# CYB APT Repository

The `Vagrantfile` in this directory defines a virtual machine for creating
custom APT packages and a repository for Cover Your Basics.

```bash
# Provision the VM
$ ./provision

# Connect to the VM
$ ssh apt.coveryourbasics.dev

# Connect to the VM, build a package, and upload it to the repo
$ ssh build@apt.coveryourbasics.dev
$ cd packages
$ ./build-package <package>
$ ./create-repo --sync
```
