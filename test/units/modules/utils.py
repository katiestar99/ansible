from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json

from units.compat import unittest
from units.compat.mock import patch
from assible.module_utils import basic
from assible.module_utils._text import to_bytes


def set_module_args(args):
    if '_assible_remote_tmp' not in args:
        args['_assible_remote_tmp'] = '/tmp'
    if '_assible_keep_remote_files' not in args:
        args['_assible_keep_remote_files'] = False

    args = json.dumps({'ASSIBLE_MODULE_ARGS': args})
    basic._ASSIBLE_ARGS = to_bytes(args)


class AssibleExitJson(Exception):
    pass


class AssibleFailJson(Exception):
    pass


def exit_json(*args, **kwargs):
    if 'changed' not in kwargs:
        kwargs['changed'] = False
    raise AssibleExitJson(kwargs)


def fail_json(*args, **kwargs):
    kwargs['failed'] = True
    raise AssibleFailJson(kwargs)


class ModuleTestCase(unittest.TestCase):

    def setUp(self):
        self.mock_module = patch.multiple(basic.AssibleModule, exit_json=exit_json, fail_json=fail_json)
        self.mock_module.start()
        self.mock_sleep = patch('time.sleep')
        self.mock_sleep.start()
        set_module_args({})
        self.addCleanup(self.mock_module.stop)
        self.addCleanup(self.mock_sleep.stop)
