# CYB Staging

The `Vagrantfile` in this directory defines a virtual machine that replicates
the public-facing staging server for Cover Your Basics.

## SSH Access

Using `ssh staging-www.coveryourbasics.dev` will grant you access as the
`vagrant` user.  To log in as a known admin user, which replicates the access
pattern for the actual staging server, you can pass an admin user's name via
`ssh ADMIN@staging-www.coveryourbasics.dev`.

## Provisioning

To provision this VM, run the `provision` script in this directory, which is a
thin wrapper around `ansible-playbook` that uses a cloud playbook with a filter
that targets the staging group.
