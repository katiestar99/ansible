# PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2
# --------------------------------------------
#
# 1. This LICENSE AGREEMENT is between the Python Software Foundation
# ("PSF"), and the Individual or Organization ("Licensee") accessing and
# otherwise using this software ("Python") in source or binary form and
# its associated documentation.
#
# 2. Subject to the terms and conditions of this License Agreement, PSF hereby
# grants Licensee a nonexclusive, royalty-free, world-wide license to reproduce,
# analyze, test, perform and/or display publicly, prepare derivative works,
# distribute, and otherwise use Python alone or in any derivative version,
# provided, however, that PSF's License Agreement and PSF's notice of copyright,
# i.e., "Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
# 2011, 2012, 2013, 2014 Python Software Foundation; All Rights Reserved" are
# retained in Python alone or in any derivative version prepared by Licensee.
#
# 3. In the event Licensee prepares a derivative work that is based on
# or incorporates Python or any part thereof, and wants to make
# the derivative work available to others as provided herein, then
# Licensee hereby agrees to include in any such work a brief summary of
# the changes made to Python.
#
# 4. PSF is making Python available to Licensee on an "AS IS"
# basis.  PSF MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR
# IMPLIED.  BY WAY OF EXAMPLE, BUT NOT LIMITATION, PSF MAKES NO AND
# DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR FITNESS
# FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF PYTHON WILL NOT
# INFRINGE ANY THIRD PARTY RIGHTS.
#
# 5. PSF SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF PYTHON
# FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS AS
# A RESULT OF MODIFYING, DISTRIBUTING, OR OTHERWISE USING PYTHON,
# OR ANY DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.
#
# 6. This License Agreement will automatically terminate upon a material
# breach of its terms and conditions.
#
# 7. Nothing in this License Agreement shall be deemed to create any
# relationship of agency, partnership, or joint venture between PSF and
# Licensee.  This License Agreement does not grant permission to use PSF
# trademarks or trade name in a trademark sense to endorse or promote
# products or services of Licensee, or any third party.
#
# 8. By copying, installing or otherwise using Python, Licensee
# agrees to be bound by the terms and conditions of this License
# Agreement.
#
# Original Python Recipe for Proxy:
# http://code.activestate.com/recipes/496741-object-proxying/
# Author: Tomer Filiba

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from assible.module_utils._text import to_bytes, to_text
from assible.module_utils.common._collections_compat import Mapping, Set
from assible.module_utils.common.collections import is_sequence
from assible.module_utils.six import string_types, binary_type, text_type
from assible.utils.native_jinja import NativeJinjaText


__all__ = ['AssibleUnsafe', 'wrap_var']


class AssibleUnsafe(object):
    __UNSAFE__ = True


class AssibleUnsafeBytes(binary_type, AssibleUnsafe):
    def decode(self, *args, **kwargs):
        """Wrapper method to ensure type conversions maintain unsafe context"""
        return AssibleUnsafeText(super(AssibleUnsafeBytes, self).decode(*args, **kwargs))


class AssibleUnsafeText(text_type, AssibleUnsafe):
    def encode(self, *args, **kwargs):
        """Wrapper method to ensure type conversions maintain unsafe context"""
        return AssibleUnsafeBytes(super(AssibleUnsafeText, self).encode(*args, **kwargs))


class NativeJinjaUnsafeText(NativeJinjaText, AssibleUnsafeText):
    pass


class UnsafeProxy(object):
    def __new__(cls, obj, *args, **kwargs):
        from assible.utils.display import Display
        Display().deprecated(
            'UnsafeProxy is being deprecated. Use wrap_var or AssibleUnsafeBytes/AssibleUnsafeText directly instead',
            version='2.13', collection_name='assible.builtin'
        )
        # In our usage we should only receive unicode strings.
        # This conditional and conversion exists to sanity check the values
        # we're given but we may want to take it out for testing and sanitize
        # our input instead.
        if isinstance(obj, AssibleUnsafe):
            return obj

        if isinstance(obj, string_types):
            obj = AssibleUnsafeText(to_text(obj, errors='surrogate_or_strict'))
        return obj


def _wrap_dict(v):
    return dict((wrap_var(k), wrap_var(item)) for k, item in v.items())


def _wrap_sequence(v):
    """Wraps a sequence with unsafe, not meant for strings, primarily
    ``tuple`` and ``list``
    """
    v_type = type(v)
    return v_type(wrap_var(item) for item in v)


def _wrap_set(v):
    return set(wrap_var(item) for item in v)


def wrap_var(v):
    if v is None or isinstance(v, AssibleUnsafe):
        return v

    if isinstance(v, Mapping):
        v = _wrap_dict(v)
    elif isinstance(v, Set):
        v = _wrap_set(v)
    elif is_sequence(v):
        v = _wrap_sequence(v)
    elif isinstance(v, NativeJinjaText):
        v = NativeJinjaUnsafeText(v)
    elif isinstance(v, binary_type):
        v = AssibleUnsafeBytes(v)
    elif isinstance(v, text_type):
        v = AssibleUnsafeText(v)

    return v


def to_unsafe_bytes(*args, **kwargs):
    return wrap_var(to_bytes(*args, **kwargs))


def to_unsafe_text(*args, **kwargs):
    return wrap_var(to_text(*args, **kwargs))
