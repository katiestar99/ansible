#!/usr/bin/env bash

set -eux

assible-playbook play.yml -i ../../inventory -v "$@"
