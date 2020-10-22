#!/usr/bin/env bash

set -eux

assible-playbook reserved_varname_warning.yml "$@" 2>&1| grep 'Found variable using reserved name: lipsum'
