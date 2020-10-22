# (c) 2020 Assible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = """
    lookup: noop
    author: Assible core team
    short_description: returns input
    description:
      - this is a noop
"""

EXAMPLES = """
- name: do nothing
  debug: msg="{{ lookup('testns.testcol.noop', [1,2,3,4] }}"
"""

RETURN = """
  _list:
    description: input given
"""

from assible.module_utils.common._collections_compat import Sequence
from assible.plugins.lookup import LookupBase
from assible.errors import AssibleError


class LookupModule(LookupBase):

    def run(self, terms, **kwargs):
        if not isinstance(terms, Sequence):
            raise AssibleError("testns.testcol.noop expects a list")
        return terms
