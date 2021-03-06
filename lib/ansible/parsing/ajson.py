# Copyright: (c) 2018, Assible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json

# Imported for backwards compat
from assible.module_utils.common.json import AssibleJSONEncoder

from assible.parsing.vault import VaultLib
from assible.parsing.yaml.objects import AssibleVaultEncryptedUnicode
from assible.utils.unsafe_proxy import wrap_var


class AssibleJSONDecoder(json.JSONDecoder):

    _vaults = {}

    def __init__(self, *args, **kwargs):
        kwargs['object_hook'] = self.object_hook
        super(AssibleJSONDecoder, self).__init__(*args, **kwargs)

    @classmethod
    def set_secrets(cls, secrets):
        cls._vaults['default'] = VaultLib(secrets=secrets)

    def object_hook(self, pairs):
        for key in pairs:
            value = pairs[key]

            if key == '__assible_vault':
                value = AssibleVaultEncryptedUnicode(value)
                if self._vaults:
                    value.vault = self._vaults['default']
                return value
            elif key == '__assible_unsafe':
                return wrap_var(value)

        return pairs
