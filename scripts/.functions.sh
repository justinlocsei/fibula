#!/bin/bash

ROOT_DIR="$(cd "$(dirname "$BASH_SOURCE")/.." && pwd)"

VENDOR_DIR="vendor"
VENV_DIR="environments"
VENV_NAME="fibula"

# Create the Python virtual environment if it does not exist
function create_virtualenv() {
  mkdir -p "$ROOT_DIR/$VENV_DIR"
  cd "$ROOT_DIR/$VENV_DIR" || exit

  if [[ ! -d $VENV_NAME  ]]; then
    virtualenv $VENV_NAME
  fi
}

# Enable the Python virtual environment
function enable_virtualenv() {
  cd "$ROOT_DIR/$VENV_DIR" || exit
  VIRTUAL_ENV_DISABLE_PROMPT="true" source $VENV_NAME/bin/activate
}

# Install the project's Python requirements via pip
function install_python_requirements() {
  cd "$ROOT_DIR" || exit
  "$VENV_DIR/$VENV_NAME/bin/pip" install --requirement requirements.txt
}

# Allow the infrastructure scripts to run
function configure_infrastructure_scripts() {
  pip install --editable "$ROOT_DIR/infrastructure"
}

# Install all required Vagrant plugins
function install_vagrant_plugins() {
  local plugin

  for plugin in "vagrant-nfs_guest" "vagrant-hostsupdater"; do
    if ! vagrant plugin list | grep "$plugin" --quiet; then
      vagrant plugin install "$plugin"
    fi
  done
}

# Set AWS environment variables
function set_aws_variables() {
  if [[ -z "$CYB_AWS_ACCESS_KEY_ID" ]]; then
    echo "You must set an AWS access key ID via the CYB_AWS_ACCESS_KEY_ID environment variable!"
  else
    export AWS_ACCESS_KEY_ID="$CYB_AWS_ACCESS_KEY_ID"
  fi

  if [[ -z "$CYB_AWS_SECRET_ACCESS_KEY" ]]; then
    echo "You must set an AWS secret access key via CYB_AWS_SECRET_ACCESS_KEY environment variable!"
  else
    export AWS_SECRET_ACCESS_KEY="$CYB_AWS_SECRET_ACCESS_KEY"
  fi
}

# Update the SSH config file to relax settings for the development machines
function update_ssh_config() {
  local begin_flag
  local end_flag
  local line
  local valid_config
  local ssh_config
  local ssh_config_temp

  ssh_config="$HOME/.ssh/config"
  ssh_config_temp="/tmp/ssh-config-fibula"
  valid_config=1

  begin_flag="# Begin fibula customization"
  end_flag="# End fibula customization"

  IFS=""
  while read -r line; do
    if [[ "$line" == "$begin_flag" ]]; then valid_config=0; fi
    if [[ $valid_config -eq 1 ]]; then echo "$line" >> "$ssh_config_temp"; fi
    if [[ "$line" == "$end_flag" ]]; then valid_config=1; fi
  done < "$ssh_config"

  mv "$ssh_config_temp" "$ssh_config"

  cat >> "$ssh_config" <<CONFIG
$begin_flag

Host *.coveryourbasics.dev
  ForwardAgent yes
  IdentityFile "$CYB_VAGRANT_KEY_PRIVATE"
  LogLevel ERROR
  StrictHostKeyChecking no
  User vagrant
  UserKnownHostsFile=/dev/null

$end_flag
CONFIG
}
