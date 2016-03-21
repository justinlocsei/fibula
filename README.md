# Fibula

This repository holds code that defines the infrastructure used to run Cover
Your Basics.

## Dependencies

Before working with fibula, you will need to manually install its dependencies.
These are:

1. [Packer](https://www.packer.io/downloads.html)
2. [Vagrant](https://www.vagrantup.com/downloads.html)
3. [VirtualBox](https://www.virtualbox.org/wiki/Downloads)

## Configuration

Before running any code, configure your environment to set the following
variables:

* `CYB_ANSIBLE_VAULT_PASSWORD_FILE`: An optional path to a file containing the password for the Ansible vault
* `CYB_AWS_ACCESS_KEY_ID`: The access key ID for the AWS management account
* `CYB_AWS_SECRET_ACCESS_KEY`: The secret access key for the AWS management account
* `CYB_NFS_DIR_CHITON`: The absolute path to the directory for the shared Chiton source
* `CYB_NFS_DIR_HIMATION`: The absolute path to the directory for the shared Himation source
* `CYB_VAGRANT_KEY_PRIVATE`: The absolute path to the private key used to access Vagrant machines
* `CYB_VAGRANT_KEY_PUBLIC`: The absolute path to the public key used to access Vagrant machines

To work with the infrastructure code, run the following from the root of this
repository:

```sh
$ ./scripts/setup
$ source scripts/develop
```

The `setup` script installs all dependencies, and should only need to be run
during initial setup, or when project requirements are updated.  The `develop`
script should be run every time you need to interact with the source.

## Box Creation

The VMs used for development are managed by Packer, and their templates can be
found in the `packer` directory.  To build a box and add it to the local Vagrant
box list, run the following:

```sh
$ ./scripts/build_box BOX_NAME
```

Provided that `BOX_NAME` matches the basename of a JSON file in the `packer`
directory, this will build the box and add it to Vagrant under the `fibula`
namespace.

## Virtual Machines

Each directory underneath the `vms` directory defines a cluster of VMs used for
Cover Your Basics.  Each machine's IP address is dynamically added to the
`/etc/hosts` file on the host as a subdomain of `coveryourbasics.com`, which
allows each VM to be treated as a normal, external host, and be largely managed
outside of Vagrant.

### SSH Access

Each machine can be accessed using
`ssh development-SUBDOMAIN.coveryourbasics.com`, which bypasses Vagrant and
relies on the partially managed `/etc/hosts` file to provide the correct SSH
parameters.

### Provisioning

To reduce the difference between development and production, each VM is directly
provisioned using Ansible, and lacks a provisioner configuration in Vagrant.  To
provision a machine, run the following commands from the root directory:

```bash
$ source scripts/develop
$ cd ansible
$ ansible-playbook playbooks/configure/PLAYBOOOK.yml
```

This enables the development version of Ansible and then uses the
`ansible-playbook` command to apply the playbook provided in `PLAYBOOK` to the
machine in question.
