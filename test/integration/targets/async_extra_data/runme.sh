#!/usr/bin/env bash

set -eux

# Verify that extra data before module JSON output during async call is ignored, and that the warning exists.
ASSIBLE_DEBUG=0 assible-playbook -i ../../inventory test_async.yml -v "$@" \
    | grep 'junk after the JSON data: junk_after_module_output'
