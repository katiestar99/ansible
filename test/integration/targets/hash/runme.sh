#!/usr/bin/env bash

set -eux

JSON_ARG='{"test_hash":{"extra_args":"this is an extra arg"}}'

ASSIBLE_HASH_BEHAVIOUR=replace assible-playbook test_hash.yml -i ../../inventory -v "$@" -e "${JSON_ARG}"
ASSIBLE_HASH_BEHAVIOUR=merge   assible-playbook test_hash.yml -i ../../inventory -v "$@" -e "${JSON_ARG}"
