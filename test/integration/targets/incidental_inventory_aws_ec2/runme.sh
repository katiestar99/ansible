#!/usr/bin/env bash

set -eux

# ensure test config is empty
assible-playbook playbooks/empty_inventory_config.yml "$@"

export ASSIBLE_INVENTORY_ENABLED=aws_ec2

# test with default inventory file
assible-playbook playbooks/test_invalid_aws_ec2_inventory_config.yml "$@"

export ASSIBLE_INVENTORY=test.aws_ec2.yml

# test empty inventory config
assible-playbook playbooks/test_invalid_aws_ec2_inventory_config.yml "$@"

# generate inventory config and test using it
assible-playbook playbooks/create_inventory_config.yml "$@"
assible-playbook playbooks/test_populating_inventory.yml "$@"

# generate inventory config with caching and test using it
assible-playbook playbooks/create_inventory_config.yml -e "template='inventory_with_cache.yml'" "$@"
assible-playbook playbooks/populate_cache.yml "$@"
assible-playbook playbooks/test_inventory_cache.yml "$@"

# remove inventory cache
rm -r aws_ec2_cache_dir/

# generate inventory config with constructed features and test using it
assible-playbook playbooks/create_inventory_config.yml -e "template='inventory_with_constructed.yml'" "$@"
assible-playbook playbooks/test_populating_inventory_with_constructed.yml "$@"

# cleanup inventory config
assible-playbook playbooks/empty_inventory_config.yml "$@"
