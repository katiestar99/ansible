#!/usr/bin/env python

"""
This script generated test_cases for test_distribution_version.py.

To do so it outputs the relevant files from /etc/*release, the output of distro.linux_distribution()
and the current assible_facts regarding the distribution version.

This assumes a working assible version in the path.
"""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import os.path
import platform
import subprocess
import sys

from assible.module_utils import distro
from assible.module_utils._text import to_text


filelist = [
    '/etc/oracle-release',
    '/etc/slackware-version',
    '/etc/redhat-release',
    '/etc/vmware-release',
    '/etc/openwrt_release',
    '/etc/system-release',
    '/etc/alpine-release',
    '/etc/release',
    '/etc/arch-release',
    '/etc/os-release',
    '/etc/SuSE-release',
    '/etc/gentoo-release',
    '/etc/os-release',
    '/etc/lsb-release',
    '/etc/altlinux-release',
    '/etc/os-release',
    '/etc/coreos/update.conf',
    '/etc/flatcar/update.conf',
    '/usr/lib/os-release',
]

fcont = {}

for f in filelist:
    if os.path.exists(f):
        s = os.path.getsize(f)
        if s > 0 and s < 10000:
            with open(f) as fh:
                fcont[f] = fh.read()

dist = distro.linux_distribution(full_distribution_name=False)

facts = ['distribution', 'distribution_version', 'distribution_release', 'distribution_major_version', 'os_family']

try:
    b_assible_out = subprocess.check_output(
        ['assible', 'localhost', '-m', 'setup'])
except subprocess.CalledProcessError as e:
    print("ERROR: assible run failed, output was: \n")
    print(e.output)
    sys.exit(e.returncode)

assible_out = to_text(b_assible_out)
parsed = json.loads(assible_out[assible_out.index('{'):])
assible_facts = {}
for fact in facts:
    try:
        assible_facts[fact] = parsed['assible_facts']['assible_' + fact]
    except Exception:
        assible_facts[fact] = "N/A"

nicename = assible_facts['distribution'] + ' ' + assible_facts['distribution_version']

output = {
    'name': nicename,
    'distro': {
        'codename': distro.codename(),
        'id': distro.id(),
        'name': distro.name(),
        'version': distro.version(),
        'version_best': distro.version(best=True),
        'lsb_release_info': distro.lsb_release_info(),
        'os_release_info': distro.os_release_info(),
    },
    'input': fcont,
    'platform.dist': dist,
    'result': assible_facts,
}

system = platform.system()
if system != 'Linux':
    output['platform.system'] = system

release = platform.release()
if release:
    output['platform.release'] = release

print(json.dumps(output, indent=4))
