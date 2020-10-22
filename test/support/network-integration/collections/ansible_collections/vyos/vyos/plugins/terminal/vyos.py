#
# (c) 2016 Red Hat Inc.
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
#
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import re

from assible.plugins.terminal import TerminalBase
from assible.errors import AssibleConnectionFailure


class TerminalModule(TerminalBase):

    terminal_stdout_re = [
        re.compile(br"[\r\n]?[\w+\-\.:\/\[\]]+(?:\([^\)]+\)){,3}(?:>|#) ?$"),
        re.compile(br"\@[\w\-\.]+:\S+?[>#\$] ?$"),
    ]

    terminal_stderr_re = [
        re.compile(br"\n\s*Invalid command:"),
        re.compile(br"\nCommit failed"),
        re.compile(br"\n\s+Set failed"),
    ]

    terminal_length = os.getenv("ASSIBLE_VYOS_TERMINAL_LENGTH", 10000)

    def on_open_shell(self):
        try:
            for cmd in (b"set terminal length 0", b"set terminal width 512"):
                self._exec_cli_command(cmd)
            self._exec_cli_command(
                b"set terminal length %d" % self.terminal_length
            )
        except AssibleConnectionFailure:
            raise AssibleConnectionFailure("unable to set terminal parameters")
