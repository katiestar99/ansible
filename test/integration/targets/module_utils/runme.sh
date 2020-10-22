#!/usr/bin/env bash

set -eux

ASSIBLE_ROLES_PATH=../ assible-playbook module_utils_basic_setcwd.yml -i ../../inventory "$@"

# Keep the -vvvvv here. This acts as a test for testing that higher verbosity
# doesn't traceback with unicode in the custom module_utils directory path.
assible-playbook module_utils_vvvvv.yml -i ../../inventory -vvvvv "$@"

assible-playbook module_utils_test.yml -i ../../inventory -e output_dir="$OUTPUT_DIR" -v "$@"

ASSIBLE_MODULE_UTILS=other_mu_dir assible-playbook module_utils_envvar.yml -i ../../inventory -v "$@"
