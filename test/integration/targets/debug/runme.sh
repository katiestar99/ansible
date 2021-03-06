#!/usr/bin/env bash

set -eux

trap 'rm -f out' EXIT

assible-playbook main.yml -i ../../inventory | tee out
for i in 1 2 3; do
  grep "ok: \[localhost\] => (item=$i)" out
  grep "\"item\": $i" out
done
