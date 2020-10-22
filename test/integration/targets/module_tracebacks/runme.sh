#!/usr/bin/env bash

set -eux

assible-playbook traceback.yml -i inventory "$@"
