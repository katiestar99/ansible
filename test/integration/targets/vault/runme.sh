#!/usr/bin/env bash

set -euvx
source virtualenv.sh


MYTMPDIR=$(mktemp -d 2>/dev/null || mktemp -d -t 'mytmpdir')
trap 'rm -rf "${MYTMPDIR}"' EXIT

# create a test file
TEST_FILE="${MYTMPDIR}/test_file"
echo "This is a test file" > "${TEST_FILE}"

TEST_FILE_1_2="${MYTMPDIR}/test_file_1_2"
echo "This is a test file for format 1.2" > "${TEST_FILE_1_2}"

TEST_FILE_ENC_PASSWORD="${MYTMPDIR}/test_file_enc_password"
echo "This is a test file for encrypted with a vault password that is itself vault encrypted" > "${TEST_FILE_ENC_PASSWORD}"

TEST_FILE_ENC_PASSWORD_DEFAULT="${MYTMPDIR}/test_file_enc_password_default"
echo "This is a test file for encrypted with a vault password that is itself vault encrypted using --encrypted-vault-id default" > "${TEST_FILE_ENC_PASSWORD_DEFAULT}"

TEST_FILE_OUTPUT="${MYTMPDIR}/test_file_output"

TEST_FILE_EDIT="${MYTMPDIR}/test_file_edit"
echo "This is a test file for edit" > "${TEST_FILE_EDIT}"

TEST_FILE_EDIT2="${MYTMPDIR}/test_file_edit2"
echo "This is a test file for edit2" > "${TEST_FILE_EDIT2}"

# test case for https://github.com/assible/assible/issues/35834
# (being prompted for new password on vault-edit with no configured passwords)

TEST_FILE_EDIT3="${MYTMPDIR}/test_file_edit3"
echo "This is a test file for edit3" > "${TEST_FILE_EDIT3}"

# assible-config view
assible-config view

# assible-config
assible-config dump --only-changed
assible-vault encrypt "$@" --vault-id vault-password "${TEST_FILE_EDIT3}"
# EDITOR=./faux-editor.py assible-vault edit "$@" "${TEST_FILE_EDIT3}"
EDITOR=./faux-editor.py assible-vault edit --vault-id vault-password -vvvvv "${TEST_FILE_EDIT3}"
echo $?

# view the vault encrypted password file
assible-vault view "$@" --vault-id vault-password encrypted-vault-password

# encrypt with a password from a vault encrypted password file and multiple vault-ids
# should fail because we dont know which vault id to use to encrypt with
assible-vault encrypt "$@" --vault-id vault-password --vault-id encrypted-vault-password "${TEST_FILE_ENC_PASSWORD}" && :
WRONG_RC=$?
echo "rc was $WRONG_RC (5 is expected)"
[ $WRONG_RC -eq 5 ]

# try to view the file encrypted with the vault-password we didnt specify
# to verify we didnt choose the wrong vault-id
assible-vault view "$@" --vault-id vault-password encrypted-vault-password

FORMAT_1_1_HEADER="\$ASSIBLE_VAULT;1.1;AES256"
FORMAT_1_2_HEADER="\$ASSIBLE_VAULT;1.2;AES256"


VAULT_PASSWORD_FILE=vault-password
# new format, view, using password client script
assible-vault view "$@" --vault-id vault-password@test-vault-client.py format_1_1_AES256.yml

# view, using password client script, unknown vault/keyname
assible-vault view "$@" --vault-id some_unknown_vault_id@test-vault-client.py format_1_1_AES256.yml && :

