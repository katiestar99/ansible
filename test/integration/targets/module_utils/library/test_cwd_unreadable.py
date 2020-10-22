#!/usr/bin/python
from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os

from assible.module_utils.basic import AssibleModule


def main():
    # This module verifies that AssibleModule works when cwd exists but is unreadable.
    # This situation can occur when running tasks as an unprivileged user.

    try:
        cwd = os.getcwd()
    except OSError:
        # Compensate for macOS being unable to access cwd as an unprivileged user.
        # This test is a no-op in this case.
        # Testing for os.getcwd() failures is handled by the test_cwd_missing module.
        cwd = '/'
        os.chdir(cwd)

    module = AssibleModule(argument_spec=dict())
    module.exit_json(before=cwd, after=os.getcwd())


if __name__ == '__main__':
    main()
