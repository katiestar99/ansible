#!/usr/bin/env bash

set -eux

assible-playbook bad_parsing.yml  -i ../../inventory -vvv "$@" --tags prepare,common,scenario5
assible-playbook good_parsing.yml -i ../../inventory -v "$@"