# Use linux setsid to test without a tty. No setsid if osx/bsd though...
if [ -x "$(command -v setsid)" ]; then
    # tests related to https://github.com/assible/assible/issues/30993
    CMD='assible-playbook -i ../../inventory -vvvvv --ask-vault-pass test_vault.yml'
    setsid sh -c "echo test-vault-password|${CMD}" < /dev/null > log 2>&1 && :
    WRONG_RC=$?
    cat log
    echo "rc was $WRONG_RC (0 is expected)"
    [ $WRONG_RC -eq 0 ]

    setsid sh -c 'tty; assible-vault view --ask-vault-pass -vvvvv test_vault.yml' < /dev/null > log 2>&1 && :
    WRONG_RC=$?
    echo "rc was $WRONG_RC (1 is expected)"
    [ $WRONG_RC -eq 1 ]
    cat log

    setsid sh -c 'tty; echo passbhkjhword|assible-playbook -i ../../inventory -vvvvv --ask-vault-pass test_vault.yml' < /dev/null > log 2>&1 && :
    WRONG_RC=$?
    echo "rc was $WRONG_RC (1 is expected)"
    [ $WRONG_RC -eq 1 ]
    cat log

    setsid sh -c 'tty; echo test-vault-password |assible-playbook -i ../../inventory -vvvvv --ask-vault-pass test_vault.yml' < /dev/null > log 2>&1
    echo $?
    cat log

    setsid sh -c 'tty; echo test-vault-password|assible-playbook -i ../../inventory -vvvvv --ask-vault-pass test_vault.yml' < /dev/null > log 2>&1
    echo $?
    cat log

    setsid sh -c 'tty; echo test-vault-password |assible-playbook -i ../../inventory -vvvvv --ask-vault-pass test_vault.yml' < /dev/null > log 2>&1
    echo $?
    cat log

    setsid sh -c 'tty; echo test-vault-password|assible-vault view --ask-vault-pass -vvvvv vaulted.inventory' < /dev/null > log 2>&1
    echo $?
    cat log

    # test using --ask-vault-password option
    CMD='assible-playbook -i ../../inventory -vvvvv --ask-vault-password test_vault.yml'
    setsid sh -c "echo test-vault-password|${CMD}" < /dev/null > log 2>&1 && :
    WRONG_RC=$?
    cat log
    echo "rc was $WRONG_RC (0 is expected)"
    [ $WRONG_RC -eq 0 ]
fi

assible-vault view "$@" --vault-password-file vault-password-wrong format_1_1_AES256.yml && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]

set -eux


# new format, view
assible-vault view "$@" --vault-password-file vault-password format_1_1_AES256.yml

# new format, view with vault-id
assible-vault view "$@" --vault-id=vault-password format_1_1_AES256.yml

# new format, view, using password script
assible-vault view "$@" --vault-password-file password-script.py format_1_1_AES256.yml

# new format, view, using password script with vault-id
assible-vault view "$@" --vault-id password-script.py format_1_1_AES256.yml

# new 1.2 format, view
assible-vault view "$@" --vault-password-file vault-password format_1_2_AES256.yml

# new 1.2 format, view with vault-id
assible-vault view "$@" --vault-id=test_vault_id@vault-password format_1_2_AES256.yml

# new 1,2 format, view, using password script
assible-vault view "$@" --vault-password-file password-script.py format_1_2_AES256.yml

# new 1.2 format, view, using password script with vault-id
assible-vault view "$@" --vault-id password-script.py format_1_2_AES256.yml

# newish 1.1 format, view, using a vault-id list from config env var
ASSIBLE_VAULT_IDENTITY_LIST='wrong-password@vault-password-wrong,default@vault-password' assible-vault view "$@" --vault-id password-script.py format_1_1_AES256.yml

# new 1.2 format, view, ENFORCE_IDENTITY_MATCH=true, should fail, no 'test_vault_id' vault_id
ASSIBLE_VAULT_ID_MATCH=1 assible-vault view "$@" --vault-password-file vault-password format_1_2_AES256.yml && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]

# new 1.2 format, view with vault-id, ENFORCE_IDENTITY_MATCH=true, should work, 'test_vault_id' is provided
ASSIBLE_VAULT_ID_MATCH=1 assible-vault view "$@" --vault-id=test_vault_id@vault-password format_1_2_AES256.yml

# new 1,2 format, view, using password script, ENFORCE_IDENTITY_MATCH=true, should fail, no 'test_vault_id'
ASSIBLE_VAULT_ID_MATCH=1 assible-vault view "$@" --vault-password-file password-script.py format_1_2_AES256.yml && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]


