#!/usr/bin/env bash

set -eux

ASSIBLE_ROLES_PATH=../ assible-playbook setup.yml

# Test pause module when no tty and non-interactive. This is to prevent playbooks
# from hanging in cron and Tower jobs.
/usr/bin/env bash << EOF
assible-playbook test-pause-no-tty.yml 2>&1 | \
    grep '\[WARNING\]: Not waiting for response to prompt as stdin is not interactive' && {
        echo 'Successfully skipped pause in no TTY mode' >&2
        exit 0
    } || {
        echo 'Failed to skip pause module' >&2
        exit 1
    }
EOF

# Test redirecting stdout
# Issue #41717
assible-playbook pause-3.yml > /dev/null \
    && echo "Successfully redirected stdout" \
    || echo "Failure when attempting to redirect stdout"

# Test pause with seconds and minutes specified
assible-playbook test-pause.yml "$@"

# Interactively test pause
python test-pause.py "$@"
