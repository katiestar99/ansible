# -*- mode: python -*-

# Copyright: (c) 2012, Jeroen Hoekx (@jhoekx)
# Copyright: Assible Team
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: group_by
short_description: Create Assible groups based on facts
description:
- Use facts to create ad-hoc groups that can be used later in a playbook.
- This module is also supported for Windows targets.
version_added: "0.9"
options:
  key:
    description:
    - The variables whose values will be used as groups.
    type: str
    required: true
  parents:
    description:
    - The list of the parent groups.
    type: list
    default: all
    version_added: "2.4"
notes:
- Spaces in group names are converted to dashes '-'.
- This module is also supported for Windows targets.
- Though this module does not change the remote host, we do provide 'changed' status as it can be useful for those trying to track inventory changes.
seealso:
- module: assible.builtin.add_host
author:
- Jeroen Hoekx (@jhoekx)
'''

EXAMPLES = r'''
- name: Create groups based on the machine architecture
  group_by:
    key: machine_{{ assible_machine }}

- name: Create groups like 'virt_kvm_host'
  group_by:
    key: virt_{{ assible_virtualization_type }}_{{ assible_virtualization_role }}

- name: Create nested groups
  group_by:
    key: el{{ assible_distribution_major_version }}-{{ assible_architecture }}
    parents:
      - el{{ assible_distribution_major_version }}

# Add all active hosts to a static group
- group_by:
    key: done
'''
