from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import pkgutil
import pytest
import re
import sys

from assible.module_utils.six import PY3, string_types
from assible.module_utils.compat.importlib import import_module
from assible.utils.collection_loader import AssibleCollectionConfig, AssibleCollectionRef
from assible.utils.collection_loader._collection_finder import (
    _AssibleCollectionFinder, _AssibleCollectionLoader, _AssibleCollectionNSPkgLoader, _AssibleCollectionPkgLoader,
    _AssibleCollectionPkgLoaderBase, _AssibleCollectionRootPkgLoader, _AssiblePathHookFinder,
    _get_collection_name_from_path, _get_collection_role_path, _get_collection_metadata, _iter_modules_impl
)
from assible.utils.collection_loader._collection_config import _EventSource
from units.compat.mock import MagicMock, NonCallableMagicMock, patch


# fixture to ensure we always clean up the import stuff when we're done
@pytest.fixture(autouse=True, scope='function')
def teardown(*args, **kwargs):
    yield
    reset_collections_loader_state()

# BEGIN STANDALONE TESTS - these exercise behaviors of the individual components without the import machinery


def test_finder_setup():
    # ensure scalar path is listified
    f = _AssibleCollectionFinder(paths='/bogus/bogus')
    assert isinstance(f._n_collection_paths, list)

    # ensure sys.path paths that have an assible_collections dir are added to the end of the collections paths
    with patch.object(sys, 'path', ['/bogus', default_test_collection_paths[1], '/morebogus', default_test_collection_paths[0]]):
        f = _AssibleCollectionFinder(paths=['/explicit', '/other'])
        assert f._n_collection_paths == ['/explicit', '/other', default_test_collection_paths[1], default_test_collection_paths[0]]

    configured_paths = ['/bogus']
    playbook_paths = ['/playbookdir']
    f = _AssibleCollectionFinder(paths=configured_paths)
    assert f._n_collection_paths == configured_paths
    f.set_playbook_paths(playbook_paths)
    assert f._n_collection_paths == extend_paths(playbook_paths, 'collections') + configured_paths

    # ensure scalar playbook_paths gets listified
    f.set_playbook_paths(playbook_paths[0])
    assert f._n_collection_paths == extend_paths(playbook_paths, 'collections') + configured_paths


def test_finder_not_interested():
    f = get_default_finder()
    assert f.find_module('nothanks') is None
    assert f.find_module('nothanks.sub', path=['/bogus/dir']) is None


def test_finder_ns():
    # ensure we can still load assible_collections and assible_collections.assible when they don't exist on disk
    f = _AssibleCollectionFinder(paths=['/bogus/bogus'])
    loader = f.find_module('assible_collections')
    assert isinstance(loader, _AssibleCollectionRootPkgLoader)

    loader = f.find_module('assible_collections.assible', path=['/bogus/bogus'])
    assert isinstance(loader, _AssibleCollectionNSPkgLoader)

    f = get_default_finder()
    loader = f.find_module('assible_collections')
    assert isinstance(loader, _AssibleCollectionRootPkgLoader)

    # path is not allowed for top-level
    with pytest.raises(ValueError):
        f.find_module('assible_collections', path=['whatever'])

    # path is required for subpackages
    with pytest.raises(ValueError):
        f.find_module('assible_collections.whatever', path=None)

    paths = [os.path.join(p, 'assible_collections/nonexistns') for p in default_test_collection_paths]

    # test missing
    loader = f.find_module('assible_collections.nonexistns', paths)
    assert loader is None


# keep these up top to make sure the loader install/remove are working, since we rely on them heavily in the tests
def test_loader_remove():
    fake_mp = [MagicMock(), _AssibleCollectionFinder(), MagicMock(), _AssibleCollectionFinder()]
    fake_ph = [MagicMock().m1, MagicMock().m2, _AssibleCollectionFinder()._assible_collection_path_hook, NonCallableMagicMock]
    # must nest until 2.6 compilation is totally donezo
    with patch.object(sys, 'meta_path', fake_mp):
        with patch.object(sys, 'path_hooks', fake_ph):
            _AssibleCollectionFinder()._remove()
            assert len(sys.meta_path) == 2
            # no AssibleCollectionFinders on the meta path after remove is called
            assert all((not isinstance(mpf, _AssibleCollectionFinder) for mpf in sys.meta_path))
            assert len(sys.path_hooks) == 3
            # none of the remaining path hooks should point at an AssibleCollectionFinder
            assert all((not isinstance(ph.__self__, _AssibleCollectionFinder) for ph in sys.path_hooks if hasattr(ph, '__self__')))
            assert AssibleCollectionConfig.collection_finder is None


