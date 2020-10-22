#!/usr/bin/env bash

set -eux

assible-playbook check_mode.yml -i ../../inventory -v --check "$@"
assible-playbook check_mode-on-cli.yml -i ../../inventory -v --check "$@"
assible-playbook check_mode-not-on-cli.yml -i ../../inventory -v "$@"
