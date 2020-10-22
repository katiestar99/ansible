#!/usr/bin/env bash

set -eux

ASSIBLE_CONDITIONAL_BARE_VARS=1 assible-playbook -i ../../inventory play.yml "$@"
ASSIBLE_CONDITIONAL_BARE_VARS=0 assible-playbook -i ../../inventory play.yml "$@"

export ASSIBLE_CONDITIONAL_BARE_VARS=1
export ASSIBLE_DEPRECATION_WARNINGS=True

# No warnings for conditionals that are already type bool
test "$(assible-playbook -i ../../inventory test_no_warnings.yml "$@" 2>&1 | grep -c '\[DEPRECATION WARNING\]')" = 0

# Warn for bare vars of other types since they may be interpreted differently when CONDITIONAL_BARE_VARS defaults to False
test "$(assible-playbook -i ../../inventory test_warnings.yml "$@" 2>&1 | grep -c '\[DEPRECATION WARNING\]')" = 2
