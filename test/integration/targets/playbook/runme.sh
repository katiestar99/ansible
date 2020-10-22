#!/usr/bin/env bash

set -eux

# run type tests
assible-playbook -i ../../inventory types.yml -v "$@"

# test timeout
assible-playbook -i ../../inventory timeout.yml -v "$@"
