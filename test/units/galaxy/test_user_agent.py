# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Assible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import platform

from assible.galaxy import user_agent
from assible.module_utils.assible_release import __version__ as assible_version


def test_user_agent():
    res = user_agent.user_agent()
    assert res.startswith('assible-galaxy/%s' % assible_version)
    assert platform.system() in res
    assert 'python:' in res
