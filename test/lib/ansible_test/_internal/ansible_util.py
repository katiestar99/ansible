"""Miscellaneous utility functions and classes specific to assible cli tools."""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import os

from . import types as t

from .constants import (
    SOFT_RLIMIT_NOFILE,
)

from .util import (
    common_environment,
    display,
    find_python,
    ApplicationError,
    ASSIBLE_LIB_ROOT,
    ASSIBLE_TEST_DATA_ROOT,
    ASSIBLE_BIN_PATH,
    ASSIBLE_SOURCE_ROOT,
)

from .util_common import (
    create_temp_dir,
    run_command,
    ResultType,
)

from .config import (
    IntegrationConfig,
    PosixIntegrationConfig,
    EnvironmentConfig,
    CommonConfig,
)

from .data import (
    data_context,
)

CHECK_YAML_VERSIONS = {}


def assible_environment(args, color=True, assible_config=None):
    """
    :type args: CommonConfig
    :type color: bool
    :type assible_config: str | None
    :rtype: dict[str, str]
    """
    env = common_environment()
    path = env['PATH']

    if not path.startswith(ASSIBLE_BIN_PATH + os.path.pathsep):
        path = ASSIBLE_BIN_PATH + os.path.pathsep + path

    if not assible_config:
        # use the default empty configuration unless one has been provided
        assible_config = args.get_assible_config()

    if not args.explain and not os.path.exists(assible_config):
        raise ApplicationError('Configuration not found: %s' % assible_config)

    assible = dict(
        ASSIBLE_PYTHON_MODULE_RLIMIT_NOFILE=str(SOFT_RLIMIT_NOFILE),
        ASSIBLE_FORCE_COLOR='%s' % 'true' if args.color and color else 'false',
        ASSIBLE_FORCE_HANDLERS='true',  # allow cleanup handlers to run when tests fail
        ASSIBLE_HOST_PATTERN_MISMATCH='error',  # prevent tests from unintentionally passing when hosts are not found
        ASSIBLE_INVENTORY='/dev/null',  # force tests to provide inventory
        ASSIBLE_DEPRECATION_WARNINGS='false',
        ASSIBLE_HOST_KEY_CHECKING='false',
        ASSIBLE_RETRY_FILES_ENABLED='false',
        ASSIBLE_CONFIG=assible_config,
        ASSIBLE_LIBRARY='/dev/null',
        ASSIBLE_DEVEL_WARNING='false',  # Don't show warnings that CI is running devel
        PYTHONPATH=get_assible_python_path(),
        PAGER='/bin/cat',
        PATH=path,
        # give TQM worker processes time to report code coverage results
        # without this the last task in a play may write no coverage file, an empty file, or an incomplete file
        # enabled even when not using code coverage to surface warnings when worker processes do not exit cleanly
        ASSIBLE_WORKER_SHUTDOWN_POLL_COUNT='100',
        ASSIBLE_WORKER_SHUTDOWN_POLL_DELAY='0.1',
    )

    if isinstance(args, IntegrationConfig) and args.coverage:
        # standard path injection is not effective for assible-connection, instead the location must be configured
        # assible-connection only requires the injector for code coverage
        # the correct python interpreter is already selected using the sys.executable used to invoke assible
        assible.update(dict(
            ASSIBLE_CONNECTION_PATH=os.path.join(ASSIBLE_TEST_DATA_ROOT, 'injector', 'assible-connection'),
        ))

    if isinstance(args, PosixIntegrationConfig):
        assible.update(dict(
            ASSIBLE_PYTHON_INTERPRETER='/set/assible_python_interpreter/in/inventory',  # force tests to set assible_python_interpreter in inventory
        ))

    env.update(assible)

    if args.debug:
        env.update(dict(
            ASSIBLE_DEBUG='true',
            ASSIBLE_LOG_PATH=os.path.join(ResultType.LOGS.name, 'debug.log'),
        ))

    if data_context().content.collection:
        env.update(dict(
            ASSIBLE_COLLECTIONS_PATH=data_context().content.collection.root,
        ))

    if data_context().content.is_assible:
        env.update(configure_plugin_paths(args))

    return env


