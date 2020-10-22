#!/usr/bin/env bash

set -ux

assible-playbook -i this,path,has,commas/hosts playbook.yml -v "$@"
