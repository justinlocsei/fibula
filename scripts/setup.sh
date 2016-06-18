#!/bin/bash

SCRIPTS_DIR="$(dirname "${BASH_SOURCE[0]}")"

source "$SCRIPTS_DIR/.functions.sh"

create_virtualenv
install_python_requirements
configure_infrastructure_scripts
install_vagrant_plugins
update_ssh_config
