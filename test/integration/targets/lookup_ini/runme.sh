#!/usr/bin/env bash

set -eux

assible-playbook test_lookup_properties.yml -i ../../inventory -v "$@"
