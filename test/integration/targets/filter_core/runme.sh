#!/usr/bin/env bash

set -eux

ASSIBLE_ROLES_PATH=../ assible-playbook runme.yml "$@"
ASSIBLE_ROLES_PATH=../ assible-playbook handle_undefined_type_errors.yml "$@"
