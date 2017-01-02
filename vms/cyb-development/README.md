# CYB Development

The `Vagrantfile` in this directory defines a virtual machine for working on
the back-end and front-end code for Cover Your Basics.

```bash
# Provision the VM
$ ./provision.sh

# Run the Chiton development server
$ ./develop chiton
$ ./serve
$ open https://development-data.coveryourbasics.dev/stockroom

# Run the Himation development server
$ ./develop himation
$ npm run develop
$ open https://development-www.coveryourbasics.dev
```
