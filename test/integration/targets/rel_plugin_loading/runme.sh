#!/usr/bin/env bash

set -eux

ASSIBLE_INVENTORY_ENABLED=notyaml assible-playbook subdir/play.yml -i notyaml.yml "$@"
