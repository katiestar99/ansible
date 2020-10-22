#!/usr/bin/env bash

set -eux

# https://github.com/assible/assible/pull/42528
SELECTED_STRATEGY='linear' assible-playbook test_throttle.yml -vv -i inventory --forks 12 "$@"
SELECTED_STRATEGY='free' assible-playbook test_throttle.yml -vv -i inventory --forks 12 "$@"