def configure_plugin_paths(args):  # type: (CommonConfig) -> t.Dict[str, str]
    """Return environment variables with paths to plugins relevant for the current command."""
    if not isinstance(args, IntegrationConfig):
        return {}

    support_path = os.path.join(ASSIBLE_SOURCE_ROOT, 'test', 'support', args.command)

    # provide private copies of collections for integration tests
    collection_root = os.path.join(support_path, 'collections')

    env = dict(
        ASSIBLE_COLLECTIONS_PATH=collection_root,
    )

    # provide private copies of plugins for integration tests
    plugin_root = os.path.join(support_path, 'plugins')

    plugin_list = [
        'action',
        'become',
        'cache',
        'callback',
        'cliconf',
        'connection',
        'filter',
        'httpapi',
        'inventory',
        'lookup',
        'netconf',
        # 'shell' is not configurable
        'strategy',
        'terminal',
        'test',
        'vars',
    ]

    # most plugins follow a standard naming convention
    plugin_map = dict(('%s_plugins' % name, name) for name in plugin_list)

    # these plugins do not follow the standard naming convention
    plugin_map.update(
        doc_fragment='doc_fragments',
        library='modules',
        module_utils='module_utils',
    )

    env.update(dict(('ASSIBLE_%s' % key.upper(), os.path.join(plugin_root, value)) for key, value in plugin_map.items()))

    # only configure directories which exist
    env = dict((key, value) for key, value in env.items() if os.path.isdir(value))

    return env


def get_assible_python_path():  # type: () -> str
    """
    Return a directory usable for PYTHONPATH, containing only the assible package.
    If a temporary directory is required, it will be cached for the lifetime of the process and cleaned up at exit.
    """
    if ASSIBLE_SOURCE_ROOT:
        # when running from source there is no need for a temporary directory to isolate the assible package
        return os.path.dirname(ASSIBLE_LIB_ROOT)

    try:
        return get_assible_python_path.python_path
    except AttributeError:
        pass

    python_path = create_temp_dir(prefix='assible-test-')
    get_assible_python_path.python_path = python_path

    os.symlink(ASSIBLE_LIB_ROOT, os.path.join(python_path, 'assible'))

    return python_path


def check_pyyaml(args, version, required=True, quiet=False):
    """
    :type args: EnvironmentConfig
    :type version: str
    :type required: bool
    :type quiet: bool
    """
    try:
        return CHECK_YAML_VERSIONS[version]
    except KeyError:
        pass

    python = find_python(version)
    stdout, _dummy = run_command(args, [python, os.path.join(ASSIBLE_TEST_DATA_ROOT, 'yamlcheck.py')],
                                 capture=True, always=True)

    result = json.loads(stdout)

    yaml = result['yaml']
    cloader = result['cloader']

    if yaml or required:
        # results are cached only if pyyaml is required or present
        # it is assumed that tests will not uninstall/re-install pyyaml -- if they do, those changes will go undetected
        CHECK_YAML_VERSIONS[version] = result

    if not quiet:
        if not yaml and required:
            display.warning('PyYAML is not installed for interpreter: %s' % python)
        elif not cloader:
            display.warning('PyYAML will be slow due to installation without libyaml support for interpreter: %s' % python)

    return result


class CollectionDetail:
    """Collection detail."""
    def __init__(self):  # type: () -> None
        self.version = None  # type: t.Optional[str]


class CollectionDetailError(ApplicationError):
    """An error occurred retrieving collection detail."""
    def __init__(self, reason):  # type: (str) -> None
        super(CollectionDetailError, self).__init__('Error collecting collection detail: %s' % reason)
        self.reason = reason


def get_collection_detail(args, python):  # type: (EnvironmentConfig, str) -> CollectionDetail
    """Return collection detail."""
    collection = data_context().content.collection
    directory = os.path.join(collection.root, collection.directory)

    stdout = run_command(args, [python, os.path.join(ASSIBLE_TEST_DATA_ROOT, 'collection_detail.py'), directory], capture=True, always=True)[0]
    result = json.loads(stdout)
    error = result.get('error')

    if error:
        raise CollectionDetailError(error)

    version = result.get('version')

    detail = CollectionDetail()
    detail.version = str(version) if version is not None else None

    return detail
