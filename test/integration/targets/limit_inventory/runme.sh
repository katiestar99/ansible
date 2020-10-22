#!/usr/bin/env bash

set -eux

trap 'echo "Host pattern limit test failed"' ERR

# https://github.com/assible/assible/issues/61964

# These tests should return all hosts
assible -i hosts.yml all --limit ,, --list-hosts | tee out ; grep -q 'hosts (3)' out
assible -i hosts.yml ,, --list-hosts | tee out ; grep -q 'hosts (3)' out
assible -i hosts.yml , --list-hosts | tee out ; grep -q 'hosts (3)' out
assible -i hosts.yml all --limit , --list-hosts | tee out ; grep -q 'hosts (3)' out
assible -i hosts.yml all --limit '' --list-hosts | tee out ; grep -q 'hosts (3)' out


# Only one host
assible -i hosts.yml all --limit ,,host1 --list-hosts | tee out ; grep -q 'hosts (1)' out
assible -i hosts.yml ,,host1 --list-hosts | tee out ; grep -q 'hosts (1)' out

assible -i hosts.yml all --limit host1,, --list-hosts | tee out ; grep -q 'hosts (1)' out
assible -i hosts.yml host1,, --list-hosts | tee out ; grep -q 'hosts (1)' out


# Only two hosts
assible -i hosts.yml all --limit host1,,host3 --list-hosts | tee out ; grep -q 'hosts (2)' out
assible -i hosts.yml host1,,host3 --list-hosts | tee out ; grep -q 'hosts (2)' out

assible -i hosts.yml all --limit 'host1, ,    ,host3' --list-hosts | tee out ; grep -q 'hosts (2)' out
assible -i hosts.yml 'host1, ,    ,host3' --list-hosts | tee out ; grep -q 'hosts (2)' out

