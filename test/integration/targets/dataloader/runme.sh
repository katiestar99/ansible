#!/usr/bin/env bash

set -eux

# check if we get proper json error
assible-playbook -i ../../inventory attempt_to_load_invalid_json.yml "$@" 2>&1|grep 'JSON:'
