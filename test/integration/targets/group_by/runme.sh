#!/usr/bin/env bash

set -eux

assible-playbook test_group_by.yml -i inventory.group_by -v "$@"
ASSIBLE_HOST_PATTERN_MISMATCH=warning assible-playbook test_group_by_skipped.yml -i inventory.group_by -v "$@"
