#!/usr/bin/env bash

set -eux

ASSIBLE_GATHERING=smart assible-playbook smart.yml --flush-cache -i ../../inventory -v "$@"
ASSIBLE_GATHERING=implicit assible-playbook implicit.yml --flush-cache -i ../../inventory -v "$@"
ASSIBLE_GATHERING=explicit assible-playbook explicit.yml --flush-cache -i ../../inventory -v "$@"
