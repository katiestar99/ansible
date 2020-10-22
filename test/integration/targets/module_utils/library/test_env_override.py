#!/usr/bin/python
# Most of these names are only available via PluginLoader so pylint doesn't
# know they exist
# pylint: disable=no-name-in-module
from __future__ import absolute_import, division, print_function
__metaclass__ = type

from assible.module_utils.basic import AssibleModule
from assible.module_utils.json_utils import data
from assible.module_utils.mork import data as mork_data

results = {"json_utils": data, "mork": mork_data}

AssibleModule(argument_spec=dict()).exit_json(**results)
