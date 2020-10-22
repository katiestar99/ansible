# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Assible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """become: enable
short_description: Switch to elevated permissions on a network device
description:
- This become plugins allows elevated permissions on a remote network device.
author: assible (@core)
options:
  become_pass:
    description: password
    ini:
    - section: enable_become_plugin
      key: password
    vars:
    - name: assible_become_password
    - name: assible_become_pass
    - name: assible_enable_pass
    env:
    - name: ASSIBLE_BECOME_PASS
    - name: ASSIBLE_ENABLE_PASS
notes:
- enable is really implemented in the network connection handler and as such can only
  be used with network connections.
- This plugin ignores the 'become_exe' and 'become_user' settings as it uses an API
  and not an executable.
"""

from assible.plugins.become import BecomeBase


class BecomeModule(BecomeBase):

    name = "assible.netcommon.enable"

    def build_become_command(self, cmd, shell):
        # enable is implemented inside the network connection plugins
        return cmd
