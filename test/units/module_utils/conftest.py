# Copyright (c) 2017 Assible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import sys
from io import BytesIO

import pytest

import assible.module_utils.basic
from assible.module_utils.six import PY3, string_types
from assible.module_utils._text import to_bytes
from assible.module_utils.common._collections_compat import MutableMapping


@pytest.fixture
def stdin(mocker, request):
    old_args = assible.module_utils.basic._ASSIBLE_ARGS
    assible.module_utils.basic._ASSIBLE_ARGS = None
    old_argv = sys.argv
    sys.argv = ['assible_unittest']

    if isinstance(request.param, string_types):
        args = request.param
    elif isinstance(request.param, MutableMapping):
        if 'ASSIBLE_MODULE_ARGS' not in request.param:
            request.param = {'ASSIBLE_MODULE_ARGS': request.param}
        if '_assible_remote_tmp' not in request.param['ASSIBLE_MODULE_ARGS']:
            request.param['ASSIBLE_MODULE_ARGS']['_assible_remote_tmp'] = '/tmp'
        if '_assible_keep_remote_files' not in request.param['ASSIBLE_MODULE_ARGS']:
            request.param['ASSIBLE_MODULE_ARGS']['_assible_keep_remote_files'] = False
        args = json.dumps(request.param)
    else:
        raise Exception('Malformed data to the stdin pytest fixture')

    fake_stdin = BytesIO(to_bytes(args, errors='surrogate_or_strict'))
    if PY3:
        mocker.patch('assible.module_utils.basic.sys.stdin', mocker.MagicMock())
        mocker.patch('assible.module_utils.basic.sys.stdin.buffer', fake_stdin)
    else:
        mocker.patch('assible.module_utils.basic.sys.stdin', fake_stdin)

    yield fake_stdin

    assible.module_utils.basic._ASSIBLE_ARGS = old_args
    sys.argv = old_argv


@pytest.fixture
def am(stdin, request):
    old_args = assible.module_utils.basic._ASSIBLE_ARGS
    assible.module_utils.basic._ASSIBLE_ARGS = None
    old_argv = sys.argv
    sys.argv = ['assible_unittest']

    argspec = {}
    if hasattr(request, 'param'):
        if isinstance(request.param, dict):
            argspec = request.param

    am = assible.module_utils.basic.AssibleModule(
        argument_spec=argspec,
    )
    am._name = 'assible_unittest'

    yield am

    assible.module_utils.basic._ASSIBLE_ARGS = old_args
    sys.argv = old_argv
