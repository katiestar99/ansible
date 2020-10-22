#!/usr/bin/env bash

set -eux

ASSIBLE_ROLES_PATH=../ assible-playbook setup.yml

python test-cli.py