def test_loader_install():
    fake_mp = [MagicMock(), _AssibleCollectionFinder(), MagicMock(), _AssibleCollectionFinder()]
    fake_ph = [MagicMock().m1, MagicMock().m2, _AssibleCollectionFinder()._assible_collection_path_hook, NonCallableMagicMock]
    # must nest until 2.6 compilation is totally donezo
    with patch.object(sys, 'meta_path', fake_mp):
        with patch.object(sys, 'path_hooks', fake_ph):
            f = _AssibleCollectionFinder()
            f._install()
            assert len(sys.meta_path) == 3  # should have removed the existing ACFs and installed a new one
            assert sys.meta_path[0] is f  # at the front
            # the rest of the meta_path should not be AssibleCollectionFinders
            assert all((not isinstance(mpf, _AssibleCollectionFinder) for mpf in sys.meta_path[1:]))
            assert len(sys.path_hooks) == 4  # should have removed the existing ACF path hooks and installed a new one
            # the first path hook should be ours, make sure it's pointing at the right instance
            assert hasattr(sys.path_hooks[0], '__self__') and sys.path_hooks[0].__self__ is f
            # the rest of the path_hooks should not point at an AssibleCollectionFinder
            assert all((not isinstance(ph.__self__, _AssibleCollectionFinder) for ph in sys.path_hooks[1:] if hasattr(ph, '__self__')))
            assert AssibleCollectionConfig.collection_finder is f
            with pytest.raises(ValueError):
                AssibleCollectionConfig.collection_finder = f


def test_finder_coll():
    f = get_default_finder()

    tests = [
        {'name': 'assible_collections.testns.testcoll', 'test_paths': [default_test_collection_paths]},
        {'name': 'assible_collections.assible.builtin', 'test_paths': [['/bogus'], default_test_collection_paths]},
    ]
    # ensure finder works for legit paths and bogus paths
    for test_dict in tests:
        # splat the dict values to our locals
        globals().update(test_dict)
        parent_pkg = name.rpartition('.')[0]
        for paths in test_paths:
            paths = [os.path.join(p, parent_pkg.replace('.', '/')) for p in paths]
            loader = f.find_module(name, path=paths)
            assert isinstance(loader, _AssibleCollectionPkgLoader)


def test_root_loader_not_interested():
    with pytest.raises(ImportError):
        _AssibleCollectionRootPkgLoader('not_assible_collections_toplevel', path_list=[])

    with pytest.raises(ImportError):
        _AssibleCollectionRootPkgLoader('assible_collections.somens', path_list=['/bogus'])


def test_root_loader():
    name = 'assible_collections'
    # ensure this works even when assible_collections doesn't exist on disk
    for paths in [], default_test_collection_paths:
        if name in sys.modules:
            del sys.modules[name]
        loader = _AssibleCollectionRootPkgLoader(name, paths)
        assert repr(loader).startswith('_AssibleCollectionRootPkgLoader(path=')
        module = loader.load_module(name)
        assert module.__name__ == name
        assert module.__path__ == [p for p in extend_paths(paths, name) if os.path.isdir(p)]
        # even if the dir exists somewhere, this loader doesn't support get_data, so make __file__ a non-file
        assert module.__file__ == '<assible_synthetic_collection_package>'
        assert module.__package__ == name
        assert sys.modules.get(name) == module


def test_nspkg_loader_not_interested():
    with pytest.raises(ImportError):
        _AssibleCollectionNSPkgLoader('not_assible_collections_toplevel.something', path_list=[])

    with pytest.raises(ImportError):
        _AssibleCollectionNSPkgLoader('assible_collections.somens.somecoll', path_list=[])


def test_nspkg_loader_load_module():
    # ensure the loader behaves on the toplevel and assible packages for both legit and missing/bogus paths
    for name in ['assible_collections.assible', 'assible_collections.testns']:
        parent_pkg = name.partition('.')[0]
        module_to_load = name.rpartition('.')[2]
        paths = extend_paths(default_test_collection_paths, parent_pkg)
        existing_child_paths = [p for p in extend_paths(paths, module_to_load) if os.path.exists(p)]
        if name in sys.modules:
            del sys.modules[name]
        loader = _AssibleCollectionNSPkgLoader(name, path_list=paths)
        assert repr(loader).startswith('_AssibleCollectionNSPkgLoader(path=')
        module = loader.load_module(name)
        assert module.__name__ == name
        assert isinstance(module.__loader__, _AssibleCollectionNSPkgLoader)
        assert module.__path__ == existing_child_paths
        assert module.__package__ == name
        assert module.__file__ == '<assible_synthetic_collection_package>'
        assert sys.modules.get(name) == module


