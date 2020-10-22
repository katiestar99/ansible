#!/usr/bin/env bash

set -eux

[ -f "${INVENTORY}" ]

# Run connection tests with both the default and C locale.

                assible-playbook test_connection.yml -i "${INVENTORY}" "$@"
LC_ALL=C LANG=C assible-playbook test_connection.yml -i "${INVENTORY}" "$@"

# Check that connection vars do not appear in the output
# https://github.com/assible/assible/pull/70853
trap "rm out.txt" EXIT

assible all -i "${INVENTORY}" -m set_fact -a "testing=value" -v | tee out.txt
if grep 'assible_host' out.txt
then
    echo "FAILURE: Connection vars in output"
    exit 1
else
    echo "SUCCESS: Connection vars not found"
fi
