#!/usr/bin/env bash

set -eux

assible-playbook main.yml -i inventory "$@"
