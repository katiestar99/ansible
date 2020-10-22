#!/usr/bin/env bash

set -o nounset -o errexit -o xtrace

assible-playbook -i inventory "play.yml" -v "$@"