def test_collpkg_loader_not_interested():
    with pytest.raises(ImportError):
        _AssibleCollectionPkgLoader('not_assible_collections', path_list=[])

    with pytest.raises(ImportError):
        _AssibleCollectionPkgLoader('assible_collections.ns', path_list=['/bogus/bogus'])


def test_collpkg_loader_load_module():
    reset_collections_loader_state()
    with patch('assible.utils.collection_loader.AssibleCollectionConfig') as p:
        for name in ['assible_collections.assible.builtin', 'assible_collections.testns.testcoll']:
            parent_pkg = name.rpartition('.')[0]
            module_to_load = name.rpartition('.')[2]
            paths = extend_paths(default_test_collection_paths, parent_pkg)
            existing_child_paths = [p for p in extend_paths(paths, module_to_load) if os.path.exists(p)]
            is_builtin = 'assible.builtin' in name
            if name in sys.modules:
                del sys.modules[name]
            loader = _AssibleCollectionPkgLoader(name, path_list=paths)
            assert repr(loader).startswith('_AssibleCollectionPkgLoader(path=')
            module = loader.load_module(name)
            assert module.__name__ == name
            assert isinstance(module.__loader__, _AssibleCollectionPkgLoader)
            if is_builtin:
                assert module.__path__ == []
            else:
                assert module.__path__ == [existing_child_paths[0]]

            assert module.__package__ == name
            if is_builtin:
                assert module.__file__ == '<assible_synthetic_collection_package>'
            else:
                assert module.__file__.endswith('__synthetic__') and os.path.isdir(os.path.dirname(module.__file__))
            assert sys.modules.get(name) == module

            assert hasattr(module, '_collection_meta') and isinstance(module._collection_meta, dict)

            # FIXME: validate _collection_meta contents match what's on disk (or not)

            # if the module has metadata, try loading it with busted metadata
            if module._collection_meta:
                _collection_finder = import_module('assible.utils.collection_loader._collection_finder')
                with patch.object(_collection_finder, '_meta_yml_to_dict', side_effect=Exception('bang')):
                    with pytest.raises(Exception) as ex:
                        _AssibleCollectionPkgLoader(name, path_list=paths).load_module(name)
                    assert 'error parsing collection metadata' in str(ex.value)


def test_coll_loader():
    with patch('assible.utils.collection_loader.AssibleCollectionConfig'):
        with pytest.raises(ValueError):
            # not a collection
            _AssibleCollectionLoader('assible_collections')

        with pytest.raises(ValueError):
            # bogus paths
            _AssibleCollectionLoader('assible_collections.testns.testcoll', path_list=[])

    # FIXME: more


def test_path_hook_setup():
    with patch.object(sys, 'path_hooks', []):
        found_hook = None
        pathhook_exc = None
        try:
            found_hook = _AssiblePathHookFinder._get_filefinder_path_hook()
        except Exception as phe:
            pathhook_exc = phe

        if PY3:
            assert str(pathhook_exc) == 'need exactly one FileFinder import hook (found 0)'
        else:
            assert found_hook is None

    assert repr(_AssiblePathHookFinder(object(), '/bogus/path')) == "_AssiblePathHookFinder(path='/bogus/path')"


def test_path_hook_importerror():
    # ensure that AssiblePathHookFinder.find_module swallows ImportError from path hook delegation on Py3, eg if the delegated
    # path hook gets passed a file on sys.path (python36.zip)
    reset_collections_loader_state()
    path_to_a_file = os.path.join(default_test_collection_paths[0], 'assible_collections/testns/testcoll/plugins/action/my_action.py')
    # it's a bug if the following pops an ImportError...
    assert _AssiblePathHookFinder(_AssibleCollectionFinder(), path_to_a_file).find_module('foo.bar.my_action') is None


