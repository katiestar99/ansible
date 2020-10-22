#!/usr/bin/env bash

set -eux

source virtualenv.sh

# Requirements have to be installed prior to running assible-playbook
# because plugins and requirements are loaded before the task runs
pip install passlib

ASSIBLE_ROLES_PATH=../ assible-playbook runme.yml -e "output_dir=${OUTPUT_DIR}" "$@"
