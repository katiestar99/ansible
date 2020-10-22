# Copyright (c) 2017 Assible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json

import pytest

from assible.module_utils.six import string_types
from assible.module_utils._text import to_bytes
from assible.module_utils.common._collections_compat import MutableMapping


@pytest.fixture
def patch_assible_module(request, mocker):
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
        raise Exception('Malformed data to the patch_assible_module pytest fixture')

    mocker.patch('assible.module_utils.basic._ASSIBLE_ARGS', to_bytes(args))
