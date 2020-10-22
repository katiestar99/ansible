# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Assible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import sys

import pytest

from assible import constants as C
from assible.cli.arguments import option_helpers as opt_help
from assible import __path__ as assible_path
from assible.release import __version__ as assible_version

if C.DEFAULT_MODULE_PATH is None:
    cpath = u'Default w/o overrides'
else:
    cpath = C.DEFAULT_MODULE_PATH

FAKE_PROG = u'assible-cli-test'
VERSION_OUTPUT = opt_help.version(prog=FAKE_PROG)


@pytest.mark.parametrize(
    'must_have', [
        FAKE_PROG + u' %s' % assible_version,
        u'config file = %s' % C.CONFIG_FILE,
        u'configured module search path = %s' % cpath,
        u'assible python module location = %s' % ':'.join(assible_path),
        u'assible collection location = %s' % ':'.join(C.COLLECTIONS_PATHS),
        u'executable location = ',
        u'python version = %s' % ''.join(sys.version.splitlines()),
    ]
)
def test_option_helper_version(must_have):
    assert must_have in VERSION_OUTPUT
