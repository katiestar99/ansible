#!/usr/bin/env bash

set -eux

assible-playbook test_includes.yml -i ../../inventory "$@"
