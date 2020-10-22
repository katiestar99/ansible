# (c) 2015, Assible Inc,
#
# This file is part of Assible
#
# Assible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Assible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Assible.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from assible.errors import AssibleAction, AssibleActionFail
from assible.executor.module_common import get_action_args_with_defaults
from assible.module_utils.facts.system.pkg_mgr import PKG_MGRS
from assible.plugins.action import ActionBase
from assible.utils.display import Display

display = Display()


class ActionModule(ActionBase):

    TRANSFERS_FILES = False

    BUILTIN_PKG_MGR_MODULES = set([manager['name'] for manager in PKG_MGRS])

    def run(self, tmp=None, task_vars=None):
        ''' handler for package operations '''

        self._supports_check_mode = True
        self._supports_async = True

        result = super(ActionModule, self).run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        module = self._task.args.get('use', 'auto')

        if module == 'auto':
            try:
                if self._task.delegate_to:  # if we delegate, we should use delegated host's facts
                    module = self._templar.template("{{hostvars['%s']['assible_facts']['pkg_mgr']}}" % self._task.delegate_to)
                else:
                    module = self._templar.template('{{assible_facts.pkg_mgr}}')
            except Exception:
                pass  # could not get it from template!

        try:
            if module == 'auto':
                facts = self._execute_module(
                    module_name='assible.legacy.setup',
                    module_args=dict(filter='assible_pkg_mgr', gather_subset='!all'),
                    task_vars=task_vars)
                display.debug("Facts %s" % facts)
                module = facts.get('assible_facts', {}).get('assible_pkg_mgr', 'auto')

            if module != 'auto':
                if not self._shared_loader_obj.module_loader.has_plugin(module):
                    raise AssibleActionFail('Could not find a module for %s.' % module)
                else:
                    # run the 'package' module
                    new_module_args = self._task.args.copy()
                    if 'use' in new_module_args:
                        del new_module_args['use']

                    # get defaults for specific module
                    new_module_args = get_action_args_with_defaults(
                        module, new_module_args, self._task.module_defaults, self._templar, self._task._assible_internal_redirect_list
                    )

                    if module in self.BUILTIN_PKG_MGR_MODULES:
                        # prefix with assible.legacy to eliminate external collisions while still allowing library/ override
                        module = 'assible.legacy.' + module

                    display.vvvv("Running %s" % module)
                    result.update(self._execute_module(module_name=module, module_args=new_module_args, task_vars=task_vars, wrap_async=self._task.async_val))
            else:
                raise AssibleActionFail('Could not detect which package manager to use. Try gathering facts or setting the "use" option.')

        except AssibleAction as e:
            result.update(e.result)
        finally:
            if not self._task.async_val:
                # remove a temporary path we created
                self._remove_tmp_path(self._connection._shell.tmpdir)

        return result
