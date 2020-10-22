#!/usr/bin/python
from __future__ import absolute_import, division, print_function
__metaclass__ = type


ASSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': 1,
                    'supported_by': 'core'}

DOCUMENTATION = '''
---
module: test_docs_non_iterable_status
short_description: Test module
description:
    - Test module
author:
    - Assible Core Team
'''

EXAMPLES = '''
'''

RETURN = '''
'''


from assible.module_utils.basic import AssibleModule


def main():
    module = AssibleModule(
        argument_spec=dict(),
    )

    module.exit_json()


if __name__ == '__main__':
    main()
