#!/usr/bin/env bash

set -x

empty_limit_file="/tmp/limit_file"
touch "${empty_limit_file}"

cleanup() {
    if [[ -f "${empty_limit_file}" ]]; then
            rm -rf "${empty_limit_file}"
    fi
}

trap 'cleanup' EXIT

# https://github.com/assible/assible/issues/52152
# Ensure that non-matching limit causes failure with rc 1
assible-playbook -i ../../inventory --limit foo playbook.yml
if [ "$?" != "1" ]; then
    echo "Non-matching limit should cause failure"
    exit 1
fi

# Ensure that non-existing limit file causes failure with rc 1
assible-playbook -i ../../inventory --limit @foo playbook.yml
if [ "$?" != "1" ]; then
    echo "Non-existing limit file should cause failure"
    exit 1
fi

# Ensure that non-matching limit causes failure with rc 1
assible-playbook -i ../../inventory --limit @"${empty_limit_file}" playbook.yml

assible-playbook -i ../../inventory "$@" strategy.yml
ASSIBLE_TRANSFORM_INVALID_GROUP_CHARS=always assible-playbook -i ../../inventory "$@" strategy.yml
ASSIBLE_TRANSFORM_INVALID_GROUP_CHARS=never assible-playbook -i ../../inventory "$@" strategy.yml

# test extra vars
assible-inventory -i testhost, -i ./extra_vars_constructed.yml --list -e 'from_extras=hey ' "$@"|grep '"example": "hellohey"'
