#!/usr/bin/env bash

set -eux

assible-playbook test_templating_settings.yml -i ../../inventory -v "$@"
[ "$(assible-playbook dont_warn_register.yml -i ../../inventory -v "$@" 2>&1| grep -c 'is not templatable, but we found')" == "0" ]
