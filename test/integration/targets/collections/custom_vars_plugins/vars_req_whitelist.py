# Copyright 2019 RedHat, inc
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
#############################################
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    vars: vars_req_whitelist
    version_added: "2.10"
    short_description: load host and group vars
    description: test loading host and group vars from a collection
    options:
      stage:
        choices: ['all', 'inventory', 'task']
        type: str
        ini:
          - key: stage
            section: vars_req_whitelist
        env:
          - name: ASSIBLE_VARS_PLUGIN_STAGE
'''

from assible.plugins.vars import BaseVarsPlugin


class VarsModule(BaseVarsPlugin):

    REQUIRES_WHITELIST = True

    def get_vars(self, loader, path, entities, cache=True):
        super(VarsModule, self).get_vars(loader, path, entities)
        return {'whitelisted': True, 'collection': False}
