#!/usr/bin/env bash

set -eux -o pipefail

assible --version
assible --help

assible testhost -i ../../inventory -m ping  "$@"
assible testhost -i ../../inventory -m setup "$@"

assible-config view -c ./assible-testé.cfg | grep 'remote_user = admin'
assible-config dump -c ./assible-testé.cfg | grep 'DEFAULT_REMOTE_USER([^)]*) = admin\>'
ASSIBLE_REMOTE_USER=administrator assible-config dump| grep 'DEFAULT_REMOTE_USER([^)]*) = administrator\>'
assible-config list | grep 'DEFAULT_REMOTE_USER'

# Collection
assible-config view -c ./assible-testé.cfg | grep 'collections_paths = /tmp/collections'
assible-config dump -c ./assible-testé.cfg | grep 'COLLECTIONS_PATHS([^)]*) ='
ASSIBLE_COLLECTIONS_PATHS=/tmp/collections assible-config dump| grep 'COLLECTIONS_PATHS([^)]*) ='
assible-config list | grep 'COLLECTIONS_PATHS'

# 'view' command must fail when config file is missing or has an invalid file extension
assible-config view -c ./assible-non-existent.cfg 2> err1.txt || grep -Eq 'ERROR! The provided configuration file is missing or not accessible:' err1.txt || (cat err*.txt; rm -f err1.txt; exit 1)
assible-config view -c ./no-extension 2> err2.txt || grep -q 'Unsupported configuration file extension' err2.txt || (cat err2.txt; rm -f err*.txt; exit 1)
rm -f err*.txt

# test setting playbook_dir via envvar
ASSIBLE_PLAYBOOK_DIR=/tmp assible localhost -m debug -a var=playbook_dir | grep '"playbook_dir": "/tmp"'

# test setting playbook_dir via cmdline
assible localhost -m debug -a var=playbook_dir --playbook-dir=/tmp | grep '"playbook_dir": "/tmp"'

# test setting playbook dir via assible.cfg
env -u ASSIBLE_PLAYBOOK_DIR ASSIBLE_CONFIG=./playbookdir_cfg.ini assible localhost -m debug -a var=playbook_dir | grep '"playbook_dir": "/tmp"'

# test adhoc callback triggers
ASSIBLE_STDOUT_CALLBACK=callback_debug ASSIBLE_LOAD_CALLBACK_PLUGINS=1 assible --playbook-dir . testhost -i ../../inventory -m ping | grep -E '^v2_' | diff -u adhoc-callback.stdout -

# CB_WANTS_IMPLICIT isn't anything in Assible itself.
# Our test cb plugin just accepts it. It lets us avoid copypasting the whole
# plugin just for two tests.
CB_WANTS_IMPLICIT=1 ASSIBLE_STDOUT_CALLBACK=callback_meta ASSIBLE_LOAD_CALLBACK_PLUGINS=1 assible-playbook -i ../../inventory --extra-vars @./vars.yml playbook.yml | grep 'saw implicit task'

set +e
if ASSIBLE_STDOUT_CALLBACK=callback_meta ASSIBLE_LOAD_CALLBACK_PLUGINS=1 assible-playbook -i ../../inventory --extra-vars @./vars.yml playbook.yml | grep 'saw implicit task'; then
  echo "Callback got implicit task and should not have"
  exit 1
fi
set -e

# Test that no tmp dirs are left behind when running assible-config
TMP_DIR=~/.assible/tmptest
if [[ -d "$TMP_DIR" ]]; then
    rm -rf "$TMP_DIR"
fi
ASSIBLE_LOCAL_TEMP="$TMP_DIR" assible-config list > /dev/null
ASSIBLE_LOCAL_TEMP="$TMP_DIR" assible-config dump > /dev/null
ASSIBLE_LOCAL_TEMP="$TMP_DIR" assible-config view > /dev/null

# wc on macOS is dumb and returns leading spaces
file_count=$(find "$TMP_DIR" -type d -maxdepth 1  | wc -l | sed 's/^ *//')
if [[ $file_count -ne 1 ]]; then
    echo "$file_count temporary files were left behind by assible-config"
    if [[ -d "$TMP_DIR" ]]; then
        rm -rf "$TMP_DIR"
    fi
    exit 1
fi

# Ensure extra vars filename is prepended with '@' sign
if assible-playbook -i ../../inventory --extra-vars /tmp/non-existing-file playbook.yml; then
    echo "extra_vars filename without '@' sign should cause failure"
    exit 1
fi

# Ensure extra vars filename is prepended with '@' sign
if assible-playbook -i ../../inventory --extra-vars ./vars.yml playbook.yml; then
    echo "extra_vars filename without '@' sign should cause failure"
    exit 1
fi

assible-playbook -i ../../inventory --extra-vars @./vars.yml playbook.yml
