#!/usr/bin/env bash

set -eux
assible-playbook test.yml -i inventory "$@"

(
unset ASSIBLE_PLAYBOOK_DIR
cd "$(dirname "$0")"

# test module docs from collection
current_out="$(assible-doc --playbook-dir ./ testns.testcol.fakemodule)"
expected_out="$(cat fakemodule.output)"
test "$current_out" == "$expected_out"

# test listing diff plugin types from collection
for ptype in cache inventory lookup vars
do
	# each plugin type adds 1 from collection
	# FIXME pre=$(assible-doc -l -t ${ptype}|wc -l)
	# FIXME post=$(assible-doc -l -t ${ptype} --playbook-dir ./|wc -l)
	# FIXME test "$pre" -eq $((post - 1))

	# ensure we ONLY list from the collection
	justcol=$(assible-doc -l -t ${ptype} --playbook-dir ./ testns.testcol|wc -l)
	test "$justcol" -eq 1

	# ensure we get 0 plugins when restricting to collection, but not supplying it
	justcol=$(assible-doc -l -t ${ptype} testns.testcol|wc -l)
	test "$justcol" -eq 0

	# ensure we get 1 plugins when restricting namespace
	justcol=$(assible-doc -l -t ${ptype} --playbook-dir ./ testns|wc -l)
	test "$justcol" -eq 1
done
)
