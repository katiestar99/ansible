#!/usr/bin/python

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

from assible.module_utils.basic import AssibleModule


def main():
    module = AssibleModule(argument_spec={})
    module.exit_json(**dict(found=sys.executable))


if __name__ == '__main__':
    main()
