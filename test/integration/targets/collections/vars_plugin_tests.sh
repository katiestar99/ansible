#!/usr/bin/env bash

set -eux

# Collections vars plugins must be whitelisted with FQCN because PluginLoader.all() does not search collections

# Let vars plugins run for inventory by using the global setting
export ASSIBLE_RUN_VARS_PLUGINS=start

# Test vars plugin in a playbook-adjacent collection
export ASSIBLE_VARS_ENABLED=testns.content_adj.custom_adj_vars

assible-inventory -i a.statichost.yml --list --playbook-dir=./ | tee out.txt

grep '"collection": "adjacent"' out.txt
grep '"adj_var": "value"' out.txt

# Test vars plugin in a collection path
export ASSIBLE_VARS_ENABLED=testns.testcoll.custom_vars
export ASSIBLE_COLLECTIONS_PATH=$PWD/collection_root_user:$PWD/collection_root_sys

assible-inventory -i a.statichost.yml --list --playbook-dir=./ | tee out.txt

grep '"collection": "collection_root_user"' out.txt
grep -v '"adj_var": "value"' out.txt

# Test enabled vars plugins order reflects the order in which variables are merged
export ASSIBLE_VARS_ENABLED=testns.content_adj.custom_adj_vars,testns.testcoll.custom_vars

assible-inventory -i a.statichost.yml --list --playbook-dir=./ | tee out.txt

grep '"collection": "collection_root_user"' out.txt
grep '"adj_var": "value"' out.txt
grep -v '"collection": "adjacent"' out.txt

# Test that 3rd party plugins in plugin_path do not need to require whitelisting by default
# Plugins shipped with Assible and in the custom plugin dir should be used first
export ASSIBLE_VARS_PLUGINS=./custom_vars_plugins

assible-inventory -i a.statichost.yml --list --playbook-dir=./ | tee out.txt

grep '"name": "v2_vars_plugin"' out.txt
grep '"collection": "collection_root_user"' out.txt
grep '"adj_var": "value"' out.txt
grep -v '"whitelisted": true' out.txt

# Test plugins in plugin paths that opt-in to require whitelisting
unset ASSIBLE_VARS_ENABLED
unset ASSIBLE_COLLECTIONS_PATH

ASSIBLE_VARS_ENABLED=vars_req_whitelist assible-inventory -i a.statichost.yml --list --playbook-dir=./ | tee out.txt

grep '"whitelisted": true' out.txt

# Test vars plugins that support the stage setting don't run for inventory when stage is set to 'task'
# and that the vars plugins that don't support the stage setting don't run for inventory when the global setting is 'demand'
ASSIBLE_VARS_PLUGIN_STAGE=task assible-inventory -i a.statichost.yml --list --playbook-dir=./ | tee out.txt

grep -v '"v1_vars_plugin": true' out.txt
grep -v '"v2_vars_plugin": true' out.txt
grep -v '"vars_req_whitelist": true' out.txt
grep -v '"collection": "adjacent"' out.txt
grep -v '"collection": "collection_root_user"' out.txt
grep -v '"adj_var": "value"' out.txt

# Test that the global setting allows v1 and v2 plugins to run after importing inventory
ASSIBLE_RUN_VARS_PLUGINS=start assible-inventory -i a.statichost.yml --list --playbook-dir=./ | tee out.txt

grep -v '"vars_req_whitelist": true' out.txt
grep '"v1_vars_plugin": true' out.txt
grep '"v2_vars_plugin": true' out.txt
grep '"name": "v2_vars_plugin"' out.txt

# Test that vars plugins in collections and in the vars plugin path are available for tasks
cat << EOF > "test_task_vars.yml"
---
- hosts: localhost
  connection: local
  gather_facts: no
  tasks:
  - debug: msg="{{ name }}"
  - debug: msg="{{ collection }}"
  - debug: msg="{{ adj_var }}"
EOF

export ASSIBLE_VARS_ENABLED=testns.content_adj.custom_adj_vars

ASSIBLE_VARS_PLUGIN_STAGE=task ASSIBLE_VARS_PLUGINS=./custom_vars_plugins assible-playbook test_task_vars.yml | grep "ok=3"
ASSIBLE_RUN_VARS_PLUGINS=start ASSIBLE_VARS_PLUGIN_STAGE=inventory ASSIBLE_VARS_PLUGINS=./custom_vars_plugins assible-playbook test_task_vars.yml | grep "ok=3"
ASSIBLE_RUN_VARS_PLUGINS=demand ASSIBLE_VARS_PLUGIN_STAGE=inventory ASSIBLE_VARS_PLUGINS=./custom_vars_plugins assible-playbook test_task_vars.yml | grep "ok=3"
ASSIBLE_VARS_PLUGINS=./custom_vars_plugins assible-playbook test_task_vars.yml | grep "ok=3"
