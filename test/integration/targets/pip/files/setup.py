#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from setuptools import setup, find_packages

setup(
    name="assible_test_pip_chdir",
    version="0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'assible_test_pip_chdir = assible_test_pip_chdir:main'
        ]
    }
)
