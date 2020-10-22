# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Say hello."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type


from assible.module_utils.basic import AssibleModule


def main():
    module = AssibleModule(
        argument_spec={
            'name': {'default': 'world'},
        },
    )
    name = module.params['name']

    module.exit_json(
        msg='Greeting {name} completed.'.
        format(name=name.title()),
        greeting='Hello, {name}!'.format(name=name),
    )


if __name__ == '__main__':
    main()
