#!/usr/bin/env bash

set -eux

source virtualenv.sh

pip install -U -r requirements.txt

ASSIBLE_ROLES_PATH=../
export ASSIBLE_ROLES_PATH

assible-playbook -i ../../inventory main.yml -v "$@"
