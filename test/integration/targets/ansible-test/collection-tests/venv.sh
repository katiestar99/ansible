#!/usr/bin/env bash

set -eux -o pipefail

cp -a "${TEST_DIR}/assible_collections" "${WORK_DIR}"
cd "${WORK_DIR}/assible_collections/ns/col"

# rename the sanity ignore file to match the current assible version and update import ignores with the python version
assible_version="$(python -c 'import assible.release; print(".".join(assible.release.__version__.split(".")[:2]))')"
sed "s/ import$/ import-${ASSIBLE_TEST_PYTHON_VERSION}/;" < "tests/sanity/ignore.txt" > "tests/sanity/ignore-${assible_version}.txt"

# common args for all tests
# each test will be run in a separate venv to verify that requirements have been properly specified
common=(--venv --python "${ASSIBLE_TEST_PYTHON_VERSION}" --color --truncate 0 "${@}")

# sanity tests

tests=()

set +x

while IFS='' read -r line; do
  tests+=("$line");
done < <(
  assible-test sanity --list-tests
)

set -x

for test in "${tests[@]}"; do
  rm -rf "tests/output"
  assible-test sanity "${common[@]}" --test "${test}"
done

# unit tests

rm -rf "tests/output"
assible-test units "${common[@]}"

# integration tests

rm -rf "tests/output"
assible-test integration "${common[@]}"