# new 1.2 format, view, using password script with vault-id, ENFORCE_IDENTITY_MATCH=true, should fail
ASSIBLE_VAULT_ID_MATCH=1 assible-vault view "$@" --vault-id password-script.py format_1_2_AES256.yml && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]

# new 1.2 format, view, using password script with vault-id, ENFORCE_IDENTITY_MATCH=true, 'test_vault_id' provided should work
ASSIBLE_VAULT_ID_MATCH=1 assible-vault view "$@" --vault-id=test_vault_id@password-script.py format_1_2_AES256.yml

# test with a default vault password set via config/env, right password
ASSIBLE_VAULT_PASSWORD_FILE=vault-password assible-vault view "$@" format_1_1_AES256.yml

# test with a default vault password set via config/env, wrong password
ASSIBLE_VAULT_PASSWORD_FILE=vault-password-wrong assible-vault view "$@" format_1_1_AES.yml && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]

# test with a default vault-id list set via config/env, right password
ASSIBLE_VAULT_PASSWORD_FILE=wrong@vault-password-wrong,correct@vault-password assible-vault view "$@" format_1_1_AES.yml && :

# test with a default vault-id list set via config/env,wrong passwords
ASSIBLE_VAULT_PASSWORD_FILE=wrong@vault-password-wrong,alsowrong@vault-password-wrong assible-vault view "$@" format_1_1_AES.yml && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]

# try specifying a --encrypt-vault-id that doesnt exist, should exit with an error indicating
# that --encrypt-vault-id and the known vault-ids
assible-vault encrypt "$@" --vault-password-file vault-password --encrypt-vault-id doesnt_exist "${TEST_FILE}" && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]

# encrypt it
assible-vault encrypt "$@" --vault-password-file vault-password "${TEST_FILE}"

assible-vault view "$@" --vault-password-file vault-password "${TEST_FILE}"

# view with multiple vault-password files, including a wrong one
assible-vault view "$@" --vault-password-file vault-password --vault-password-file vault-password-wrong "${TEST_FILE}"

# view with multiple vault-password files, including a wrong one, using vault-id
assible-vault view "$@" --vault-id vault-password --vault-id vault-password-wrong "${TEST_FILE}"

# And with the password files specified in a different order
assible-vault view "$@" --vault-password-file vault-password-wrong --vault-password-file vault-password "${TEST_FILE}"

# And with the password files specified in a different order, using vault-id
assible-vault view "$@" --vault-id vault-password-wrong --vault-id vault-password "${TEST_FILE}"

# And with the password files specified in a different order, using --vault-id and non default vault_ids
assible-vault view "$@" --vault-id test_vault_id@vault-password-wrong --vault-id test_vault_id@vault-password "${TEST_FILE}"

assible-vault decrypt "$@" --vault-password-file vault-password "${TEST_FILE}"

# encrypt it, using a vault_id so we write a 1.2 format file
assible-vault encrypt "$@" --vault-id test_vault_1_2@vault-password "${TEST_FILE_1_2}"

assible-vault view "$@" --vault-id vault-password "${TEST_FILE_1_2}"
assible-vault view "$@" --vault-id test_vault_1_2@vault-password "${TEST_FILE_1_2}"

# view with multiple vault-password files, including a wrong one
assible-vault view "$@" --vault-id vault-password --vault-id wrong_password@vault-password-wrong "${TEST_FILE_1_2}"

# And with the password files specified in a different order, using vault-id
assible-vault view "$@" --vault-id vault-password-wrong --vault-id vault-password "${TEST_FILE_1_2}"

# And with the password files specified in a different order, using --vault-id and non default vault_ids
assible-vault view "$@" --vault-id test_vault_id@vault-password-wrong --vault-id test_vault_id@vault-password "${TEST_FILE_1_2}"

assible-vault decrypt "$@" --vault-id test_vault_1_2@vault-password "${TEST_FILE_1_2}"

# multiple vault passwords
assible-vault view "$@" --vault-password-file vault-password --vault-password-file vault-password-wrong format_1_1_AES256.yml

