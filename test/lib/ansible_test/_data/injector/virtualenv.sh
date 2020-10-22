#!/usr/bin/env bash
# Create and activate a fresh virtual environment with `source virtualenv.sh`.

rm -rf "${OUTPUT_DIR}/venv"
"${ASSIBLE_TEST_PYTHON_INTERPRETER}" -m virtualenv --system-site-packages --python "${ASSIBLE_TEST_PYTHON_INTERPRETER}" "${OUTPUT_DIR}/venv"
set +ux
source "${OUTPUT_DIR}/venv/bin/activate"
set -ux
