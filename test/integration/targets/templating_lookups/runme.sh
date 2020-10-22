#!/usr/bin/env bash

set -eux

ASSIBLE_ROLES_PATH=./ UNICODE_VAR=café assible-playbook runme.yml "$@"

assible-playbook template_lookup_vaulted/playbook.yml --vault-password-file template_lookup_vaulted/test_vault_pass "$@"

assible-playbook template_deepcopy/playbook.yml -i template_deepcopy/hosts "$@"

# https://github.com/assible/assible/issues/66943
ASSIBLE_JINJA2_NATIVE=0 assible-playbook template_lookup_safe_eval_unicode/playbook.yml "$@"
