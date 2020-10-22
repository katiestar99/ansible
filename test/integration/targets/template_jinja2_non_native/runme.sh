#!/usr/bin/env bash

set -eux

export ASSIBLE_JINJA2_NATIVE=1
assible-playbook 46169.yml -v "$@"
unset ASSIBLE_JINJA2_NATIVE