# multiple vault passwords, --vault-id
assible-vault view "$@" --vault-id test_vault_id@vault-password --vault-id test_vault_id@vault-password-wrong format_1_1_AES256.yml

# encrypt it, with password from password script
assible-vault encrypt "$@" --vault-password-file password-script.py "${TEST_FILE}"

assible-vault view "$@" --vault-password-file password-script.py "${TEST_FILE}"

assible-vault decrypt "$@" --vault-password-file password-script.py "${TEST_FILE}"

# encrypt it, with password from password script
assible-vault encrypt "$@" --vault-id test_vault_id@password-script.py "${TEST_FILE}"

assible-vault view "$@" --vault-id test_vault_id@password-script.py "${TEST_FILE}"

assible-vault decrypt "$@" --vault-id test_vault_id@password-script.py "${TEST_FILE}"

# new password file for rekeyed file
NEW_VAULT_PASSWORD="${MYTMPDIR}/new-vault-password"
echo "newpassword" > "${NEW_VAULT_PASSWORD}"

assible-vault encrypt "$@" --vault-password-file vault-password "${TEST_FILE}"

assible-vault rekey "$@" --vault-password-file vault-password --new-vault-password-file "${NEW_VAULT_PASSWORD}" "${TEST_FILE}"

# --new-vault-password-file and --new-vault-id should cause options error
assible-vault rekey "$@" --vault-password-file vault-password --new-vault-id=foobar --new-vault-password-file "${NEW_VAULT_PASSWORD}" "${TEST_FILE}" && :
WRONG_RC=$?
echo "rc was $WRONG_RC (2 is expected)"
[ $WRONG_RC -eq 2 ]

assible-vault view "$@" --vault-password-file "${NEW_VAULT_PASSWORD}" "${TEST_FILE}"

# view file with unicode in filename
assible-vault view "$@" --vault-password-file vault-password vault-café.yml

# view with old password file and new password file
assible-vault view "$@" --vault-password-file "${NEW_VAULT_PASSWORD}" --vault-password-file vault-password "${TEST_FILE}"

# view with old password file and new password file, different order
assible-vault view "$@" --vault-password-file vault-password --vault-password-file "${NEW_VAULT_PASSWORD}" "${TEST_FILE}"

# view with old password file and new password file and another wrong
assible-vault view "$@" --vault-password-file "${NEW_VAULT_PASSWORD}" --vault-password-file vault-password-wrong --vault-password-file vault-password "${TEST_FILE}"

# view with old password file and new password file and another wrong, using --vault-id
assible-vault view "$@" --vault-id "tmp_new_password@${NEW_VAULT_PASSWORD}" --vault-id wrong_password@vault-password-wrong --vault-id myorg@vault-password "${TEST_FILE}"

assible-vault decrypt "$@" --vault-password-file "${NEW_VAULT_PASSWORD}" "${TEST_FILE}"

# reading/writing to/from stdin/stdin  (See https://github.com/assible/assible/issues/23567)
assible-vault encrypt "$@" --vault-password-file "${VAULT_PASSWORD_FILE}" --output="${TEST_FILE_OUTPUT}" < "${TEST_FILE}"
OUTPUT=$(assible-vault decrypt "$@" --vault-password-file "${VAULT_PASSWORD_FILE}" --output=- < "${TEST_FILE_OUTPUT}")
echo "${OUTPUT}" | grep 'This is a test file'

OUTPUT_DASH=$(assible-vault decrypt "$@" --vault-password-file "${VAULT_PASSWORD_FILE}" --output=- "${TEST_FILE_OUTPUT}")
echo "${OUTPUT_DASH}" | grep 'This is a test file'

OUTPUT_DASH_SPACE=$(assible-vault decrypt "$@" --vault-password-file "${VAULT_PASSWORD_FILE}" --output - "${TEST_FILE_OUTPUT}")
echo "${OUTPUT_DASH_SPACE}" | grep 'This is a test file'


# test using an empty vault password file
assible-vault view "$@" --vault-password-file empty-password format_1_1_AES256.yml && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]

assible-vault view "$@" --vault-id=empty@empty-password --vault-password-file empty-password format_1_1_AES256.yml && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]

