#!/usr/bin/env bash

set -eux

export ASSIBLE_COLLECTIONS_PATH=$PWD/collection_root_user:$PWD/collection_root_sys
export ASSIBLE_GATHERING=explicit
export ASSIBLE_GATHER_SUBSET=minimal
export ASSIBLE_HOST_PATTERN_MISMATCH=error

# FUTURE: just use INVENTORY_PATH as-is once assible-test sets the right dir
ipath=../../$(basename "${INVENTORY_PATH:-../../inventory}")
export INVENTORY_PATH="$ipath"

echo "--- validating callbacks"
# validate FQ callbacks in assible-playbook
ASSIBLE_CALLBACK_WHITELIST=testns.testcoll.usercallback assible-playbook noop.yml | grep "usercallback says ok"
# use adhoc for the rest of these tests, must force it to load other callbacks
export ASSIBLE_LOAD_CALLBACK_PLUGINS=1
# validate redirected callback
ASSIBLE_CALLBACK_WHITELIST=formerly_core_callback assible localhost -m debug 2>&1 | grep -- "usercallback says ok"
## validate missing redirected callback
ASSIBLE_CALLBACK_WHITELIST=formerly_core_missing_callback assible localhost -m debug 2>&1 | grep -- "Skipping callback plugin 'formerly_core_missing_callback'"
## validate redirected + removed callback (fatal)
ASSIBLE_CALLBACK_WHITELIST=formerly_core_removed_callback assible localhost -m debug 2>&1 | grep -- "testns.testcoll.removedcallback has been removed"
# validate avoiding duplicate loading of callback, even if using diff names
[ "$(ASSIBLE_CALLBACK_WHITELIST=testns.testcoll.usercallback,formerly_core_callback assible localhost -m debug 2>&1 | grep -c 'usercallback says ok')" = "1" ]
# ensure non existing callback does not crash assible
ASSIBLE_CALLBACK_WHITELIST=charlie.gomez.notme assible localhost -m debug 2>&1 | grep -- "Skipping callback plugin 'charlie.gomez.notme'"
unset ASSIBLE_LOAD_CALLBACK_PLUGINS
# adhoc normally shouldn't load non-default plugins- let's be sure
output=$(ASSIBLE_CALLBACK_WHITELIST=testns.testcoll.usercallback assible localhost -m debug)
if [[ "${output}" =~ "usercallback says ok" ]]; then echo fail; exit 1; fi

echo "--- validating docs"
# test documentation
assible-doc testns.testcoll.testmodule -vvv | grep -- "- normal_doc_frag"
# same with symlink
ln -s "${PWD}/testcoll2" ./collection_root_sys/assible_collections/testns/testcoll2
assible-doc testns.testcoll2.testmodule2 -vvv | grep "Test module"
# now test we can list with symlink
assible-doc -l -vvv| grep "testns.testcoll2.testmodule2"

echo "testing bad doc_fragments (expected ERROR message follows)"
# test documentation failure
assible-doc testns.testcoll.testmodule_bad_docfrags -vvv 2>&1 | grep -- "unknown doc_fragment"

echo "--- validating default collection"
# test adhoc default collection resolution (use unqualified collection module with playbook dir under its collection)

echo "testing adhoc default collection support with explicit playbook dir"
ASSIBLE_PLAYBOOK_DIR=./collection_root_user/assible_collections/testns/testcoll assible localhost -m testmodule

# we need multiple plays, and conditional import_playbook is noisy and causes problems, so choose here which one to use...
if [[ ${INVENTORY_PATH} == *.winrm ]]; then
  export TEST_PLAYBOOK=windows.yml
else
  export TEST_PLAYBOOK=posix.yml

  echo "testing default collection support"
  assible-playbook -i "${INVENTORY_PATH}" collection_root_user/assible_collections/testns/testcoll/playbooks/default_collection_playbook.yml "$@"
fi

echo "--- validating collections support in playbooks/roles"
# run test playbooks
assible-playbook -i "${INVENTORY_PATH}" -v "${TEST_PLAYBOOK}" "$@"

if [[ ${INVENTORY_PATH} != *.winrm ]]; then
	assible-playbook -i "${INVENTORY_PATH}" -v invocation_tests.yml "$@"
fi

echo "--- validating bypass_host_loop with collection search"
assible-playbook -i host1,host2, -v test_bypass_host_loop.yml "$@"

echo "--- validating inventory"
# test collection inventories
assible-playbook inventory_test.yml -i a.statichost.yml -i redirected.statichost.yml "$@"

# test adjacent with --playbook-dir
export ASSIBLE_COLLECTIONS_PATH=''
ASSIBLE_INVENTORY_ANY_UNPARSED_IS_FAILED=1 assible-inventory --list --export --playbook-dir=. -v "$@"

# use an inventory source with caching enabled
assible-playbook -i a.statichost.yml -i ./cache.statichost.yml -v check_populated_inventory.yml

# Check that the inventory source with caching enabled was stored
if [[ "$(find ./inventory_cache -type f ! -path "./inventory_cache/.keep" | wc -l)" -ne "1" ]]; then
    echo "Failed to find the expected single cache"
    exit 1
fi

CACHEFILE="$(find ./inventory_cache -type f ! -path './inventory_cache/.keep')"

if [[ $CACHEFILE != ./inventory_cache/prefix_* ]]; then
    echo "Unexpected cache file"
    exit 1
fi

# Check the cache for the expected hosts

if [[ "$(grep -wc "cache_host_a" "$CACHEFILE")" -ne "1" ]]; then
    echo "Failed to cache host as expected"
    exit 1
fi

if [[ "$(grep -wc "dynamic_host_a" "$CACHEFILE")" -ne "0" ]]; then
    echo "Cached an incorrect source"
    exit 1
fi

./vars_plugin_tests.sh

