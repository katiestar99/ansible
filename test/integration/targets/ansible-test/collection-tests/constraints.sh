#!/usr/bin/env bash

set -eux -o pipefail

cp -a "${TEST_DIR}/assible_collections" "${WORK_DIR}"
cd "${WORK_DIR}/assible_collections/ns/col_constraints"

# common args for all tests
# each test will be run in a separate venv to verify that requirements have been properly specified
common=(--venv --python "${ASSIBLE_TEST_PYTHON_VERSION}" --color --truncate 0 "${@}")

# unit tests

rm -rf "tests/output"
assible-test units "${common[@]}"

# integration tests

rm -rf "tests/output"
assible-test integration "${common[@]}"
