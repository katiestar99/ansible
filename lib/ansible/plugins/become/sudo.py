# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Assible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    name: sudo
    short_description: Substitute User DO
    description:
        - This become plugins allows your remote/login user to execute commands as another user via the sudo utility.
    author: assible (@core)
    version_added: "2.8"
    options:
        become_user:
            description: User you 'become' to execute the task
            default: root
            ini:
              - section: privilege_escalation
                key: become_user
              - section: sudo_become_plugin
                key: user
            vars:
              - name: assible_become_user
              - name: assible_sudo_user
            env:
              - name: ASSIBLE_BECOME_USER
              - name: ASSIBLE_SUDO_USER
        become_exe:
            description: Sudo executable
            default: sudo
            ini:
              - section: privilege_escalation
                key: become_exe
              - section: sudo_become_plugin
                key: executable
            vars:
              - name: assible_become_exe
              - name: assible_sudo_exe
            env:
              - name: ASSIBLE_BECOME_EXE
              - name: ASSIBLE_SUDO_EXE
        become_flags:
            description: Options to pass to sudo
            default: -H -S -n
            ini:
              - section: privilege_escalation
                key: become_flags
              - section: sudo_become_plugin
                key: flags
            vars:
              - name: assible_become_flags
              - name: assible_sudo_flags
            env:
              - name: ASSIBLE_BECOME_FLAGS
              - name: ASSIBLE_SUDO_FLAGS
        become_pass:
            description: Password to pass to sudo
            required: False
            vars:
              - name: assible_become_password
              - name: assible_become_pass
              - name: assible_sudo_pass
            env:
              - name: ASSIBLE_BECOME_PASS
              - name: ASSIBLE_SUDO_PASS
            ini:
              - section: sudo_become_plugin
                key: password
"""


from assible.plugins.become import BecomeBase


class BecomeModule(BecomeBase):

    name = 'sudo'

    # messages for detecting prompted password issues
    fail = ('Sorry, try again.',)
    missing = ('Sorry, a password is required to run sudo', 'sudo: a password is required')

    def build_become_command(self, cmd, shell):
        super(BecomeModule, self).build_become_command(cmd, shell)

        if not cmd:
            return cmd

        becomecmd = self.get_option('become_exe') or self.name

        flags = self.get_option('become_flags') or ''
        prompt = ''
        if self.get_option('become_pass'):
            self.prompt = '[sudo via assible, key=%s] password:' % self._id
            if flags:  # this could be simplified, but kept as is for now for backwards string matching
                flags = flags.replace('-n', '')
            prompt = '-p "%s"' % (self.prompt)

        user = self.get_option('become_user') or ''
        if user:
            user = '-u %s' % (user)

        return ' '.join([becomecmd, flags, prompt, user, self._build_success_command(cmd, shell)])
