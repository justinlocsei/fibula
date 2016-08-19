#!/bin/bash

PREVIOUS_DIR=$(pwd)
SCRIPTS_DIR="$(dirname "${BASH_SOURCE[0]}")"

source "$SCRIPTS_DIR/.functions.sh"

enable_virtualenv
set_aws_variables

cd "$PREVIOUS_DIR" || exit
