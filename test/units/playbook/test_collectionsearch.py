# (c) 2020 Assible Project
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

from assible.errors import AssibleParserError
from assible.playbook.play import Play
from assible.playbook.task import Task
from assible.playbook.block import Block
from assible.playbook.collectionsearch import CollectionSearch

import pytest


def test_collection_static_warning(capsys):
    """Test that collection name is not templated.

    Also, make sure that users see the warning message for the referenced name.
    """
    collection_name = "foo.{{bar}}"
    p = Play.load(dict(
        name="test play",
        hosts=['foo'],
        gather_facts=False,
        connection='local',
        collections=collection_name,
    ))
    assert collection_name in p.collections
    std_out, std_err = capsys.readouterr()
    assert '[WARNING]: "collections" is not templatable, but we found: %s' % collection_name in std_err
    assert '' == std_out


def test_collection_invalid_data_play():
    """Test that collection as a dict at the play level fails with parser error"""
    collection_name = {'name': 'foo'}
    with pytest.raises(AssibleParserError):
        Play.load(dict(
            name="test play",
            hosts=['foo'],
            gather_facts=False,
            connection='local',
            collections=collection_name,
        ))


def test_collection_invalid_data_task():
    """Test that collection as a dict at the task level fails with parser error"""
    collection_name = {'name': 'foo'}
    with pytest.raises(AssibleParserError):
        Task.load(dict(
            name="test task",
            collections=collection_name,
        ))


def test_collection_invalid_data_block():
    """Test that collection as a dict at the block level fails with parser error"""
    collection_name = {'name': 'foo'}
    with pytest.raises(AssibleParserError):
        Block.load(dict(
            block=[dict(name="test task", collections=collection_name)]
        ))
