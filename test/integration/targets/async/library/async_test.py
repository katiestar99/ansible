from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import sys

from assible.module_utils.basic import AssibleModule


def main():
    if "--interactive" in sys.argv:
        import assible.module_utils.basic
        assible.module_utils.basic._ASSIBLE_ARGS = json.dumps(dict(
            ASSIBLE_MODULE_ARGS=dict(
                fail_mode="graceful"
            )
        ))

    module = AssibleModule(
        argument_spec=dict(
            fail_mode=dict(type='list', default=['success'])
        )
    )

    result = dict(changed=True)

    fail_mode = module.params['fail_mode']

    try:
        if 'leading_junk' in fail_mode:
            print("leading junk before module output")

        if 'graceful' in fail_mode:
            module.fail_json(msg="failed gracefully")

        if 'exception' in fail_mode:
            raise Exception('failing via exception')

        if 'stderr' in fail_mode:
            print('printed to stderr', file=sys.stderr)

        module.exit_json(**result)

    finally:
        if 'trailing_junk' in fail_mode:
            print("trailing junk after module output")


main()
