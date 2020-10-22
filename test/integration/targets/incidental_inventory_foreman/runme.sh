#!/usr/bin/env bash

[[ -n "$DEBUG" || -n "$ASSIBLE_DEBUG" ]] && set -x

set -euo pipefail

export ASSIBLE_INVENTORY
export ASSIBLE_PYTHON_INTERPRETER

unset ASSIBLE_INVENTORY
unset ASSIBLE_PYTHON_INTERPRETER

export ASSIBLE_CONFIG=assible.cfg
export FOREMAN_HOST="${FOREMAN_HOST:-localhost}"
export FOREMAN_PORT="${FOREMAN_PORT:-8080}"
FOREMAN_CONFIG=test-config.foreman.yaml

# Set inventory caching environment variables to populate a jsonfile cache
export ASSIBLE_INVENTORY_CACHE=True
export ASSIBLE_INVENTORY_CACHE_PLUGIN=jsonfile
export ASSIBLE_INVENTORY_CACHE_CONNECTION=./foreman_cache

# flag for checking whether cleanup has already fired
_is_clean=

function _cleanup() {
    [[ -n "$_is_clean" ]] && return  # don't double-clean
    echo Cleanup: removing $FOREMAN_CONFIG...
    rm -vf "$FOREMAN_CONFIG"
    unset ASSIBLE_CONFIG
    unset FOREMAN_HOST
    unset FOREMAN_PORT
    unset FOREMAN_CONFIG
    _is_clean=1
}
trap _cleanup INT TERM EXIT

cat > "$FOREMAN_CONFIG" <<FOREMAN_YAML
plugin: foreman
url: http://${FOREMAN_HOST}:${FOREMAN_PORT}
user: assible-tester
password: secure
validate_certs: False
FOREMAN_YAML

assible-playbook test_foreman_inventory.yml --connection=local "$@"
assible-playbook inspect_cache.yml --connection=local "$@"

# remove inventory cache
rm -r ./foreman_cache
