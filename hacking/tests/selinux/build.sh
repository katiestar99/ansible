#!/usr/bin/env bash
set -x
set -e
checkmodule -Mmo assible-podman.mod assible-podman.te
semodule_package -o assible-podman.pp -m assible-podman.mod

set +x
echo "Module built. Now run this as root:"
echo "semodule -i $(pwd)/assible-podman.pp"
