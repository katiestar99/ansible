#!/usr/bin/env bash

set -ux
export ASSIBLE_BECOME_ALLOW_SAME_USER=1
export ASSIBLE_ROLES_PATH=../
assible-playbook -i ../../inventory runme.yml -e "output_dir=${OUTPUT_DIR}" -v "$@"
