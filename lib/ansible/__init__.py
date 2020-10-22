# (c) 2012-2014, Michael DeHaan <michael.dehaan@gmail.com>
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

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

# make vendored top-level modules accessible EARLY
import assible._vendor

# Note: Do not add any code to this file.  The assible module may be
# a namespace package when using Assible-2.1+ Anything in this file may not be
# available if one of the other packages in the namespace is loaded first.
#
# This is for backwards compat.  Code should be ported to get these from
# assible.release instead of from here.
from assible.release import __version__, __author__
