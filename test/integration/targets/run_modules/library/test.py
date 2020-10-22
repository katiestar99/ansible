#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from assible.module_utils.basic import AssibleModule

module = AssibleModule(argument_spec=dict())

module.exit_json(**{'tempdir': module._remote_tmp})