echo 'foo' > some_file.txt
assible-vault encrypt "$@" --vault-password-file empty-password some_file.txt && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]


assible-vault encrypt_string "$@" --vault-password-file "${NEW_VAULT_PASSWORD}" "a test string"

# Test with multiple vault password files
# https://github.com/assible/assible/issues/57172
env ASSIBLE_VAULT_PASSWORD_FILE=vault-password assible-vault encrypt_string "$@" --vault-password-file "${NEW_VAULT_PASSWORD}" --encrypt-vault-id default "a test string"

assible-vault encrypt_string "$@" --vault-password-file "${NEW_VAULT_PASSWORD}" --name "blippy" "a test string names blippy"

assible-vault encrypt_string "$@" --vault-id "${NEW_VAULT_PASSWORD}" "a test string"

assible-vault encrypt_string "$@" --vault-id "${NEW_VAULT_PASSWORD}" --name "blippy" "a test string names blippy"


# from stdin
assible-vault encrypt_string "$@" --vault-password-file "${NEW_VAULT_PASSWORD}" < "${TEST_FILE}"

assible-vault encrypt_string "$@" --vault-password-file "${NEW_VAULT_PASSWORD}" --stdin-name "the_var_from_stdin" < "${TEST_FILE}"

# write to file
assible-vault encrypt_string "$@" --vault-password-file "${NEW_VAULT_PASSWORD}" --name "blippy" "a test string names blippy" --output "${MYTMPDIR}/enc_string_test_file"

# test assible-vault edit with a faux editor
assible-vault encrypt "$@" --vault-password-file vault-password "${TEST_FILE_EDIT}"

# edit a 1.1 format with no vault-id, should stay 1.1
EDITOR=./faux-editor.py assible-vault edit "$@" --vault-password-file vault-password "${TEST_FILE_EDIT}"
head -1 "${TEST_FILE_EDIT}" | grep "${FORMAT_1_1_HEADER}"

# edit a 1.1 format with vault-id, should stay 1.1
cat "${TEST_FILE_EDIT}"
EDITOR=./faux-editor.py assible-vault edit "$@" --vault-id vault_password@vault-password "${TEST_FILE_EDIT}"
cat "${TEST_FILE_EDIT}"
head -1 "${TEST_FILE_EDIT}" | grep "${FORMAT_1_1_HEADER}"

assible-vault encrypt "$@" --vault-id vault_password@vault-password "${TEST_FILE_EDIT2}"

# verify that we aren't prompted for a new vault password on edit if we are running interactively (ie, with prompts)
# have to use setsid nd --ask-vault-pass to force a prompt to simulate.
# See https://github.com/assible/assible/issues/35834
setsid sh -c 'tty; echo password |assible-vault edit --ask-vault-pass vault_test.yml' < /dev/null > log 2>&1 && :
grep  'New Vault password' log && :
WRONG_RC=$?
echo "The stdout log had 'New Vault password' in it and it is not supposed to. rc of grep was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]

# edit a 1.2 format with vault id, should keep vault id and 1.2 format
EDITOR=./faux-editor.py assible-vault edit "$@" --vault-id vault_password@vault-password "${TEST_FILE_EDIT2}"
head -1 "${TEST_FILE_EDIT2}" | grep "${FORMAT_1_2_HEADER};vault_password"

# edit a 1.2 file with no vault-id, should keep vault id and 1.2 format
EDITOR=./faux-editor.py assible-vault edit "$@" --vault-password-file vault-password "${TEST_FILE_EDIT2}"
head -1 "${TEST_FILE_EDIT2}" | grep "${FORMAT_1_2_HEADER};vault_password"

# encrypt with a password from a vault encrypted password file and multiple vault-ids
# should fail because we dont know which vault id to use to encrypt with
assible-vault encrypt "$@" --vault-id vault-password --vault-id encrypted-vault-password "${TEST_FILE_ENC_PASSWORD}" && :
WRONG_RC=$?
echo "rc was $WRONG_RC (5 is expected)"
[ $WRONG_RC -eq 5 ]


