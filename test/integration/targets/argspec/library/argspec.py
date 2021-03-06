#!/usr/bin/python
# Copyright: (c) 2020, Matt Martz <matt@sivel.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from assible.module_utils.basic import AssibleModule


def main():
    module = AssibleModule(
        {
            'required': {
                'required': True,
            },
            'required_one_of_one': {},
            'required_one_of_two': {},
            'required_by_one': {},
            'required_by_two': {},
            'required_by_three': {},
            'state': {
                'type': 'str',
                'choices': ['absent', 'present'],
            },
            'path': {},
            'content': {},
            'mapping': {
                'type': 'dict',
            },
            'required_one_of': {
                'required_one_of': [['thing', 'other']],
                'type': 'list',
                'elements': 'dict',
                'options': {
                    'thing': {},
                    'other': {},
                },
            },
            'required_by': {
                'required_by': {'thing': 'other'},
                'type': 'list',
                'elements': 'dict',
                'options': {
                    'thing': {},
                    'other': {},
                },
            },
            'required_together': {
                'required_together': [['thing', 'other']],
                'type': 'list',
                'elements': 'dict',
                'options': {
                    'thing': {},
                    'other': {},
                    'another': {},
                },
            },
            'required_if': {
                'required_if': (
                    ('thing', 'foo', ('other',), True),
                ),
                'type': 'list',
                'elements': 'dict',
                'options': {
                    'thing': {},
                    'other': {},
                    'another': {},
                },
            },
            'json': {
                'type': 'json',
            },
            'fail_on_missing_params': {
                'type': 'list',
                'default': [],
            },
            'needed_param': {},
            'required_together_one': {},
            'required_together_two': {},
            'suboptions_list_no_elements': {
                'type': 'list',
                'options': {
                    'thing': {},
                },
            },
            'choices_with_strings_like_bools': {
                'type': 'str',
                'choices': [
                    'on',
                    'off',
                ],
            },
        },
        required_if=(
            ('state', 'present', ('path', 'content'), True),
        ),
        mutually_exclusive=(
            ('path', 'content'),
        ),
        required_one_of=(
            ('required_one_of_one', 'required_one_of_two'),
        ),
        required_by={
            'required_by_one': ('required_by_two', 'required_by_three'),
        },
        required_together=(
            ('required_together_one', 'required_together_two'),
        ),
    )

    module.fail_on_missing_params(module.params['fail_on_missing_params'])

    module.exit_json(**module.params)


if __name__ == '__main__':
    main()
