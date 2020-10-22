#!/usr/bin/env bash

set -eux

# ignore empty env var and use default
# shellcheck disable=SC1007
ASSIBLE_TIMEOUT= assible -m ping testhost -i ../../inventory "$@"

# env var is wrong type, this should be a fatal error pointing at the setting
ASSIBLE_TIMEOUT='lola' assible -m ping testhost -i ../../inventory "$@" 2>&1|grep 'Invalid type for configuration option setting: DEFAULT_TIMEOUT'

# https://github.com/assible/assible/issues/69577                                                         
ASSIBLE_REMOTE_TMP="$HOME/.assible/directory_with_no_space"  assible -m ping testhost -i ../../inventory "$@" 
                                                                                                          
ASSIBLE_REMOTE_TMP="$HOME/.assible/directory with space"  assible -m ping testhost -i ../../inventory "$@"