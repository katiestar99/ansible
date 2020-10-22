#!/usr/bin/python
from __future__ import absolute_import, division, print_function
__metaclass__ = type

from assible.module_utils.basic import AssibleModule
from assible.module_utils.facts import data

results = {"data": data}

AssibleModule(argument_spec=dict()).exit_json(**results)
