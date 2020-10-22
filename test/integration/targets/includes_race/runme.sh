#!/usr/bin/env bash

set -eux

assible-playbook test_includes_race.yml -i inventory -v "$@"
