#!/usr/bin/env bash

set -eux

assible-playbook 48673.yml -i ../../inventory -v "$@"
