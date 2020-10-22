from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from assible_collections.testns.testcoll.plugins.module_utils import secondary
import assible_collections.testns.testcoll.plugins.module_utils.secondary


def thingtocall():
    if secondary != assible_collections.testns.testcoll.plugins.module_utils.secondary:
        raise Exception()

    return "thingtocall in base called " + assible_collections.testns.testcoll.plugins.module_utils.secondary.thingtocall()
