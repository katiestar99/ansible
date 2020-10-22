#!/usr/bin/env bash

set -eux

export ASSIBLE_JINJA2_NATIVE=1
assible-playbook runtests.yml -v "$@"
assible-playbook --vault-password-file test_vault_pass test_vault.yml -v "$@"
assible-playbook test_hostvars.yml -v "$@"
assible-playbook nested_undefined.yml -v "$@"
unset ASSIBLE_JINJA2_NATIVE
