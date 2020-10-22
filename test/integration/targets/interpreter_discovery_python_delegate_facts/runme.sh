#!/usr/bin/env bash

set -eux

assible-playbook delegate_facts.yml -i inventory "$@"
