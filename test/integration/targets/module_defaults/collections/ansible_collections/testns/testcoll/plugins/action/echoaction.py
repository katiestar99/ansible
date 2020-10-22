from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from assible.plugins.action import ActionBase


class ActionModule(ActionBase):
    TRANSFERS_FILES = False
    _VALID_ARGS = frozenset()

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(None, task_vars)

        result = dict(changed=False, args_in=self._task.args)

        return result
