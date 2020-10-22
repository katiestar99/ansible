# -*- coding: utf-8 -*-
# (c) 2018 Matt Martz <matt@sivel.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from assible.module_utils.six import PY3
from assible.utils.unsafe_proxy import AssibleUnsafe, AssibleUnsafeBytes, AssibleUnsafeText, wrap_var


def test_wrap_var_text():
    assert isinstance(wrap_var(u'foo'), AssibleUnsafeText)


def test_wrap_var_bytes():
    assert isinstance(wrap_var(b'foo'), AssibleUnsafeBytes)


def test_wrap_var_string():
    if PY3:
        assert isinstance(wrap_var('foo'), AssibleUnsafeText)
    else:
        assert isinstance(wrap_var('foo'), AssibleUnsafeBytes)


def test_wrap_var_dict():
    assert isinstance(wrap_var(dict(foo='bar')), dict)
    assert not isinstance(wrap_var(dict(foo='bar')), AssibleUnsafe)
    assert isinstance(wrap_var(dict(foo=u'bar'))['foo'], AssibleUnsafeText)


def test_wrap_var_dict_None():
    assert wrap_var(dict(foo=None))['foo'] is None
    assert not isinstance(wrap_var(dict(foo=None))['foo'], AssibleUnsafe)


def test_wrap_var_list():
    assert isinstance(wrap_var(['foo']), list)
    assert not isinstance(wrap_var(['foo']), AssibleUnsafe)
    assert isinstance(wrap_var([u'foo'])[0], AssibleUnsafeText)


def test_wrap_var_list_None():
    assert wrap_var([None])[0] is None
    assert not isinstance(wrap_var([None])[0], AssibleUnsafe)


def test_wrap_var_set():
    assert isinstance(wrap_var(set(['foo'])), set)
    assert not isinstance(wrap_var(set(['foo'])), AssibleUnsafe)
    for item in wrap_var(set([u'foo'])):
        assert isinstance(item, AssibleUnsafeText)


def test_wrap_var_set_None():
    for item in wrap_var(set([None])):
        assert item is None
        assert not isinstance(item, AssibleUnsafe)


def test_wrap_var_tuple():
    assert isinstance(wrap_var(('foo',)), tuple)
    assert not isinstance(wrap_var(('foo',)), AssibleUnsafe)
    assert isinstance(wrap_var(('foo',))[0], AssibleUnsafe)


def test_wrap_var_tuple_None():
    assert wrap_var((None,))[0] is None
    assert not isinstance(wrap_var((None,))[0], AssibleUnsafe)


def test_wrap_var_None():
    assert wrap_var(None) is None
    assert not isinstance(wrap_var(None), AssibleUnsafe)


def test_wrap_var_unsafe_text():
    assert isinstance(wrap_var(AssibleUnsafeText(u'foo')), AssibleUnsafeText)


def test_wrap_var_unsafe_bytes():
    assert isinstance(wrap_var(AssibleUnsafeBytes(b'foo')), AssibleUnsafeBytes)


def test_wrap_var_no_ref():
    thing = {
        'foo': {
            'bar': 'baz'
        },
        'bar': ['baz', 'qux'],
        'baz': ('qux',),
        'none': None,
        'text': 'text',
    }
    wrapped_thing = wrap_var(thing)
    thing is not wrapped_thing
    thing['foo'] is not wrapped_thing['foo']
    thing['bar'][0] is not wrapped_thing['bar'][0]
    thing['baz'][0] is not wrapped_thing['baz'][0]
    thing['none'] is not wrapped_thing['none']
    thing['text'] is not wrapped_thing['text']


def test_AssibleUnsafeText():
    assert isinstance(AssibleUnsafeText(u'foo'), AssibleUnsafe)


def test_AssibleUnsafeBytes():
    assert isinstance(AssibleUnsafeBytes(b'foo'), AssibleUnsafe)
