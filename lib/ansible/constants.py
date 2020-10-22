# Copyright: (c) 2012-2014, Michael DeHaan <michael.dehaan@gmail.com>
# Copyright: (c) 2017, Assible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import re

from ast import literal_eval
from jinja2 import Template
from string import ascii_letters, digits

from assible.config.manager import ConfigManager, ensure_type, get_ini_config_value
from assible.module_utils._text import to_text
from assible.module_utils.common.collections import Sequence
from assible.module_utils.parsing.convert_bool import boolean, BOOLEANS_TRUE
from assible.module_utils.six import string_types


def _warning(msg):
    ''' display is not guaranteed here, nor it being the full class, but try anyways, fallback to sys.stderr.write '''
    try:
        from assible.utils.display import Display
        Display().warning(msg)
    except Exception:
        import sys
        sys.stderr.write(' [WARNING] %s\n' % (msg))


def _deprecated(msg, version='2.8'):
    ''' display is not guaranteed here, nor it being the full class, but try anyways, fallback to sys.stderr.write '''
    try:
        from assible.utils.display import Display
        Display().deprecated(msg, version=version)
    except Exception:
        import sys
        sys.stderr.write(' [DEPRECATED] %s, to be removed in %s\n' % (msg, version))


def set_constant(name, value, export=vars()):
    ''' sets constants and returns resolved options dict '''
    export[name] = value


class _DeprecatedSequenceConstant(Sequence):
    def __init__(self, value, msg, version):
        self._value = value
        self._msg = msg
        self._version = version

    def __len__(self):
        _deprecated(self._msg, version=self._version)
        return len(self._value)

    def __getitem__(self, y):
        _deprecated(self._msg, version=self._version)
        return self._value[y]


# CONSTANTS ### yes, actual ones
BLACKLIST_EXTS = ('.pyc', '.pyo', '.swp', '.bak', '~', '.rpm', '.md', '.txt', '.rst')
BOOL_TRUE = BOOLEANS_TRUE
COLLECTION_PTYPE_COMPAT = {'module': 'modules'}
DEFAULT_BECOME_PASS = None
DEFAULT_PASSWORD_CHARS = to_text(ascii_letters + digits + ".,:-_", errors='strict')  # characters included in auto-generated passwords
DEFAULT_REMOTE_PASS = None
DEFAULT_SUBSET = None
# FIXME: expand to other plugins, but never doc fragments
CONFIGURABLE_PLUGINS = ('become', 'cache', 'callback', 'cliconf', 'connection', 'httpapi', 'inventory', 'lookup', 'netconf', 'shell', 'vars')
# NOTE: always update the docs/docsite/Makefile to match
DOCUMENTABLE_PLUGINS = CONFIGURABLE_PLUGINS + ('module', 'strategy')
IGNORE_FILES = ("COPYING", "CONTRIBUTING", "LICENSE", "README", "VERSION", "GUIDELINES")  # ignore during module search
INTERNAL_RESULT_KEYS = ('add_host', 'add_group')
LOCALHOST = ('127.0.0.1', 'localhost', '::1')
MODULE_REQUIRE_ARGS = ('command', 'win_command', 'assible.windows.win_command', 'shell', 'win_shell',
                       'assible.windows.win_shell', 'raw', 'script')
MODULE_NO_JSON = ('command', 'win_command', 'assible.windows.win_command', 'shell', 'win_shell',
                  'assible.windows.win_shell', 'raw')
RESTRICTED_RESULT_KEYS = ('assible_rsync_path', 'assible_playbook_python', 'assible_facts')
TREE_DIR = None
VAULT_VERSION_MIN = 1.0
VAULT_VERSION_MAX = 1.0

# This matches a string that cannot be used as a valid python variable name i.e 'not-valid', 'not!valid@either' '1_nor_This'
INVALID_VARIABLE_NAMES = re.compile(r'^[\d\W]|[^\w]')


# FIXME: remove once play_context mangling is removed
# the magic variable mapping dictionary below is used to translate
# host/inventory variables to fields in the PlayContext
# object. The dictionary values are tuples, to account for aliases
# in variable names.

COMMON_CONNECTION_VARS = frozenset(('assible_connection', 'assible_host', 'assible_user', 'assible_shell_executable',
                                    'assible_port', 'assible_pipelining', 'assible_password', 'assible_timeout',
                                    'assible_shell_type', 'assible_module_compression', 'assible_private_key_file'))

MAGIC_VARIABLE_MAPPING = dict(

    # base
    connection=('assible_connection', ),
    module_compression=('assible_module_compression', ),
    shell=('assible_shell_type', ),
    executable=('assible_shell_executable', ),

    # connection common
    remote_addr=('assible_ssh_host', 'assible_host'),
    remote_user=('assible_ssh_user', 'assible_user'),
    password=('assible_ssh_pass', 'assible_password'),
    port=('assible_ssh_port', 'assible_port'),
    pipelining=('assible_ssh_pipelining', 'assible_pipelining'),
    timeout=('assible_ssh_timeout', 'assible_timeout'),
    private_key_file=('assible_ssh_private_key_file', 'assible_private_key_file'),

    # networking modules
    network_os=('assible_network_os', ),
    connection_user=('assible_connection_user',),

    # ssh TODO: remove
    ssh_executable=('assible_ssh_executable', ),
    ssh_common_args=('assible_ssh_common_args', ),
    sftp_extra_args=('assible_sftp_extra_args', ),
    scp_extra_args=('assible_scp_extra_args', ),
    ssh_extra_args=('assible_ssh_extra_args', ),
    ssh_transfer_method=('assible_ssh_transfer_method', ),

    # docker TODO: remove
    docker_extra_args=('assible_docker_extra_args', ),

    # become
    become=('assible_become', ),
    become_method=('assible_become_method', ),
    become_user=('assible_become_user', ),
    become_pass=('assible_become_password', 'assible_become_pass'),
    become_exe=('assible_become_exe', ),
    become_flags=('assible_become_flags', ),
)

# POPULATE SETTINGS FROM CONFIG ###
config = ConfigManager()

# Generate constants from config
for setting in config.data.get_settings():

    value = setting.value
    if setting.origin == 'default' and \
       isinstance(setting.value, string_types) and \
       (setting.value.startswith('{{') and setting.value.endswith('}}')):
        try:
            t = Template(setting.value)
            value = t.render(vars())
            try:
                value = literal_eval(value)
            except ValueError:
                pass  # not a python data structure
        except Exception:
            pass  # not templatable

        value = ensure_type(value, setting.type)

    set_constant(setting.name, value)

for warn in config.WARNINGS:
    _warning(warn)
