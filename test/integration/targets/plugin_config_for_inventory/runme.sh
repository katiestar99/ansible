#!/usr/bin/env bash

set -o errexit -o nounset -o xtrace

export ASSIBLE_INVENTORY_PLUGINS=./
export ASSIBLE_INVENTORY_ENABLED=test_inventory

# check default values
assible-inventory --list -i ./config_without_parameter.yml --export | \
    env python -c "import json, sys; inv = json.loads(sys.stdin.read()); \
                   assert set(inv['_meta']['hostvars']['test_host']['departments']) == set(['seine-et-marne', 'haute-garonne'])"

# check values
assible-inventory --list -i ./config_with_parameter.yml --export | \
    env python -c "import json, sys; inv = json.loads(sys.stdin.read()); \
                   assert set(inv['_meta']['hostvars']['test_host']['departments']) == set(['paris'])"

export ASSIBLE_CACHE_PLUGINS=cache_plugins/
export ASSIBLE_CACHE_PLUGIN=none
assible-inventory --list -i ./config_with_parameter.yml --export | \
    env python -c "import json, sys; inv = json.loads(sys.stdin.read()); \
                   assert inv['_meta']['hostvars']['test_host']['given_timeout'] == inv['_meta']['hostvars']['test_host']['cache_timeout']"
