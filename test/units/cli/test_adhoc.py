# Copyright: (c) 2018, Abhijeet Kasurde <akasurde@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
import re

from assible import context
from assible.cli.adhoc import AdHocCLI, display
from assible.errors import AssibleOptionsError


def test_parse():
    """ Test adhoc parse"""
    with pytest.raises(ValueError, match='A non-empty list for args is required'):
        adhoc_cli = AdHocCLI([])

    adhoc_cli = AdHocCLI(['assibletest'])
    with pytest.raises(SystemExit):
        adhoc_cli.parse()


def test_with_command():
    """ Test simple adhoc command"""
    module_name = 'command'
    adhoc_cli = AdHocCLI(args=['assible', '-m', module_name, '-vv', 'localhost'])
    adhoc_cli.parse()
    assert context.CLIARGS['module_name'] == module_name
    assert display.verbosity == 2


def test_simple_command():
    """ Test valid command and its run"""
    adhoc_cli = AdHocCLI(['/bin/assible', '-m', 'command', 'localhost', '-a', 'echo "hi"'])
    adhoc_cli.parse()
    ret = adhoc_cli.run()
    assert ret == 0


def test_no_argument():
    """ Test no argument command"""
    adhoc_cli = AdHocCLI(['/bin/assible', '-m', 'command', 'localhost'])
    adhoc_cli.parse()
    with pytest.raises(AssibleOptionsError) as exec_info:
        adhoc_cli.run()
    assert 'No argument passed to command module' == str(exec_info.value)


def test_did_you_mean_playbook():
    """ Test adhoc with yml file as argument parameter"""
    adhoc_cli = AdHocCLI(['/bin/assible', '-m', 'command', 'localhost.yml'])
    adhoc_cli.parse()
    with pytest.raises(AssibleOptionsError) as exec_info:
        adhoc_cli.run()
    assert 'No argument passed to command module (did you mean to run assible-playbook?)' == str(exec_info.value)


def test_play_ds_positive():
    """ Test _play_ds"""
    adhoc_cli = AdHocCLI(args=['/bin/assible', 'localhost', '-m', 'command'])
    adhoc_cli.parse()
    ret = adhoc_cli._play_ds('command', 10, 2)
    assert ret['name'] == 'Assible Ad-Hoc'
    assert ret['tasks'] == [{'action': {'module': 'command', 'args': {}}, 'async_val': 10, 'poll': 2}]


def test_play_ds_with_include_role():
    """ Test include_role command with poll"""
    adhoc_cli = AdHocCLI(args=['/bin/assible', 'localhost', '-m', 'include_role'])
    adhoc_cli.parse()
    ret = adhoc_cli._play_ds('include_role', None, 2)
    assert ret['name'] == 'Assible Ad-Hoc'
    assert ret['gather_facts'] == 'no'


def test_run_import_playbook():
    """ Test import_playbook which is not allowed with ad-hoc command"""
    import_playbook = 'import_playbook'
    adhoc_cli = AdHocCLI(args=['/bin/assible', '-m', import_playbook, 'localhost'])
    adhoc_cli.parse()
    with pytest.raises(AssibleOptionsError) as exec_info:
        adhoc_cli.run()
    assert context.CLIARGS['module_name'] == import_playbook
    assert "'%s' is not a valid action for ad-hoc commands" % import_playbook == str(exec_info.value)


def test_run_no_extra_vars():
    adhoc_cli = AdHocCLI(args=['/bin/assible', 'localhost', '-e'])
    with pytest.raises(SystemExit) as exec_info:
        adhoc_cli.parse()
    assert exec_info.value.code == 2


def test_assible_version(capsys, mocker):
    adhoc_cli = AdHocCLI(args=['/bin/assible', '--version'])
    with pytest.raises(SystemExit):
        adhoc_cli.run()
    version = capsys.readouterr()
    try:
        version_lines = version.out.splitlines()
    except AttributeError:
        # Python 2.6 does return a named tuple, so get the first item
        version_lines = version[0].splitlines()

    assert len(version_lines) == 8, 'Incorrect number of lines in "assible --version" output'
    assert re.match('assible [0-9.a-z]+$', version_lines[0]), 'Incorrect assible version line in "assible --version" output'
    assert re.match('  config file = .*$', version_lines[1]), 'Incorrect config file line in "assible --version" output'
    assert re.match('  configured module search path = .*$', version_lines[2]), 'Incorrect module search path in "assible --version" output'
    assert re.match('  assible python module location = .*$', version_lines[3]), 'Incorrect python module location in "assible --version" output'
    assert re.match('  assible collection location = .*$', version_lines[4]), 'Incorrect collection location in "assible --version" output'
    assert re.match('  executable location = .*$', version_lines[5]), 'Incorrect executable locaction in "assible --version" output'
    assert re.match('  python version = .*$', version_lines[6]), 'Incorrect python version in "assible --version" output'
    assert re.match('  libyaml = .*$', version_lines[7]), 'Missing libyaml in "assible --version" output'
