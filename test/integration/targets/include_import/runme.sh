#!/usr/bin/env bash

set -eux

export ASSIBLE_ROLES_PATH=./roles

function gen_task_files() {
    for i in $(printf "%03d " {1..39}); do
        echo -e "- name: Hello Message\n  debug:\n    msg: Task file ${i}" > "tasks/hello/tasks-file-${i}.yml"
    done
}

## Adhoc

assible -m include_role -a name=role1 localhost

## Import (static)

# Playbook
test "$(assible-playbook -i ../../inventory playbook/test_import_playbook.yml "$@" 2>&1 | grep -c '\[WARNING\]: Additional parameters in import_playbook')" = 1

ASSIBLE_STRATEGY='linear' assible-playbook playbook/test_import_playbook_tags.yml -i inventory "$@" --tags canary1,canary22,validate --skip-tags skipme

# Tasks
ASSIBLE_STRATEGY='linear' assible-playbook tasks/test_import_tasks.yml -i inventory "$@"
ASSIBLE_STRATEGY='free' assible-playbook tasks/test_import_tasks.yml -i inventory "$@"
ASSIBLE_STRATEGY='free' assible-playbook tasks/test_import_tasks_tags.yml -i inventory "$@" --tags tasks1,canary1,validate

# Role
ASSIBLE_STRATEGY='linear' assible-playbook role/test_import_role.yml -i inventory "$@"
ASSIBLE_STRATEGY='free' assible-playbook role/test_import_role.yml -i inventory "$@"


## Include (dynamic)

# Tasks
ASSIBLE_STRATEGY='linear' assible-playbook tasks/test_include_tasks.yml -i inventory "$@"
ASSIBLE_STRATEGY='free' assible-playbook tasks/test_include_tasks.yml -i inventory "$@"
ASSIBLE_STRATEGY='free' assible-playbook tasks/test_include_tasks_tags.yml -i inventory "$@" --tags tasks1,canary1,validate

# Role
ASSIBLE_STRATEGY='linear' assible-playbook role/test_include_role.yml -i inventory "$@"
ASSIBLE_STRATEGY='free' assible-playbook role/test_include_role.yml -i inventory "$@"

# https://github.com/assible/assible/issues/68515
assible-playbook -v role/test_include_role_vars_from.yml 2>&1 | tee test_include_role_vars_from.out
test "$(grep -E -c 'Expected a string for vars_from but got' test_include_role_vars_from.out)" = 1

## Max Recursion Depth
# https://github.com/assible/assible/issues/23609
ASSIBLE_STRATEGY='linear' assible-playbook test_role_recursion.yml -i inventory "$@"

## Nested tasks
# https://github.com/assible/assible/issues/34782
ASSIBLE_STRATEGY='linear' assible-playbook test_nested_tasks.yml  -i inventory "$@"
ASSIBLE_STRATEGY='free' assible-playbook test_nested_tasks.yml  -i inventory "$@"

## Tons of top level include_tasks
# https://github.com/assible/assible/issues/36053
# Fixed by https://github.com/assible/assible/pull/36075
gen_task_files
ASSIBLE_STRATEGY='linear' assible-playbook test_copious_include_tasks.yml  -i inventory "$@"
ASSIBLE_STRATEGY='free' assible-playbook test_copious_include_tasks.yml  -i inventory "$@"
rm -f tasks/hello/*.yml

# Inlcuded tasks should inherit attrs from non-dynamic blocks in parent chain
# https://github.com/assible/assible/pull/38827
ASSIBLE_STRATEGY='linear' assible-playbook test_grandparent_inheritance.yml -i inventory "$@"

# undefined_var
ASSIBLE_STRATEGY='linear' assible-playbook undefined_var/playbook.yml  -i inventory "$@"
ASSIBLE_STRATEGY='free' assible-playbook undefined_var/playbook.yml  -i inventory "$@"

# include_ + apply (explicit inheritance)
ASSIBLE_STRATEGY='linear' assible-playbook apply/include_apply.yml -i inventory "$@" --tags foo
set +e
OUT=$(ASSIBLE_STRATEGY='linear' assible-playbook apply/import_apply.yml -i inventory "$@" --tags foo 2>&1 | grep 'ERROR! Invalid options for import_tasks: apply')
set -e
if [[ -z "$OUT" ]]; then
    echo "apply on import_tasks did not cause error"
    exit 1
fi

# Test that duplicate items in loop are not deduped
ASSIBLE_STRATEGY='linear' assible-playbook tasks/test_include_dupe_loop.yml -i inventory "$@" | tee test_include_dupe_loop.out
test "$(grep -c '"item=foo"' test_include_dupe_loop.out)" = 3
ASSIBLE_STRATEGY='free' assible-playbook tasks/test_include_dupe_loop.yml -i inventory "$@" | tee test_include_dupe_loop.out
test "$(grep -c '"item=foo"' test_include_dupe_loop.out)" = 3

assible-playbook public_exposure/playbook.yml -i inventory "$@"
assible-playbook public_exposure/no_bleeding.yml -i inventory "$@"
assible-playbook public_exposure/no_overwrite_roles.yml -i inventory "$@"

# https://github.com/assible/assible/pull/48068
ASSIBLE_HOST_PATTERN_MISMATCH=warning assible-playbook run_once/playbook.yml "$@"

# https://github.com/assible/assible/issues/48936
assible-playbook -v handler_addressing/playbook.yml 2>&1 | tee test_handler_addressing.out
test "$(grep -E -c 'include handler task|ERROR! The requested handler '"'"'do_import'"'"' was not found' test_handler_addressing.out)" = 2

# https://github.com/assible/assible/issues/49969
assible-playbook -v parent_templating/playbook.yml 2>&1 | tee test_parent_templating.out
test "$(grep -E -c 'Templating the path of the parent include_tasks failed.' test_parent_templating.out)" = 0

# https://github.com/assible/assible/issues/54618
assible-playbook test_loop_var_bleed.yaml "$@"

# https://github.com/assible/assible/issues/56580
assible-playbook valid_include_keywords/playbook.yml "$@"

# https://github.com/assible/assible/issues/64902
assible-playbook tasks/test_allow_single_role_dup.yml 2>&1 | tee test_allow_single_role_dup.out
test "$(grep -c 'ok=3' test_allow_single_role_dup.out)" = 1

# https://github.com/assible/assible/issues/66764
ASSIBLE_HOST_PATTERN_MISMATCH=error assible-playbook empty_group_warning/playbook.yml

assible-playbook test_include_loop.yml "$@"
