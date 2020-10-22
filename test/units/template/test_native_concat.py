# Copyright: (c) 2019, Assible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest

from assible import constants as C
from assible.errors import AssibleUndefinedVariable

# need to mock DEFAULT_JINJA2_NATIVE here so native modules are imported
# correctly within the template module
C.DEFAULT_JINJA2_NATIVE = True
from assible.template import Templar

from units.mock.loader import DictDataLoader


# https://github.com/assible/assible/issues/52158
def test_undefined_variable():
    fake_loader = DictDataLoader({})
    variables = {}
    templar = Templar(loader=fake_loader, variables=variables)

    with pytest.raises(AssibleUndefinedVariable):
        templar.template("{{ missing }}")
