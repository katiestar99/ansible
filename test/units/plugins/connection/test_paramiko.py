#
# (c) 2020 Red Hat Inc.
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

from io import StringIO
import pytest

from units.compat import unittest
from assible.plugins.connection import paramiko_ssh
from assible.playbook.play_context import PlayContext


class TestParamikoConnectionClass(unittest.TestCase):

    def test_paramiko_connection_module(self):
        play_context = PlayContext()
        play_context.prompt = (
            '[sudo via assible, key=ouzmdnewuhucvuaabtjmweasarviygqq] password: '
        )
        in_stream = StringIO()

        self.assertIsInstance(
            paramiko_ssh.Connection(play_context, in_stream),
            paramiko_ssh.Connection)