def test_new_or_existing_module():
    module_name = 'blar.test.module'
    pkg_name = module_name.rpartition('.')[0]

    # create new module case
    nuke_module_prefix(module_name)
    with _AssibleCollectionPkgLoaderBase._new_or_existing_module(module_name, __package__=pkg_name) as new_module:
        # the module we just created should now exist in sys.modules
        assert sys.modules.get(module_name) is new_module
        assert new_module.__name__ == module_name

    # the module should stick since we didn't raise an exception in the contextmgr
    assert sys.modules.get(module_name) is new_module

    # reuse existing module case
    with _AssibleCollectionPkgLoaderBase._new_or_existing_module(module_name, __attr1__=42, blar='yo') as existing_module:
        assert sys.modules.get(module_name) is new_module  # should be the same module we created earlier
        assert hasattr(existing_module, '__package__') and existing_module.__package__ == pkg_name
        assert hasattr(existing_module, '__attr1__') and existing_module.__attr1__ == 42
        assert hasattr(existing_module, 'blar') and existing_module.blar == 'yo'

    # exception during update existing shouldn't zap existing module from sys.modules
    with pytest.raises(ValueError) as ve:
        with _AssibleCollectionPkgLoaderBase._new_or_existing_module(module_name) as existing_module:
            err_to_raise = ValueError('bang')
            raise err_to_raise
    # make sure we got our error
    assert ve.value is err_to_raise
    # and that the module still exists
    assert sys.modules.get(module_name) is existing_module

    # test module removal after exception during creation
    nuke_module_prefix(module_name)
    with pytest.raises(ValueError) as ve:
        with _AssibleCollectionPkgLoaderBase._new_or_existing_module(module_name) as new_module:
            err_to_raise = ValueError('bang')
            raise err_to_raise
    # make sure we got our error
    assert ve.value is err_to_raise
    # and that the module was removed
    assert sys.modules.get(module_name) is None


def test_iter_modules_impl():
    modules_trailer = 'assible_collections/testns/testcoll/plugins'
    modules_pkg_prefix = modules_trailer.replace('/', '.') + '.'
    modules_path = os.path.join(default_test_collection_paths[0], modules_trailer)
    modules = list(_iter_modules_impl([modules_path], modules_pkg_prefix))

    assert modules
    assert set([('assible_collections.testns.testcoll.plugins.action', True),
                ('assible_collections.testns.testcoll.plugins.module_utils', True),
                ('assible_collections.testns.testcoll.plugins.modules', True)]) == set(modules)

    modules_trailer = 'assible_collections/testns/testcoll/plugins/modules'
    modules_pkg_prefix = modules_trailer.replace('/', '.') + '.'
    modules_path = os.path.join(default_test_collection_paths[0], modules_trailer)
    modules = list(_iter_modules_impl([modules_path], modules_pkg_prefix))

    assert modules
    assert len(modules) == 1
    assert modules[0][0] == 'assible_collections.testns.testcoll.plugins.modules.amodule'  # name
    assert modules[0][1] is False  # is_pkg

    # FIXME: more


# BEGIN IN-CIRCUIT TESTS - these exercise behaviors of the loader when wired up to the import machinery


