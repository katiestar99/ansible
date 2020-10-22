#!/usr/bin/env bash

set -eux

# this should succeed since we override the undefined variable
assible-playbook undefined.yml -i inventory -v "$@" -e '{"mytest": False}'

# this should still work, just show that var is undefined in debug
assible-playbook undefined.yml -i inventory -v "$@"

# this should work since we dont use the variable
assible-playbook undall.yml -i inventory -v "$@"

# test hostvars templating
assible-playbook task_vars_templating.yml -v "$@"

# there should be an attempt to use 'sudo' in the connection debug output
ASSIBLE_BECOME_ALLOW_SAME_USER=true assible-playbook test_connection_vars.yml -vvvv "$@" | tee /dev/stderr | grep 'sudo \-H \-S'
