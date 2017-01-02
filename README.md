# Fibula

This repository holds code that defines the infrastructure used to run Cover
Your Basics.

## Dependencies

Before working with fibula, you will need to manually install its dependencies:

1. [Packer](https://www.packer.io/downloads.html)
2. [Vagrant](https://www.vagrantup.com/downloads.html)
3. [VirtualBox](https://www.virtualbox.org/wiki/Downloads)

## Configuration

Before running any code, ensure that values for the following environment
variables are automatically set in your shell:

* `CYB_ANSIBLE_VAULT_PASSWORD_FILE`: An optional path to a file containing the password for the Ansible vault
* `CYB_AWS_ACCESS_KEY_ID`: The access key ID for the AWS management account
* `CYB_AWS_SECRET_ACCESS_KEY`: The secret access key for the AWS management account
* `CYB_DO_API_TOKEN`: The Digital Ocean API token
* `CYB_NFS_DIR_CHITON`: The absolute path to the directory for the shared Chiton source
* `CYB_NFS_DIR_HIMATION`: The absolute path to the directory for the shared Himation source
* `CYB_VAGRANT_KEY_PRIVATE`: The absolute path to the private key used to access Vagrant machines

To work with the infrastructure code, run the following commands:

```bash
# Install dependencies
$ ./scripts/env/setup.sh

# Activate the development environment
$ source scripts/env/develop.sh
```

## Box Creation

```bash
# Build the Ubuntu 14.04 Packer box defined in the packer/ directory
$ ./scripts/vms/build-box.py ubuntu-14.04

# Use the box in a Vagrantfile
$ cat 'config.vm.box = "fibula/ubuntu-14.04"' >> Vagrantfile
```

## Virtual Machines

Each directory underneath the `vms` directory defines a VM used for Cover Your
Basics.  Each machine's IP address is dynamically added to the `/etc/hosts` file
on the host as a subdomain of `coveryourbasics.dev`, which allows each VM to be
treated as a normal, external host, and be largely managed outside of Vagrant.

### SSH Access

Each machine can be accessed using `ssh SUBDOMAIN.coveryourbasics.dev`, which
bypasses Vagrant and relies on the partially managed `/etc/hosts` file to
provide the correct SSH parameters.

## Servers

All management of servers is done using the `fib` command, which is made
available when running the setup script. It has many subcommands, all of which
can be listed by running `fib --help`.

### Infrastructure

To automatically build out the remote resources used to serve Cover Your Basics,
run the following commands:

```bash
# Create resources
$ fib build

# Update resources
$ fib sync

# Remove unused resources
$ fib prune
```

### Deploying

Application code can be deployed by running the following command:

```bash
$ fib deploy to <environment>
```

This is a thin wrapper around `ansible-playbook` that deploys to all machines in
the `<environment>` group. By default, the inventory file whose name matches the
environment is used, but this can be changed using the `--inventory` option. For
example, to do a test deploy to all staging machines in the development
inventory, you could run the following command:

```bash
$ fib deploy to staging --inventory=development
```
