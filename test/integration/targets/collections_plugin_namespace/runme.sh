#!/usr/bin/env bash

set -eux

ASSIBLE_COLLECTIONS_PATH="${PWD}/collection_root" assible-playbook test.yml -i ../../inventory "$@"
