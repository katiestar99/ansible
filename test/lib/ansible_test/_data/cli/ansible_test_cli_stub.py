#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
"""Command line entry point for assible-test."""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import sys


def main():
    """Main program entry point."""
    assible_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source_root = os.path.join(assible_root, 'test', 'lib')

    if os.path.exists(os.path.join(source_root, 'assible_test', '_internal', 'cli.py')):
        # running from source, use that version of assible-test instead of any version that may already be installed
        sys.path.insert(0, source_root)

    # noinspection PyProtectedMember
    from assible_test._internal.cli import main as cli_main

    cli_main()


if __name__ == '__main__':
    main()
