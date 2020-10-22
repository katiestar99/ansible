#!/usr/bin/env bash

set -eux

#ASSIBLE_CACHE_PLUGINS=cache_plugins/ ASSIBLE_CACHE_PLUGIN=none assible-playbook test_gathering_facts.yml -i inventory -v "$@"
assible-playbook test_gathering_facts.yml -i inventory -e output_dir="$OUTPUT_DIR" -v "$@"
#ASSIBLE_CACHE_PLUGIN=base assible-playbook test_gathering_facts.yml -i inventory -v "$@"

ASSIBLE_GATHERING=smart assible-playbook test_run_once.yml -i inventory -v "$@"

# ensure clean_facts is working properly
assible-playbook test_prevent_injection.yml -i inventory -v "$@"

# ensure fact merging is working properly
assible-playbook verify_merge_facts.yml -v "$@" -e 'assible_facts_parallel: False'

# ensure we dont clobber facts in loop
assible-playbook prevent_clobbering.yml -v "$@"