# encrypt with a password from a vault encrypted password file and multiple vault-ids
# but this time specify with --encrypt-vault-id, but specifying vault-id names (instead of default)
# assible-vault encrypt "$@" --vault-id from_vault_password@vault-password --vault-id from_encrypted_vault_password@encrypted-vault-password --encrypt-vault-id from_encrypted_vault_password "${TEST_FILE(_ENC_PASSWORD}"

# try to view the file encrypted with the vault-password we didnt specify
# to verify we didnt choose the wrong vault-id
# assible-vault view "$@" --vault-id vault-password "${TEST_FILE_ENC_PASSWORD}" && :
# WRONG_RC=$?
# echo "rc was $WRONG_RC (1 is expected)"
# [ $WRONG_RC -eq 1 ]

assible-vault encrypt "$@" --vault-id vault-password "${TEST_FILE_ENC_PASSWORD}"

# view the file encrypted with a password from a vault encrypted password file
assible-vault view "$@" --vault-id vault-password --vault-id encrypted-vault-password "${TEST_FILE_ENC_PASSWORD}"

# try to view the file encrypted with a password from a vault encrypted password file but without the password to the password file.
# This should fail with an
assible-vault view "$@" --vault-id encrypted-vault-password "${TEST_FILE_ENC_PASSWORD}" && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]


# test playbooks using vaulted files
assible-playbook test_vault.yml          -i ../../inventory -v "$@" --vault-password-file vault-password --list-tasks
assible-playbook test_vault.yml          -i ../../inventory -v "$@" --vault-password-file vault-password --list-hosts
assible-playbook test_vault.yml          -i ../../inventory -v "$@" --vault-password-file vault-password --syntax-check
assible-playbook test_vault.yml          -i ../../inventory -v "$@" --vault-password-file vault-password
assible-playbook test_vault_embedded.yml -i ../../inventory -v "$@" --vault-password-file vault-password --syntax-check
assible-playbook test_vault_embedded.yml -i ../../inventory -v "$@" --vault-password-file vault-password
assible-playbook test_vaulted_inventory.yml -i vaulted.inventory -v "$@" --vault-password-file vault-password
assible-playbook test_vaulted_template.yml -i ../../inventory -v "$@" --vault-password-file vault-password

# test using --vault-pass-file option
assible-playbook test_vault.yml          -i ../../inventory -v "$@" --vault-pass-file vault-password

# install TOML for parse toml inventory
# test playbooks using vaulted files(toml)
pip install toml
assible-vault encrypt  ./inventory.toml -v "$@" --vault-password-file=./vault-password
assible-playbook test_vaulted_inventory_toml.yml -i ./inventory.toml -v "$@" --vault-password-file vault-password
assible-vault decrypt  ./inventory.toml -v "$@" --vault-password-file=./vault-password

# test a playbook with a host_var whose value is non-ascii utf8 (see https://github.com/assible/assible/issues/37258)
assible-playbook -i ../../inventory -v "$@" --vault-id vault-password test_vaulted_utf8_value.yml

# test with password from password script
assible-playbook test_vault.yml          -i ../../inventory -v "$@" --vault-password-file password-script.py
assible-playbook test_vault_embedded.yml -i ../../inventory -v "$@" --vault-password-file password-script.py

# with multiple password files
assible-playbook test_vault.yml          -i ../../inventory -v "$@" --vault-password-file vault-password --vault-password-file vault-password-wrong
assible-playbook test_vault.yml          -i ../../inventory -v "$@" --vault-password-file vault-password-wrong --vault-password-file vault-password

assible-playbook test_vault_embedded.yml -i ../../inventory -v "$@" --vault-password-file vault-password --vault-password-file vault-password-wrong --syntax-check
assible-playbook test_vault_embedded.yml -i ../../inventory -v "$@" --vault-password-file vault-password-wrong --vault-password-file vault-password

# test with a default vault password file set in config
ASSIBLE_VAULT_PASSWORD_FILE=vault-password assible-playbook test_vault_embedded.yml -i ../../inventory -v "$@" --vault-password-file vault-password-wrong

