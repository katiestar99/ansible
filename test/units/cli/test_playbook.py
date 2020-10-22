# (c) 2016, Adrian Likins <alikins@redhat.com>
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

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from units.compat import unittest
from units.mock.loader import DictDataLoader

from assible import context
from assible.inventory.manager import InventoryManager
from assible.vars.manager import VariableManager

from assible.cli.playbook import PlaybookCLI


class TestPlaybookCLI(unittest.TestCase):
    def test_flush_cache(self):
        cli = PlaybookCLI(args=["assible-playbook", "--flush-cache", "foobar.yml"])
        cli.parse()
        self.assertTrue(context.CLIARGS['flush_cache'])

        variable_manager = VariableManager()
        fake_loader = DictDataLoader({'foobar.yml': ""})
        inventory = InventoryManager(loader=fake_loader, sources='testhost,')

        variable_manager.set_host_facts('testhost', {'canary': True})
        self.assertTrue('testhost' in variable_manager._fact_cache)

        cli._flush_cache(inventory, variable_manager)
        self.assertFalse('testhost' in variable_manager._fact_cache)
