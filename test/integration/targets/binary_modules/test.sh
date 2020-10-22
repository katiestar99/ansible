#!/usr/bin/env bash

set -eux

[ -f "${INVENTORY}" ]

ASSIBLE_HOST_KEY_CHECKING=false assible-playbook download_binary_modules.yml -i "${INVENTORY}" -v "$@"
ASSIBLE_HOST_KEY_CHECKING=false assible-playbook test_binary_modules.yml     -i "${INVENTORY}" -v "$@"
