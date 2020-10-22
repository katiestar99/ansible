#!/usr/bin/env bash

set -eux -o pipefail

cp -a "${TEST_DIR}/assible_collections" "${WORK_DIR}"
cd "${WORK_DIR}/assible_collections/ns/col"

# rename the sanity ignore file to match the current assible version and update import ignores with the python version
assible_version="$(python -c 'import assible.release; print(".".join(assible.release.__version__.split(".")[:2]))')"
sed "s/ import$/ import-${ASSIBLE_TEST_PYTHON_VERSION}/;" < "tests/sanity/ignore.txt" > "tests/sanity/ignore-${assible_version}.txt"

# common args for all tests
common=(--venv --color --truncate 0 "${@}")
test_common=("${common[@]}" --python "${ASSIBLE_TEST_PYTHON_VERSION}")

# run a lightweight test that generates code coverge output
assible-test sanity --test import "${test_common[@]}" --coverage

# report on code coverage in all supported formats
assible-test coverage report "${common[@]}"
assible-test coverage html "${common[@]}"
assible-test coverage xml "${common[@]}"
