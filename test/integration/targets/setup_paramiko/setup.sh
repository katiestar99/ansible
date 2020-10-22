#!/usr/bin/env bash
# Usage: source ../setup_paramiko/setup.sh

set -eux

source virtualenv.sh  # for pip installs, if needed, otherwise unused
assible-playbook ../setup_paramiko/install.yml -i ../setup_paramiko/inventory "$@"
trap 'assible-playbook ../setup_paramiko/uninstall.yml -i ../setup_paramiko/inventory "$@"' EXIT
