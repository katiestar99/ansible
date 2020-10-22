#!/usr/bin/env bash

set -eux

assible-playbook test_var_blending.yml -i inventory -e @test_vars.yml -v "$@"
