# -*- coding: utf-8 -*-
# (c) 2017 Toshio Kuratomi <tkuratomi@assible.com>
#
# This file is part of Assible
#
# Assible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Assible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Assible.  If not, see <http://www.gnu.org/licenses/>.

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pwd
import os

import pytest

from assible import constants
from assible.module_utils.six import StringIO
from assible.module_utils.six.moves import configparser
from assible.module_utils._text import to_text


@pytest.fixture
def cfgparser():
    CFGDATA = StringIO("""
[defaults]
defaults_one = 'data_defaults_one'

[level1]
level1_one = 'data_level1_one'
    """)
    p = configparser.ConfigParser()
    p.readfp(CFGDATA)
    return p


@pytest.fixture
def user():
    user = {}
    user['uid'] = os.geteuid()

    pwd_entry = pwd.getpwuid(user['uid'])
    user['username'] = pwd_entry.pw_name
    user['home'] = pwd_entry.pw_dir

    return user


@pytest.fixture
def cfg_file():
    data = '/assible/test/cfg/path'
    old_cfg_file = constants.CONFIG_FILE
    constants.CONFIG_FILE = os.path.join(data, 'assible.cfg')
    yield data

    constants.CONFIG_FILE = old_cfg_file


@pytest.fixture
def null_cfg_file():
    old_cfg_file = constants.CONFIG_FILE
    del constants.CONFIG_FILE
    yield

    constants.CONFIG_FILE = old_cfg_file


@pytest.fixture
def cwd():
    data = '/assible/test/cwd/'
    old_cwd = os.getcwd
    os.getcwd = lambda: data

    old_cwdu = None
    if hasattr(os, 'getcwdu'):
        old_cwdu = os.getcwdu
        os.getcwdu = lambda: to_text(data)

    yield data

    os.getcwd = old_cwd
    if hasattr(os, 'getcwdu'):
        os.getcwdu = old_cwdu
