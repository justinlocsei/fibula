# Fibula

This repository holds code that defines the infrastructure used to run Cover
Your Basics.

## Dependencies

Before working with fibula, you will need to manually install its dependencies.
These are:

1. [Packer v0.8.6](https://releases.hashicorp.com/packer/0.8.6/)
2. [Vagrant v1.8.1](https://releases.hashicorp.com/vagrant/1.8.1/)
3. [VirtualBox v4.3.4](https://www.virtualbox.org/wiki/Download_Old_Builds_4_3)

## Configuration

Before running any code, configure your environment to set the following
variables:

* `CYB_NFS_DIR_CHITON`: The absolute path to the directory for the shared Chiton source
* `CYB_NFS_DIR_HIMATION`: The absolute path to the directory for the shared Himation source
* `CYB_VAGRANT_KEY_PRIVATE`: The absolute path to the private key used to access Vagrant machines
* `CYB_VAGRANT_KEY_PUBLIC`: The absolute path to the public key used to access Vagrant machines
* `CYB_ANSIBLE_VAULT_PASSWORD_FILE`: An optional path to a file containing the password for the Ansible vault

To work with the infrastructure code, run the following from the root of this
repository:

```sh
$ ./scripts/setup
$ source scripts/develop
```

The `setup` script installs all dependencies, and should only need to be run
during initial setup, or when project requirements are updated.  The `develop`
script should be run every time you need to interact with the source.

## Box Management

The VMs used for development are managed by Packer, and their templates can be
found in the `packer` directory.  To build a box and add it to the local Vagrant
box list, run the following:

```sh
$ ./scripts/build_box BOX_NAME
```

Provided the `BOX_NAME` matches the basename of a JSON file in the `packer`
directory, this will build the box and add it to Vagrant under the `fibula`
namespace.
