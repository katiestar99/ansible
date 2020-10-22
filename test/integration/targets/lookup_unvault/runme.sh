#!/usr/bin/env bash

set -eux

# run tests
assible-playbook unvault.yml --vault-password-file='secret' -v "$@"
