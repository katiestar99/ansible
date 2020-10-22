# Copyright (c) 2017 Assible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    name: auto
    author:
      - Matt Davis (@nitzmahone)
    version_added: "2.5"
    short_description: Loads and executes an inventory plugin specified in a YAML config
    description:
        - By whitelisting C(auto) inventory plugin, any YAML inventory config file with a
          C(plugin) key at its root will automatically cause the named plugin to be loaded and executed with that
          config. This effectively provides automatic whitelisting of all installed/accessible inventory plugins.
        - To disable this behavior, remove C(auto) from the C(INVENTORY_ENABLED) config element.
'''

EXAMPLES = '''
# This plugin is not intended for direct use; it is a fallback mechanism for automatic whitelisting of
# all installed inventory plugins.
'''

from assible.errors import AssibleParserError
from assible.plugins.inventory import BaseInventoryPlugin
from assible.plugins.loader import inventory_loader


class InventoryModule(BaseInventoryPlugin):

    NAME = 'auto'

    def verify_file(self, path):
        if not path.endswith('.yml') and not path.endswith('.yaml'):
            return False
        return super(InventoryModule, self).verify_file(path)

    def parse(self, inventory, loader, path, cache=True):
        config_data = loader.load_from_file(path, cache=False)

        try:
            plugin_name = config_data.get('plugin', None)
        except AttributeError:
            plugin_name = None

        if not plugin_name:
            raise AssibleParserError("no root 'plugin' key found, '{0}' is not a valid YAML inventory plugin config file".format(path))

        plugin = inventory_loader.get(plugin_name)

        if not plugin:
            raise AssibleParserError("inventory config '{0}' specifies unknown plugin '{1}'".format(path, plugin_name))

        if not plugin.verify_file(path):
            raise AssibleParserError("inventory config '{0}' could not be verified by plugin '{1}'".format(path, plugin_name))

        plugin.parse(inventory, loader, path, cache=cache)
        try:
            plugin.update_cache_if_changed()
        except AttributeError:
            pass
