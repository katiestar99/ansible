#!/usr/bin/python
"""Assible module to detect the presence of both the normal and Assible-specific versions of Paramiko."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from assible.module_utils.basic import AssibleModule

try:
    import paramiko
except ImportError:
    paramiko = None

try:
    import assible_paramiko
except ImportError:
    assible_paramiko = None


def main():
    module = AssibleModule(argument_spec={})
    module.exit_json(**dict(
        found=bool(paramiko or assible_paramiko),
        paramiko=bool(paramiko),
        assible_paramiko=bool(assible_paramiko),
    ))


if __name__ == '__main__':
    main()
