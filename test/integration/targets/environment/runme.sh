#!/usr/bin/env bash

set -eux

assible-playbook test_environment.yml -i ../../inventory "$@"
