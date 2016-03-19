# Development VMs

The `Vagrantfile` in this directory defines a cluster of virtual machines for
the back-end and front-end servers used for Cover Your Basics.

## SSH Access

Using the `ssh development-SUBDOMAIN.coveryourbasics.com` command will access
each machine as the `vagrant` user, which is suitable for inspecting the state
of the provisioned VM.  However, for development, you will want to run the
`develop` script in this directory.  Calling this script with the VM name as its
first and only argument will SSH in to the VM as the application user for the
named VM, allowing you to interact with the application and its source code.

## Provisioning

To provision these VMs, use the `configure/development_VM.yml` Ansible
playbooks, which only target the VM named in `VM`.  Alternatively, you can use
the `configure/development.yml` playbook to provision all machines in this
cluster.