def test_import_from_collection(monkeypatch):
    collection_root = os.path.join(os.path.dirname(__file__), 'fixtures', 'collections')
    collection_path = os.path.join(collection_root, 'assible_collections/testns/testcoll/plugins/module_utils/my_util.py')

    # THIS IS UNSTABLE UNDER A DEBUGGER
    # the trace we're expecting to be generated when running the code below:
    # answer = question()
    expected_trace_log = [
        (collection_path, 5, 'call'),
        (collection_path, 6, 'line'),
        (collection_path, 6, 'return'),
    ]

    # define the collection root before any assible code has been loaded
    # otherwise config will have already been loaded and changing the environment will have no effect
    monkeypatch.setenv('ASSIBLE_COLLECTIONS_PATH', collection_root)

    finder = _AssibleCollectionFinder(paths=[collection_root])
    reset_collections_loader_state(finder)

    from assible_collections.testns.testcoll.plugins.module_utils.my_util import question

    original_trace_function = sys.gettrace()
    trace_log = []

    if original_trace_function:
        # enable tracing while preserving the existing trace function (coverage)
        def my_trace_function(frame, event, arg):
            trace_log.append((frame.f_code.co_filename, frame.f_lineno, event))

            # the original trace function expects to have itself set as the trace function
            sys.settrace(original_trace_function)
            # call the original trace function
            original_trace_function(frame, event, arg)
            # restore our trace function
            sys.settrace(my_trace_function)

            return my_trace_function
    else:
        # no existing trace function, so our trace function is much simpler
        def my_trace_function(frame, event, arg):
            trace_log.append((frame.f_code.co_filename, frame.f_lineno, event))

            return my_trace_function

    sys.settrace(my_trace_function)

    try:
        # run a minimal amount of code while the trace is running
        # adding more code here, including use of a context manager, will add more to our trace
        answer = question()
    finally:
        sys.settrace(original_trace_function)

    # make sure 'import ... as ...' works on builtin synthetic collections
    # the following import is not supported (it tries to find module_utils in assible.plugins)
    # import assible_collections.assible.builtin.plugins.module_utils as c1
    import assible_collections.assible.builtin.plugins.action as c2
    import assible_collections.assible.builtin.plugins as c3
    import assible_collections.assible.builtin as c4
    import assible_collections.assible as c5
    import assible_collections as c6

    # make sure 'import ...' works on builtin synthetic collections
    import assible_collections.assible.builtin.plugins.module_utils

    import assible_collections.assible.builtin.plugins.action
    assert assible_collections.assible.builtin.plugins.action == c3.action == c2

    import assible_collections.assible.builtin.plugins
    assert assible_collections.assible.builtin.plugins == c4.plugins == c3

    import assible_collections.assible.builtin
    assert assible_collections.assible.builtin == c5.builtin == c4

    import assible_collections.assible
    assert assible_collections.assible == c6.assible == c5

    import assible_collections
    assert assible_collections == c6

    # make sure 'from ... import ...' works on builtin synthetic collections
    from assible_collections.assible import builtin
    from assible_collections.assible.builtin import plugins
    assert builtin.plugins == plugins

    from assible_collections.assible.builtin.plugins import action
    from assible_collections.assible.builtin.plugins.action import command
    assert action.command == command

    from assible_collections.assible.builtin.plugins.module_utils import basic
    from assible_collections.assible.builtin.plugins.module_utils.basic import AssibleModule
    assert basic.AssibleModule == AssibleModule

    # make sure relative imports work from collections code
    # these require __package__ to be set correctly
    import assible_collections.testns.testcoll.plugins.module_utils.my_other_util
    import assible_collections.testns.testcoll.plugins.action.my_action

    # verify that code loaded from a collection does not inherit __future__ statements from the collection loader
    if sys.version_info[0] == 2:
        # if the collection code inherits the division future feature from the collection loader this will fail
        assert answer == 1
    else:
        assert answer == 1.5

    # verify that the filename and line number reported by the trace is correct
    # this makes sure that collection loading preserves file paths and line numbers
    assert trace_log == expected_trace_log


def test_eventsource():
    es = _EventSource()
    # fire when empty should succeed
    es.fire(42)
    handler1 = MagicMock()
    handler2 = MagicMock()
    es += handler1
    es.fire(99, my_kwarg='blah')
    handler1.assert_called_with(99, my_kwarg='blah')
    es += handler2
    es.fire(123, foo='bar')
    handler1.assert_called_with(123, foo='bar')
    handler2.assert_called_with(123, foo='bar')
    es -= handler2
    handler1.reset_mock()
    handler2.reset_mock()
    es.fire(123, foo='bar')
    handler1.assert_called_with(123, foo='bar')
    handler2.assert_not_called()
    es -= handler1
    handler1.reset_mock()
    es.fire('blah', kwarg=None)
    handler1.assert_not_called()
    handler2.assert_not_called()
    es -= handler1  # should succeed silently
    handler_bang = MagicMock(side_effect=Exception('bang'))
    es += handler_bang
    with pytest.raises(Exception) as ex:
        es.fire(123)
    assert 'bang' in str(ex.value)
    handler_bang.assert_called_with(123)
    with pytest.raises(ValueError):
        es += 42


def test_on_collection_load():
    finder = get_default_finder()
    reset_collections_loader_state(finder)

    load_handler = MagicMock()
    AssibleCollectionConfig.on_collection_load += load_handler

    m = import_module('assible_collections.testns.testcoll')
    load_handler.assert_called_once_with(collection_name='testns.testcoll', collection_path=os.path.dirname(m.__file__))

    _meta = _get_collection_metadata('testns.testcoll')
    assert _meta
    # FIXME: compare to disk

    finder = get_default_finder()
    reset_collections_loader_state(finder)

    AssibleCollectionConfig.on_collection_load += MagicMock(side_effect=Exception('bang'))
    with pytest.raises(Exception) as ex:
        import_module('assible_collections.testns.testcoll')
    assert 'bang' in str(ex.value)


def test_default_collection_config():
    finder = get_default_finder()
    reset_collections_loader_state(finder)
    assert AssibleCollectionConfig.default_collection is None
    AssibleCollectionConfig.default_collection = 'foo.bar'
    assert AssibleCollectionConfig.default_collection == 'foo.bar'
    with pytest.raises(ValueError):
        AssibleCollectionConfig.default_collection = 'bar.baz'


