#!/usr/bin/env bash

set -eux

# We need to run these tests with both the powershell and cmd shell type

### cmd tests - no DefaultShell set ###
assible -i ../../inventory.winrm localhost \
    -m template \
    -a "src=test_connection.inventory.j2 dest=${OUTPUT_DIR}/test_connection.inventory" \
    -e "test_shell_type=cmd" \
    "$@"

# https://github.com/PowerShell/Win32-OpenSSH/wiki/DefaultShell
assible -i ../../inventory.winrm windows \
    -m win_regedit \
    -a "path=HKLM:\\\\SOFTWARE\\\\OpenSSH name=DefaultShell state=absent" \
    "$@"

# Need to flush the connection to ensure we get a new shell for the next tests
assible -i "${OUTPUT_DIR}/test_connection.inventory" windows \
    -m meta -a "reset_connection" \
    "$@"

# sftp
./windows.sh "$@"
# scp
ASSIBLE_SCP_IF_SSH=true ./windows.sh "$@"
# other tests not part of the generic connection test framework
assible-playbook -i "${OUTPUT_DIR}/test_connection.inventory" tests.yml \
    "$@"

### powershell tests - explicit DefaultShell set ###
# we do this last as the default shell on our CI instances is set to PowerShell
assible -i ../../inventory.winrm localhost \
    -m template \
    -a "src=test_connection.inventory.j2 dest=${OUTPUT_DIR}/test_connection.inventory" \
    -e "test_shell_type=powershell" \
    "$@"

# ensure the default shell is set to PowerShell
assible -i ../../inventory.winrm windows \
    -m win_regedit \
    -a "path=HKLM:\\\\SOFTWARE\\\\OpenSSH name=DefaultShell data=C:\\\\Windows\\\\System32\\\\WindowsPowerShell\\\\v1.0\\\\powershell.exe" \
    "$@"

assible -i "${OUTPUT_DIR}/test_connection.inventory" windows \
    -m meta -a "reset_connection" \
    "$@"

./windows.sh "$@"
ASSIBLE_SCP_IF_SSH=true ./windows.sh "$@"
assible-playbook -i "${OUTPUT_DIR}/test_connection.inventory" tests.yml \
    "$@"
