#!/usr/bin/python
# https://github.com/assible/assible/issues/64664
# https://github.com/assible/assible/issues/64479

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import sys

from assible.module_utils.basic import AssibleModule


def main():
    module = AssibleModule({})

    this_module = sys.modules[__name__]
    module.exit_json(
        failed=not getattr(this_module, 'AssibleModule', False)
    )


if __name__ == '__main__':
    main()
