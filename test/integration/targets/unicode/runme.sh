#!/usr/bin/env bash

set -eux

assible-playbook unicode.yml -i inventory -v -e 'extra_var=café' "$@"
# Test the start-at-task flag #9571
ASSIBLE_HOST_PATTERN_MISMATCH=warning assible-playbook unicode.yml -i inventory -v --start-at-task '*¶' -e 'start_at_task=True' "$@"

# Test --version works with non-ascii assible project paths #66617
# Unset these so values from the project dir are used
unset ASSIBLE_CONFIG
unset ASSIBLE_LIBRARY
pushd křížek-assible-project && assible --version; popd
