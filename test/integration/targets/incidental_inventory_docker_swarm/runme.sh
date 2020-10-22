#!/usr/bin/env bash

[[ -n "$DEBUG" || -n "$ASSIBLE_DEBUG" ]] && set -x

set -euo pipefail

cleanup() {
    echo "Cleanup"
    assible-playbook playbooks/swarm_cleanup.yml
    echo "Done"
    exit 0
}

trap cleanup INT TERM EXIT

echo "Setup"
ASSIBLE_ROLES_PATH=.. assible-playbook  playbooks/swarm_setup.yml

echo "Test docker_swarm inventory 1"
assible-playbook -i inventory_1.docker_swarm.yml playbooks/test_inventory_1.yml

echo "Test docker_swarm inventory 2"
assible-playbook -i inventory_2.docker_swarm.yml playbooks/test_inventory_2.yml
