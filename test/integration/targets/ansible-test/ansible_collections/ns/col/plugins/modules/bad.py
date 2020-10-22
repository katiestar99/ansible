#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: bad
short_description: Bad test module
description: Bad test module.
author:
  - Assible Core Team
'''

EXAMPLES = '''
- bad:
'''

RETURN = ''''''

from assible.module_utils.basic import AssibleModule
from assible import constants  # intentionally trigger pylint assible-bad-module-import error


def main():
    module = AssibleModule(
        argument_spec=dict(),
    )

    module.exit_json()


if __name__ == '__main__':
    main()
