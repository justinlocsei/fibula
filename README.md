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
* `CYB_DO_API_TOKEN`: The Digital Ocean API token
* `CYB_NFS_DIR_CHITON`: The absolute path to the directory for the shared Chiton source
* `CYB_NFS_DIR_HIMATION`: The absolute path to the directory for the shared Himation source
* `CYB_VAGRANT_KEY_PRIVATE`: The absolute path to the private key used to access Vagrant machines

To work with the infrastructure code, run the following from the root of this
repository:

```sh
$ ./scripts/env/setup.sh
$ source scripts/env/develop.sh
```

The `setup` script installs all dependencies, and should only need to be run
during initial setup, or when project requirements are updated.  The `develop`
script should be run every time you need to interact with the source.

## Box Creation

The VMs used for development are managed by Packer, and their templates can be
found in the `packer` directory.  To build a box and add it to the local Vagrant
box list, run the following:

```sh
$ ./scripts/vms/build-box.py BOX_NAME
```

Provided that `BOX_NAME` matches the basename of a JSON file in the `packer`
directory, this will build the box and add it to Vagrant under the `fibula`
namespace.

## Virtual Machines

Each directory underneath the `vms` directory defines a cluster of VMs used for
Cover Your Basics.  Each machine's IP address is dynamically added to the
`/etc/hosts` file on the host as a subdomain of `coveryourbasics.dev`, which
allows each VM to be treated as a normal, external host, and be largely managed
outside of Vagrant.

### SSH Access

Each machine can be accessed using `ssh SUBDOMAIN.coveryourbasics.dev`, which
bypasses Vagrant and relies on the partially managed `/etc/hosts` file to
provide the correct SSH parameters.

### Provisioning

To reduce the difference between development and production, each VM is directly
provisioned using Ansible, and lacks a provisioner configuration in Vagrant.  To
provision a machine, run the following commands from the root directory:

```bash
$ source scripts/env/develop.sh
$ cd ansible
$ ansible-playbook playbooks/PLAYBOOOK.yml
```

This enables the development version of Ansible and then uses the
`ansible-playbook` command to apply the playbook provided in `PLAYBOOK` to the
machine in question.

## Servers

All management of servers is done using the `fib` command, which is made
available when running the `scripts/env/setup.sh` script, and whose source code
is located in the `infrastructure` directory of this repo.  It has many
subcommands, all of which can be listed by running `fib --help`.

### Infrastructure

To automatically build out the remote resources used to serve Cover Your Basics,
run the following commands:

```bash
$ fib build
$ fib sync
$ fib prune
```

This will create any missing resources, correct any drift between the current
and desired state of resources, and remove any unused resources.

### Deploying

Application code can be deployed by running the following command:

```bash
$ fib deploy to <ENVIRONMENT>
```

This is a thin wrapper around `ansible-playbook` that deploys to all machines in
the `<ENVIRONMENT>` group. By default, the inventory file whose name matches the
environment is used, but this can be changed using the `--inventory` option. For
example, to do a test deploy to all staging machines in the development
inventory, you could run the following command:

```bash
$ fib deploy to staging --inventory=development
```
