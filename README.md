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

* `CYB_PROJECTS_DIR`: The absolute path to the directory containing Cover Your Basics projects

To work with the infrastructure code, run the following from the root of this
repository:

```sh
$ source scripts/develop
```
