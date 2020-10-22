#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from assible.module_utils.basic import AssibleModule


def main():
    module = AssibleModule(
        argument_spec=dict(),
    )
    result = {
        'selinux_special_fs': module._selinux_special_fs,
        'tmpdir': module._tmpdir,
        'keep_remote_files': module._keep_remote_files,
        'version': module.assible_version,
    }
    module.exit_json(**result)


if __name__ == '__main__':
    main()
