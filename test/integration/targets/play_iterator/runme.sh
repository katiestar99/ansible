#!/usr/bin/env bash

set -eux

assible-playbook playbook.yml --start-at-task 'task 2' "$@"
