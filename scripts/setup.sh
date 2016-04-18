#!/bin/bash

SCRIPTS_DIR="$(dirname "$BASH_SOURCE")"

source "$SCRIPTS_DIR/.functions"

create_virtualenv
install_python_requirements
configure_infrastructure_scripts
install_vagrant_plugins
install_ansible
update_ssh_config