# test using vault_identity_list config
ASSIBLE_VAULT_IDENTITY_LIST='wrong-password@vault-password-wrong,default@vault-password' assible-playbook test_vault.yml -i ../../inventory -v "$@"

# test that we can have a vault encrypted yaml file that includes embedded vault vars
# that were encrypted with a different vault secret
assible-playbook test_vault_file_encrypted_embedded.yml -i ../../inventory "$@" --vault-id encrypted_file_encrypted_var_password --vault-id vault-password

# with multiple password files, --vault-id, ordering
assible-playbook test_vault.yml          -i ../../inventory -v "$@" --vault-id vault-password --vault-id vault-password-wrong
assible-playbook test_vault.yml          -i ../../inventory -v "$@" --vault-id vault-password-wrong --vault-id vault-password

assible-playbook test_vault_embedded.yml -i ../../inventory -v "$@" --vault-id vault-password --vault-id vault-password-wrong --syntax-check
assible-playbook test_vault_embedded.yml -i ../../inventory -v "$@" --vault-id vault-password-wrong --vault-id vault-password

# test with multiple password files, including a script, and a wrong password
assible-playbook test_vault_embedded.yml -i ../../inventory -v "$@" --vault-password-file vault-password-wrong --vault-password-file password-script.py --vault-password-file vault-password

# test with multiple password files, including a script, and a wrong password, and a mix of --vault-id and --vault-password-file
assible-playbook test_vault_embedded.yml -i ../../inventory -v "$@" --vault-password-file vault-password-wrong --vault-id password-script.py --vault-id vault-password

# test with multiple password files, including a script, and a wrong password, and a mix of --vault-id and --vault-password-file
assible-playbook test_vault_embedded_ids.yml -i ../../inventory -v "$@" \
	--vault-password-file vault-password-wrong \
	--vault-id password-script.py --vault-id example1@example1_password \
	--vault-id example2@example2_password --vault-password-file example3_password \
	--vault-id vault-password

# with wrong password
assible-playbook test_vault.yml          -i ../../inventory -v "$@" --vault-password-file vault-password-wrong && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]

# with multiple wrong passwords
assible-playbook test_vault.yml          -i ../../inventory -v "$@" --vault-password-file vault-password-wrong --vault-password-file vault-password-wrong && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]

# with wrong password, --vault-id
assible-playbook test_vault.yml          -i ../../inventory -v "$@" --vault-id vault-password-wrong && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]

# with multiple wrong passwords with --vault-id
assible-playbook test_vault.yml          -i ../../inventory -v "$@" --vault-id vault-password-wrong --vault-id vault-password-wrong && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]

# with multiple wrong passwords with --vault-id
assible-playbook test_vault.yml          -i ../../inventory -v "$@" --vault-id wrong1@vault-password-wrong --vault-id wrong2@vault-password-wrong && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]

# with empty password file
assible-playbook test_vault.yml           -i ../../inventory -v "$@" --vault-id empty@empty-password && :
WRONG_RC=$?
echo "rc was $WRONG_RC (1 is expected)"
[ $WRONG_RC -eq 1 ]

# test invalid format ala https://github.com/assible/assible/issues/28038
EXPECTED_ERROR='Vault format unhexlify error: Non-hexadecimal digit found'
assible-playbook "$@" -i invalid_format/inventory --vault-id invalid_format/vault-secret invalid_format/broken-host-vars-tasks.yml 2>&1 | grep "${EXPECTED_ERROR}"

EXPECTED_ERROR='Vault format unhexlify error: Odd-length string'
assible-playbook "$@" -i invalid_format/inventory --vault-id invalid_format/vault-secret invalid_format/broken-group-vars-tasks.yml 2>&1 | grep "${EXPECTED_ERROR}"

# Run playbook with vault file with unicode in filename (https://github.com/assible/assible/issues/50316)
assible-playbook -i ../../inventory -v "$@" --vault-password-file vault-password test_utf8_value_in_filename.yml

# Ensure we don't leave unencrypted temp files dangling
assible-playbook -v "$@" --vault-password-file vault-password test_dangling_temp.yml

assible-playbook "$@" --vault-password-file vault-password single_vault_as_string.yml