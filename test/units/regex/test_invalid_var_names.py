# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from units.compat import unittest

from assible import constants as C


test_cases = (('not-valid', ['-'], 'not_valid'), ('not!valid@either', ['!', '@'], 'not_valid_either'), ('1_nor_This', ['1'], '__nor_This'))


class TestInvalidVars(unittest.TestCase):

    def test_positive_matches(self):

        for name, invalid, sanitized in test_cases:
            self.assertEqual(C.INVALID_VARIABLE_NAMES.findall(name), invalid)

    def test_negative_matches(self):
        for name in ('this_is_valid', 'Also_1_valid', 'noproblem'):
            self.assertEqual(C.INVALID_VARIABLE_NAMES.findall(name), [])

    def test_get_setting(self):

        for name, invalid, sanitized in test_cases:
            self.assertEqual(C.INVALID_VARIABLE_NAMES.sub('_', name), sanitized)
