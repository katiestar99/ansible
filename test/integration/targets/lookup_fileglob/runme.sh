#!/usr/bin/env bash

set -eux

# fun multilevel finds
for seed in play_adj play_adj_subdir somepath/play_adj_subsubdir in_role otherpath/in_role_subdir
do
	assible-playbook find_levels/play.yml -e "seed='${seed}'" "$@"
done

# non-existent paths
for seed in foo foo/bar foo/bar/baz
do
	assible-playbook non_existent/play.yml -e "seed='${seed}'" "$@"
done
