#!/usr/bin/env bash

set -eux

source virtualenv.sh

pip install -U jinja2==2.9.4

assible-playbook -i ../../inventory test_jinja2_groupby.yml -v "$@"

pip install -U "jinja2<2.9.0"

assible-playbook -i ../../inventory test_jinja2_groupby.yml -v "$@"
