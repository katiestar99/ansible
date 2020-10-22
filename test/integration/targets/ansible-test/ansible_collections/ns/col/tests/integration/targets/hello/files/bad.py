from __future__ import absolute_import, division, print_function
__metaclass__ = type

import tempfile

try:
    import urllib2  # intentionally trigger pylint assible-bad-import error
except ImportError:
    urllib2 = None

try:
    from urllib2 import Request  # intentionally trigger pylint assible-bad-import-from error
except ImportError:
    Request = None

tempfile.mktemp()  # intentionally trigger pylint assible-bad-function error
