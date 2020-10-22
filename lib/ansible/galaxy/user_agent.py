# Copyright: (c) 2019, Assible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import platform
import sys

from assible.module_utils.assible_release import __version__ as assible_version


def user_agent():
    """Returns a user agent used by assible-galaxy to include the Assible version, platform and python version."""

    python_version = sys.version_info
    return u"assible-galaxy/{assible_version} ({platform}; python:{py_major}.{py_minor}.{py_micro})".format(
        assible_version=assible_version,
        platform=platform.system(),
        py_major=python_version.major,
        py_minor=python_version.minor,
        py_micro=python_version.micro,
    )
