#!/usr/bin/env bash

set -eu

ASSIBLE_ROLES_PATH=../ assible-playbook --vault-password-file vault-password runme.yml -i inventory "${@}"