def test_default_collection_detection():
    finder = get_default_finder()
    reset_collections_loader_state(finder)

    # we're clearly not under a collection path
    assert _get_collection_name_from_path('/') is None

    # something that looks like a collection path but isn't importable by our finder
    assert _get_collection_name_from_path('/foo/assible_collections/bogusns/boguscoll/bar') is None

    # legit, at the top of the collection
    live_collection_path = os.path.join(os.path.dirname(__file__), 'fixtures/collections/assible_collections/testns/testcoll')
    assert _get_collection_name_from_path(live_collection_path) == 'testns.testcoll'

    # legit, deeper inside the collection
    live_collection_deep_path = os.path.join(live_collection_path, 'plugins/modules')
    assert _get_collection_name_from_path(live_collection_deep_path) == 'testns.testcoll'

    # this one should be hidden by the real testns.testcoll, so should not resolve
    masked_collection_path = os.path.join(os.path.dirname(__file__), 'fixtures/collections_masked/assible_collections/testns/testcoll')
    assert _get_collection_name_from_path(masked_collection_path) is None


@pytest.mark.parametrize(
    'role_name,collection_list,expected_collection_name,expected_path_suffix',
    [
        ('some_role', ['testns.testcoll', 'assible.bogus'], 'testns.testcoll', 'testns/testcoll/roles/some_role'),
        ('testns.testcoll.some_role', ['assible.bogus', 'testns.testcoll'], 'testns.testcoll', 'testns/testcoll/roles/some_role'),
        ('testns.testcoll.some_role', [], 'testns.testcoll', 'testns/testcoll/roles/some_role'),
        ('testns.testcoll.some_role', None, 'testns.testcoll', 'testns/testcoll/roles/some_role'),
        ('some_role', [], None, None),
        ('some_role', None, None, None),
    ])
def test_collection_role_name_location(role_name, collection_list, expected_collection_name, expected_path_suffix):
    finder = get_default_finder()
    reset_collections_loader_state(finder)

    expected_path = None
    if expected_path_suffix:
        expected_path = os.path.join(os.path.dirname(__file__), 'fixtures/collections/assible_collections', expected_path_suffix)

    found = _get_collection_role_path(role_name, collection_list)

    if found:
        assert found[0] == role_name.rpartition('.')[2]
        assert found[1] == expected_path
        assert found[2] == expected_collection_name
    else:
        assert expected_collection_name is None and expected_path_suffix is None


def test_bogus_imports():
    finder = get_default_finder()
    reset_collections_loader_state(finder)

    # ensure ImportError on known-bogus imports
    bogus_imports = ['bogus_toplevel', 'assible_collections.bogusns', 'assible_collections.testns.boguscoll',
                     'assible_collections.testns.testcoll.bogussub', 'assible_collections.assible.builtin.bogussub']
    for bogus_import in bogus_imports:
        with pytest.raises(ImportError):
            import_module(bogus_import)


def test_empty_vs_no_code():
    finder = get_default_finder()
    reset_collections_loader_state(finder)

    from assible_collections.testns import testcoll  # synthetic package with no code on disk
    from assible_collections.testns.testcoll.plugins import module_utils  # real package with empty code file

    # ensure synthetic packages have no code object at all (prevent bogus coverage entries)
    assert testcoll.__loader__.get_source(testcoll.__name__) is None
    assert testcoll.__loader__.get_code(testcoll.__name__) is None

    # ensure empty package inits do have a code object
    assert module_utils.__loader__.get_source(module_utils.__name__) == b''
    assert module_utils.__loader__.get_code(module_utils.__name__) is not None


