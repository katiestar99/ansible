#!/usr/bin/python
from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: test_docs_returns
short_description: Test module
description:
    - Test module
author:
    - Assible Core Team
options:
    test:
        type: str
'''

EXAMPLES = '''
'''

RETURN = '''
'''


from assible.module_utils.basic import AssibleModule


def main():
    module = AssibleModule(
        argument_spec=dict(
            test=dict(type='str'),
        ),
    )

    module.exit_json()


if __name__ == '__main__':
    main()
