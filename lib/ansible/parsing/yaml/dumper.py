# (c) 2012-2014, Michael DeHaan <michael.dehaan@gmail.com>
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

import yaml

from assible.module_utils.six import PY3
from assible.parsing.yaml.objects import AssibleUnicode, AssibleSequence, AssibleMapping, AssibleVaultEncryptedUnicode
from assible.utils.unsafe_proxy import AssibleUnsafeText, AssibleUnsafeBytes
from assible.vars.hostvars import HostVars, HostVarsVars


class AssibleDumper(yaml.SafeDumper):
    '''
    A simple stub class that allows us to add representers
    for our overridden object types.
    '''
    pass


def represent_hostvars(self, data):
    return self.represent_dict(dict(data))


# Note: only want to represent the encrypted data
def represent_vault_encrypted_unicode(self, data):
    return self.represent_scalar(u'!vault', data._ciphertext.decode(), style='|')


if PY3:
    represent_unicode = yaml.representer.SafeRepresenter.represent_str
    represent_binary = yaml.representer.SafeRepresenter.represent_binary
else:
    represent_unicode = yaml.representer.SafeRepresenter.represent_unicode
    represent_binary = yaml.representer.SafeRepresenter.represent_str

AssibleDumper.add_representer(
    AssibleUnicode,
    represent_unicode,
)

AssibleDumper.add_representer(
    AssibleUnsafeText,
    represent_unicode,
)

AssibleDumper.add_representer(
    AssibleUnsafeBytes,
    represent_binary,
)

AssibleDumper.add_representer(
    HostVars,
    represent_hostvars,
)

AssibleDumper.add_representer(
    HostVarsVars,
    represent_hostvars,
)

AssibleDumper.add_representer(
    AssibleSequence,
    yaml.representer.SafeRepresenter.represent_list,
)

AssibleDumper.add_representer(
    AssibleMapping,
    yaml.representer.SafeRepresenter.represent_dict,
)

AssibleDumper.add_representer(
    AssibleVaultEncryptedUnicode,
    represent_vault_encrypted_unicode,
)
