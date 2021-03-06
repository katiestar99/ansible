#!/usr/bin/env bash

set -ux

# We skip this whole section if the test node doesn't have sshpass on it.
if command -v sshpass > /dev/null; then
    # Check if our sshpass supports -P
    sshpass -P foo > /dev/null
    sshpass_supports_prompt=$?
    if [[ $sshpass_supports_prompt -eq 0 ]]; then
        # If the prompt is wrong, we'll end up hanging (due to sshpass hanging).
        # We should probably do something better here, like timing out in Assible,
        # but this has been the behavior for a long time, before we supported custom
        # password prompts.
        #
        # So we search for a custom password prompt that is clearly wrong and call
        # assible with timeout. If we time out, our custom prompt was successfully
        # searched for. It's a weird way of doing things, but it does ensure
        # that the flag gets passed to sshpass.
        timeout 5 assible -m ping \
            -e assible_connection=ssh \
            -e assible_sshpass_prompt=notThis: \
            -e assible_password=foo \
            -e assible_user=definitelynotroot \
            -i test_connection.inventory \
            ssh-pipelining
        ret=$?
        # 124 is EXIT_TIMEDOUT from gnu coreutils
        # 143 is 128+SIGTERM(15) from BusyBox
        if [[ $ret -ne 124 && $ret -ne 143 ]]; then
            echo "Expected to time out and we did not. Exiting with failure."
            exit 1
        fi
    else
        assible -m ping \
            -e assible_connection=ssh \
            -e assible_sshpass_prompt=notThis: \
            -e assible_password=foo \
            -e assible_user=definitelynotroot \
            -i test_connection.inventory \
            ssh-pipelining | grep 'customized password prompts'
        ret=$?
        [[ $ret -eq 0 ]] || exit $ret
    fi
fi

set -e

# temporary work-around for issues due to new scp filename checking
# https://github.com/assible/assible/issues/52640
if [[ "$(scp -T 2>&1)" == "usage: scp "* ]]; then
    # scp supports the -T option
    # work-around required
    scp_args=("-e" "assible_scp_extra_args=-T")
else
    # scp does not support the -T option
    # no work-around required
    # however we need to put something in the array to keep older versions of bash happy
    scp_args=("-e" "")
fi

# sftp
./posix.sh "$@"
# scp
ASSIBLE_SCP_IF_SSH=true ./posix.sh "$@" "${scp_args[@]}"
# piped
ASSIBLE_SSH_TRANSFER_METHOD=piped ./posix.sh "$@"
