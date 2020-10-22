# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest

from assible.cli.doc import DocCLI


TTY_IFY_DATA = {
    # No substitutions
    'no-op': 'no-op',
    'no-op Z(test)': 'no-op Z(test)',
    # Simple cases of all substitutions
    'I(italic)': "`italic'",
    'B(bold)': '*bold*',
    'M(assible.builtin.module)': '[assible.builtin.module]',
    'U(https://docs.assible.com)': 'https://docs.assible.com',
    'L(the user guide,https://docs.assible.com/user-guide.html)': 'the user guide <https://docs.assible.com/user-guide.html>',
    'R(the user guide,user-guide)': 'the user guide',
    'C(/usr/bin/file)': "`/usr/bin/file'",
    'HORIZONTALLINE': '\n{0}\n'.format('-' * 13),
    # Multiple substitutions
    'The M(assible.builtin.yum) module B(MUST) be given the C(package) parameter.  See the R(looping docs,using-loops) for more info':
    "The [assible.builtin.yum] module *MUST* be given the `package' parameter.  See the looping docs for more info",
    # Problem cases
    'IBM(International Business Machines)': 'IBM(International Business Machines)',
    'L(the user guide, https://docs.assible.com/)': 'the user guide <https://docs.assible.com/>',
    'R(the user guide, user-guide)': 'the user guide',
}


@pytest.mark.parametrize('text, expected', sorted(TTY_IFY_DATA.items()))
def test_ttyify(text, expected):
    assert DocCLI.tty_ify(text) == expected
