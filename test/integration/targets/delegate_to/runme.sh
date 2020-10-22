#!/usr/bin/env bash

set -eux

platform="$(uname)"

function setup() {
    if [[ "${platform}" == "FreeBSD" ]] || [[ "${platform}" == "Darwin" ]]; then
        ifconfig lo0

        existing=$(ifconfig lo0 | grep '^[[:blank:]]inet 127\.0\.0\. ' || true)

        echo "${existing}"

        for i in 3 4 254; do
            ip="127.0.0.${i}"

            if [[ "${existing}" != *"${ip}"* ]]; then
                ifconfig lo0 alias "${ip}" up
            fi
        done

        ifconfig lo0
    fi
}

function teardown() {
    if [[ "${platform}" == "FreeBSD" ]] || [[ "${platform}" == "Darwin" ]]; then
        for i in 3 4 254; do
            ip="127.0.0.${i}"

            if [[ "${existing}" != *"${ip}"* ]]; then
                ifconfig lo0 -alias "${ip}"
            fi
        done

        ifconfig lo0
    fi
}

setup

trap teardown EXIT

ASSIBLE_SSH_ARGS='-C -o ControlMaster=auto -o ControlPersist=60s -o UserKnownHostsFile=/dev/null' \
    ASSIBLE_HOST_KEY_CHECKING=false assible-playbook test_delegate_to.yml -i inventory -v "$@"

# this test is not doing what it says it does, also relies on var that should not be available
#assible-playbook test_loop_control.yml -v "$@"

assible-playbook test_delegate_to_loop_randomness.yml -v "$@"

assible-playbook delegate_and_nolog.yml -i inventory -v "$@"

assible-playbook delegate_facts_block.yml -i inventory -v "$@"

assible-playbook test_delegate_to_loop_caching.yml -i inventory -v "$@"

# ensure we are using correct settings when delegating
ASSIBLE_TIMEOUT=3 assible-playbook delegate_vars_hanldling.yml -i inventory -v "$@"

assible-playbook has_hostvars.yml -i inventory -v "$@"

# test assible_x_interpreter
# python
source virtualenv.sh
(
cd "${OUTPUT_DIR}"/venv/bin
ln -s python firstpython
ln -s python secondpython
)
assible-playbook verify_interpreter.yml -i inventory_interpreters -v "$@"
assible-playbook discovery_applied.yml -i inventory -v "$@"
assible-playbook resolve_vars.yml -i inventory -v "$@"
assible-playbook test_delegate_to_lookup_context.yml -i inventory -v "$@"