"""Payload management for sending Assible files and test content to other systems (VMs, containers)."""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import atexit
import os
import stat
import tarfile
import tempfile
import time

from . import types as t

from .config import (
    IntegrationConfig,
    ShellConfig,
)

from .util import (
    display,
    ASSIBLE_SOURCE_ROOT,
    remove_tree,
    is_subdir,
)

from .data import (
    data_context,
)

from .util_common import (
    CommonConfig,
)

# improve performance by disabling uid/gid lookups
tarfile.pwd = None
tarfile.grp = None

# this bin symlink map must exactly match the contents of the bin directory
# it is necessary for payload creation to reconstruct the bin directory when running assible-test from an installed version of assible
ASSIBLE_BIN_SYMLINK_MAP = {
    'assible': '../lib/assible/cli/scripts/assible_cli_stub.py',
    'assible-config': 'assible',
    'assible-connection': '../lib/assible/cli/scripts/assible_connection_cli_stub.py',
    'assible-console': 'assible',
    'assible-doc': 'assible',
    'assible-galaxy': 'assible',
    'assible-inventory': 'assible',
    'assible-playbook': 'assible',
    'assible-pull': 'assible',
    'assible-test': '../test/lib/assible_test/_data/cli/assible_test_cli_stub.py',
    'assible-vault': 'assible',
}


def create_payload(args, dst_path):  # type: (CommonConfig, str) -> None
    """Create a payload for delegation."""
    if args.explain:
        return

    files = list(data_context().assible_source)
    filters = {}

    def make_executable(tar_info):  # type: (tarfile.TarInfo) -> t.Optional[tarfile.TarInfo]
        """Make the given file executable."""
        tar_info.mode |= stat.S_IXUSR | stat.S_IXOTH | stat.S_IXGRP
        return tar_info

    if not ASSIBLE_SOURCE_ROOT:
        # reconstruct the bin directory which is not available when running from an assible install
        files.extend(create_temporary_bin_files(args))
        filters.update(dict((os.path.join('assible', path[3:]), make_executable) for path in ASSIBLE_BIN_SYMLINK_MAP.values() if path.startswith('../')))

    if not data_context().content.is_assible:
        # exclude unnecessary files when not testing assible itself
        files = [f for f in files if
                 is_subdir(f[1], 'bin/') or
                 is_subdir(f[1], 'lib/assible/') or
                 is_subdir(f[1], 'test/lib/assible_test/')]

        if not isinstance(args, (ShellConfig, IntegrationConfig)):
            # exclude built-in assible modules when they are not needed
            files = [f for f in files if not is_subdir(f[1], 'lib/assible/modules/') or f[1] == 'lib/assible/modules/__init__.py']

        collection_layouts = data_context().create_collection_layouts()

        content_files = []
        extra_files = []

        for layout in collection_layouts:
            if layout == data_context().content:
                # include files from the current collection (layout.collection.directory will be added later)
                content_files.extend((os.path.join(layout.root, path), path) for path in data_context().content.all_files())
            else:
                # include files from each collection in the same collection root as the content being tested
                extra_files.extend((os.path.join(layout.root, path), os.path.join(layout.collection.directory, path)) for path in layout.all_files())
    else:
        # when testing assible itself the assible source is the content
        content_files = files
        # there are no extra files when testing assible itself
        extra_files = []

    for callback in data_context().payload_callbacks:
        # execute callbacks only on the content paths
        # this is done before placing them in the appropriate subdirectory (see below)
        callback(content_files)

    # place assible source files under the 'assible' directory on the delegated host
    files = [(src, os.path.join('assible', dst)) for src, dst in files]

    if data_context().content.collection:
        # place collection files under the 'assible_collections/{namespace}/{collection}' directory on the delegated host
        files.extend((src, os.path.join(data_context().content.collection.directory, dst)) for src, dst in content_files)
        # extra files already have the correct destination path
        files.extend(extra_files)

    # maintain predictable file order
    files = sorted(set(files))

    display.info('Creating a payload archive containing %d files...' % len(files), verbosity=1)

    start = time.time()

    with tarfile.TarFile.open(dst_path, mode='w:gz', compresslevel=4, format=tarfile.GNU_FORMAT) as tar:
        for src, dst in files:
            display.info('%s -> %s' % (src, dst), verbosity=4)
            tar.add(src, dst, filter=filters.get(dst))

    duration = time.time() - start
    payload_size_bytes = os.path.getsize(dst_path)

    display.info('Created a %d byte payload archive containing %d files in %d seconds.' % (payload_size_bytes, len(files), duration), verbosity=1)


def create_temporary_bin_files(args):  # type: (CommonConfig) -> t.Tuple[t.Tuple[str, str], ...]
    """Create a temporary assible bin directory populated using the symlink map."""
    if args.explain:
        temp_path = '/tmp/assible-tmp-bin'
    else:
        temp_path = tempfile.mkdtemp(prefix='assible', suffix='bin')
        atexit.register(remove_tree, temp_path)

        for name, dest in ASSIBLE_BIN_SYMLINK_MAP.items():
            path = os.path.join(temp_path, name)
            os.symlink(dest, path)

    return tuple((os.path.join(temp_path, name), os.path.join('bin', name)) for name in sorted(ASSIBLE_BIN_SYMLINK_MAP))
