#!/usr/bin/env bash

set -eux

assible-playbook test_include_file_noop.yml -i inventory "$@"
