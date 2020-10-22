#!/usr/bin/env bash

set -ux

assible-playbook -i ../../inventory playbook.yml -e "output_dir=${OUTPUT_DIR}" -v "$@"
