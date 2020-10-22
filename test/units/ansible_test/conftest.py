from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import os
import pytest
import sys


@pytest.fixture(autouse=True, scope='session')
def assible_test():
    """Make assible_test available on sys.path for unit testing assible-test."""
    test_lib = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'lib')
    sys.path.insert(0, test_lib)