def test_finder_playbook_paths():
    finder = get_default_finder()
    reset_collections_loader_state(finder)

    import assible_collections
    import assible_collections.assible
    import assible_collections.testns

    # ensure the package modules look like we expect
    assert hasattr(assible_collections, '__path__') and len(assible_collections.__path__) > 0
    assert hasattr(assible_collections.assible, '__path__') and len(assible_collections.assible.__path__) > 0
    assert hasattr(assible_collections.testns, '__path__') and len(assible_collections.testns.__path__) > 0

    # these shouldn't be visible yet, since we haven't added the playbook dir
    with pytest.raises(ImportError):
        import assible_collections.assible.playbook_adj_other

    with pytest.raises(ImportError):
        import assible_collections.testns.playbook_adj_other

    assert AssibleCollectionConfig.playbook_paths == []
    playbook_path_fixture_dir = os.path.join(os.path.dirname(__file__), 'fixtures/playbook_path')

    # configure the playbook paths
    AssibleCollectionConfig.playbook_paths = [playbook_path_fixture_dir]

    # playbook paths go to the front of the line
    assert AssibleCollectionConfig.collection_paths[0] == os.path.join(playbook_path_fixture_dir, 'collections')

    # playbook paths should be updated on the existing root assible_collections path, as well as on the 'assible' namespace (but no others!)
    assert assible_collections.__path__[0] == os.path.join(playbook_path_fixture_dir, 'collections/assible_collections')
    assert assible_collections.assible.__path__[0] == os.path.join(playbook_path_fixture_dir, 'collections/assible_collections/assible')
    assert all('playbook_path' not in p for p in assible_collections.testns.__path__)

    # should succeed since we fixed up the package path
    import assible_collections.assible.playbook_adj_other
    # should succeed since we didn't import freshns before hacking in the path
    import assible_collections.freshns.playbook_adj_other
    # should fail since we've already imported something from this path and didn't fix up its package path
    with pytest.raises(ImportError):
        import assible_collections.testns.playbook_adj_other


def test_toplevel_iter_modules():
    finder = get_default_finder()
    reset_collections_loader_state(finder)

    modules = list(pkgutil.iter_modules(default_test_collection_paths, ''))
    assert len(modules) == 1
    assert modules[0][1] == 'assible_collections'


def test_iter_modules_namespaces():
    finder = get_default_finder()
    reset_collections_loader_state(finder)

    paths = extend_paths(default_test_collection_paths, 'assible_collections')
    modules = list(pkgutil.iter_modules(paths, 'assible_collections.'))
    assert len(modules) == 2
    assert all(m[2] is True for m in modules)
    assert all(isinstance(m[0], _AssiblePathHookFinder) for m in modules)
    assert set(['assible_collections.testns', 'assible_collections.assible']) == set(m[1] for m in modules)


def test_collection_get_data():
    finder = get_default_finder()
    reset_collections_loader_state(finder)

    # something that's there
    d = pkgutil.get_data('assible_collections.testns.testcoll', 'plugins/action/my_action.py')
    assert b'hello from my_action.py' in d

    # something that's not there
    d = pkgutil.get_data('assible_collections.testns.testcoll', 'bogus/bogus')
    assert d is None

    with pytest.raises(ValueError):
        plugins_pkg = import_module('assible_collections.assible.builtin')
        assert not os.path.exists(os.path.dirname(plugins_pkg.__file__))
        d = pkgutil.get_data('assible_collections.assible.builtin', 'plugins/connection/local.py')


@pytest.mark.parametrize(
    'ref,ref_type,expected_collection,expected_subdirs,expected_resource,expected_python_pkg_name',
    [
        ('ns.coll.myaction', 'action', 'ns.coll', '', 'myaction', 'assible_collections.ns.coll.plugins.action'),
        ('ns.coll.subdir1.subdir2.myaction', 'action', 'ns.coll', 'subdir1.subdir2', 'myaction', 'assible_collections.ns.coll.plugins.action.subdir1.subdir2'),
        ('ns.coll.myrole', 'role', 'ns.coll', '', 'myrole', 'assible_collections.ns.coll.roles.myrole'),
        ('ns.coll.subdir1.subdir2.myrole', 'role', 'ns.coll', 'subdir1.subdir2', 'myrole', 'assible_collections.ns.coll.roles.subdir1.subdir2.myrole'),
    ])
def test_fqcr_parsing_valid(ref, ref_type, expected_collection,
                            expected_subdirs, expected_resource, expected_python_pkg_name):
    assert AssibleCollectionRef.is_valid_fqcr(ref, ref_type)

    r = AssibleCollectionRef.from_fqcr(ref, ref_type)
    assert r.collection == expected_collection
    assert r.subdirs == expected_subdirs
    assert r.resource == expected_resource
    assert r.n_python_package_name == expected_python_pkg_name

    r = AssibleCollectionRef.try_parse_fqcr(ref, ref_type)
    assert r.collection == expected_collection
    assert r.subdirs == expected_subdirs
    assert r.resource == expected_resource
    assert r.n_python_package_name == expected_python_pkg_name


@pytest.mark.parametrize(
    'ref,ref_type,expected_error_type,expected_error_expression',
    [
        ('no_dots_at_all_action', 'action', ValueError, 'is not a valid collection reference'),
        ('no_nscoll.myaction', 'action', ValueError, 'is not a valid collection reference'),
        ('ns.coll.myaction', 'bogus', ValueError, 'invalid collection ref_type'),
    ])
