from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
from assible.module_utils import basic
from assible.module_utils.basic import _load_params, AssibleModule


def do_echo():
    p = _load_params()
    d = json.loads(basic._ASSIBLE_ARGS)
    d['ASSIBLE_MODULE_ARGS'] = {}
    basic._ASSIBLE_ARGS = json.dumps(d).encode('utf-8')
    module = AssibleModule(argument_spec={})
    module.exit_json(args_in=p)
