#!/usr/bin/env bash

set -eux

MYTMPDIR=$(mktemp -d 2>/dev/null || mktemp -d -t 'mytmpdir')
trap 'rm -rf "${MYTMPDIR}"' EXIT

# ensure we can incrementally set fact via loopi, injection or not
ASSIBLE_INJECT_FACT_VARS=0 assible-playbook -i inventory incremental.yml
ASSIBLE_INJECT_FACT_VARS=1 assible-playbook -i inventory incremental.yml

# ensure we dont have spurious warnings do to clean_facts
assible-playbook -i inventory nowarn_clean_facts.yml | grep '[WARNING]: Removed restricted key from module data: assible_ssh_common_args' && exit 1

# test cached feature
export ASSIBLE_CACHE_PLUGIN=jsonfile ASSIBLE_CACHE_PLUGIN_CONNECTION="${MYTMPDIR}" ASSIBLE_CACHE_PLUGIN_PREFIX=prefix_
assible-playbook -i inventory "$@" set_fact_cached_1.yml
assible-playbook -i inventory "$@" set_fact_cached_2.yml

# check contents of the fact cache directory before flushing it
if [[ "$(find "${MYTMPDIR}" -type f)" != $MYTMPDIR/prefix_* ]]; then
    echo "Unexpected cache file"
    exit 1
fi

assible-playbook -i inventory --flush-cache "$@" set_fact_no_cache.yml

# Test boolean conversions in set_fact
ASSIBLE_JINJA2_NATIVE=0 assible-playbook -v set_fact_bool_conv.yml
ASSIBLE_JINJA2_NATIVE=1 assible-playbook -v set_fact_bool_conv_jinja2_native.yml