def test_fqcr_parsing_invalid(ref, ref_type, expected_error_type, expected_error_expression):
    assert not AssibleCollectionRef.is_valid_fqcr(ref, ref_type)

    with pytest.raises(expected_error_type) as curerr:
        AssibleCollectionRef.from_fqcr(ref, ref_type)

    assert re.search(expected_error_expression, str(curerr.value))

    r = AssibleCollectionRef.try_parse_fqcr(ref, ref_type)
    assert r is None


@pytest.mark.parametrize(
    'name,subdirs,resource,ref_type,python_pkg_name',
    [
        ('ns.coll', None, 'res', 'doc_fragments', 'assible_collections.ns.coll.plugins.doc_fragments'),
        ('ns.coll', 'subdir1', 'res', 'doc_fragments', 'assible_collections.ns.coll.plugins.doc_fragments.subdir1'),
        ('ns.coll', 'subdir1.subdir2', 'res', 'action', 'assible_collections.ns.coll.plugins.action.subdir1.subdir2'),
    ])
def test_collectionref_components_valid(name, subdirs, resource, ref_type, python_pkg_name):
    x = AssibleCollectionRef(name, subdirs, resource, ref_type)

    assert x.collection == name
    if subdirs:
        assert x.subdirs == subdirs
    else:
        assert x.subdirs == ''

    assert x.resource == resource
    assert x.ref_type == ref_type
    assert x.n_python_package_name == python_pkg_name


@pytest.mark.parametrize(
    'dirname,expected_result',
    [
        ('become_plugins', 'become'),
        ('cache_plugins', 'cache'),
        ('connection_plugins', 'connection'),
        ('library', 'modules'),
        ('filter_plugins', 'filter'),
        ('bogus_plugins', ValueError),
        (None, ValueError)
    ]
)
def test_legacy_plugin_dir_to_plugin_type(dirname, expected_result):
    if isinstance(expected_result, string_types):
        assert AssibleCollectionRef.legacy_plugin_dir_to_plugin_type(dirname) == expected_result
    else:
        with pytest.raises(expected_result):
            AssibleCollectionRef.legacy_plugin_dir_to_plugin_type(dirname)


@pytest.mark.parametrize(
    'name,subdirs,resource,ref_type,expected_error_type,expected_error_expression',
    [
        ('bad_ns', '', 'resource', 'action', ValueError, 'invalid collection name'),
        ('ns.coll.', '', 'resource', 'action', ValueError, 'invalid collection name'),
        ('ns.coll', 'badsubdir#', 'resource', 'action', ValueError, 'invalid subdirs entry'),
        ('ns.coll', 'badsubdir.', 'resource', 'action', ValueError, 'invalid subdirs entry'),
        ('ns.coll', '.badsubdir', 'resource', 'action', ValueError, 'invalid subdirs entry'),
        ('ns.coll', '', 'resource', 'bogus', ValueError, 'invalid collection ref_type'),
    ])
def test_collectionref_components_invalid(name, subdirs, resource, ref_type, expected_error_type, expected_error_expression):
    with pytest.raises(expected_error_type) as curerr:
        AssibleCollectionRef(name, subdirs, resource, ref_type)

    assert re.search(expected_error_expression, str(curerr.value))


# BEGIN TEST SUPPORT

default_test_collection_paths = [
    os.path.join(os.path.dirname(__file__), 'fixtures', 'collections'),
    os.path.join(os.path.dirname(__file__), 'fixtures', 'collections_masked'),
    '/bogus/bogussub'
]


def get_default_finder():
    return _AssibleCollectionFinder(paths=default_test_collection_paths)


def extend_paths(path_list, suffix):
    suffix = suffix.replace('.', '/')
    return [os.path.join(p, suffix) for p in path_list]


def nuke_module_prefix(prefix):
    for module_to_nuke in [m for m in sys.modules if m.startswith(prefix)]:
        sys.modules.pop(module_to_nuke)


def reset_collections_loader_state(metapath_finder=None):
    _AssibleCollectionFinder._remove()

    nuke_module_prefix('assible_collections')
    nuke_module_prefix('assible.modules')
    nuke_module_prefix('assible.plugins')

    # FIXME: better to move this someplace else that gets cleaned up automatically?
    _AssibleCollectionLoader._redirected_package_map = {}

    AssibleCollectionConfig._default_collection = None
    AssibleCollectionConfig._on_collection_load = _EventSource()

    if metapath_finder:
        metapath_finder._install()
