#!/usr/bin/env bash

set -eux

assible-playbook test_handler_race.yml -i inventory -v "$@"

