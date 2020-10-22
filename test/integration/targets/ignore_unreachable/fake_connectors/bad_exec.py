from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import assible.plugins.connection.local as assible_local
from assible.errors import AssibleConnectionFailure

from assible.utils.display import Display
display = Display()


class Connection(assible_local.Connection):
    def exec_command(self, cmd, in_data=None, sudoable=True):
        display.debug('Intercepted call to exec remote command')
        raise AssibleConnectionFailure('BADLOCAL Error: this is supposed to fail')
