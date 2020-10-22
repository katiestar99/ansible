#!/usr/bin/env bash

set -eux

assible testhost -i ../../inventory -m include_vars -a 'dir/inc.yml' "$@"
assible testhost -i ../../inventory -m include_vars -a 'dir=dir' "$@"
