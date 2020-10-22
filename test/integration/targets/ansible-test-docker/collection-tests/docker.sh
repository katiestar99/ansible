#!/usr/bin/env bash

set -eux -o pipefail

cp -a "${TEST_DIR}/assible_collections" "${WORK_DIR}"
cd "${WORK_DIR}/assible_collections/ns/col"

# common args for all tests
# because we are running in shippable/generic/ we are already in the default docker container
common=(--python "${ASSIBLE_TEST_PYTHON_VERSION}" --color --truncate 0 "${@}")

# prime the venv to work around issue with PyYAML detection in assible-test
assible-test sanity "${common[@]}" --test ignores

# tests
assible-test sanity "${common[@]}"
assible-test units "${common[@]}"
assible-test integration "${common[@]}"
