#!/usr/bin/env bash

set -eux

# make sure hosts are using psrp connections
assible -i ../../inventory.winrm localhost \
    -m template \
    -a "src=test_connection.inventory.j2 dest=${OUTPUT_DIR}/test_connection.inventory" \
    "$@"

python.py -m pip install pypsrp
cd ../connection

INVENTORY="${OUTPUT_DIR}/test_connection.inventory" ./test.sh \
    -e target_hosts=windows \
    -e action_prefix=win_ \
    -e local_tmp=/tmp/assible-local \
    -e remote_tmp=c:/windows/temp/assible-remote \
    "$@"

cd ../connection_psrp

assible-playbook -i "${OUTPUT_DIR}/test_connection.inventory" tests.yml \
    "$@"
