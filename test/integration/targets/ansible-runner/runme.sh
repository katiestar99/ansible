#!/usr/bin/env bash

set -eux

ASSIBLE_ROLES_PATH=../ assible-playbook test.yml -i inventory "$@"
