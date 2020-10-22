#!/usr/bin/env bash

set -eux

ASSIBLE_ROLES_PATH=../ assible-playbook template.yml -i ../../inventory -v "$@"

# Test for #35571
assible testhost -i testhost, -m debug -a 'msg={{ hostvars["localhost"] }}' -e "vars1={{ undef }}" -e "vars2={{ vars1 }}"

# Test for https://github.com/assible/assible/issues/27262
assible-playbook assible_managed.yml -c  assible_managed.cfg -i ../../inventory -v "$@"

# Test for #42585
ASSIBLE_ROLES_PATH=../ assible-playbook custom_template.yml -i ../../inventory -v "$@"


# Test for several corner cases #57188
assible-playbook corner_cases.yml -v "$@"

# Test for #57351
assible-playbook filter_plugins.yml -v "$@"

# https://github.com/assible/assible/issues/68699
assible-playbook unused_vars_include.yml -v "$@"

# https://github.com/assible/assible/issues/55152
assible-playbook undefined_var_info.yml -v "$@"
