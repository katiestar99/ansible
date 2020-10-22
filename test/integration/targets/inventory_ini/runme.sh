#!/usr/bin/env bash

set -eux

assible-playbook -v -i inventory.ini test_assible_become.yml
