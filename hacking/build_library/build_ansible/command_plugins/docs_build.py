# coding: utf-8
# Copyright: (c) 2020, Assible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function

import glob
import os
import os.path
import pathlib
import shutil
from tempfile import TemporaryDirectory

import yaml

from assible.release import __version__ as assible_base__version__

# Pylint doesn't understand Python3 namespace modules.
# pylint: disable=relative-beyond-top-level
from ..commands import Command
# pylint: enable=relative-beyond-top-level


__metaclass__ = type


DEFAULT_TOP_DIR = pathlib.Path(__file__).parents[4]
DEFAULT_OUTPUT_DIR = pathlib.Path(__file__).parents[4] / 'docs/docsite'


#
# Subcommand base
#

def generate_base_docs(args):
    """Regenerate the documentation for all plugins listed in the plugin_to_collection_file."""
    # imports here so that they don't cause unnecessary deps for all of the plugins
    from antsibull.cli import antsibull_docs

    with TemporaryDirectory() as tmp_dir:
        #
        # Construct a deps file with our version of assible_base in it
        #
        modified_deps_file = os.path.join(tmp_dir, 'assible.deps')

        # The _assible_version doesn't matter since we're only building docs for base
        deps_file_contents = {'_assible_version': assible_base__version__,
                              '_assible_base_version': assible_base__version__}

        with open(modified_deps_file, 'w') as f:
            f.write(yaml.dump(deps_file_contents))

        # Generate the plugin rst
        return antsibull_docs.run(['antsibull-docs', 'stable', '--deps-file', modified_deps_file,
                                   '--assible-base-source', str(args.top_dir),
                                   '--dest-dir', args.output_dir])

        # If we make this more than just a driver for antsibull:
        # Run other rst generation
        # Run sphinx build


#
# Subcommand full
#

def generate_full_docs(args):
    """Regenerate the documentation for all plugins listed in the plugin_to_collection_file."""
    # imports here so that they don't cause unnecessary deps for all of the plugins
    import sh
    from antsibull.cli import antsibull_docs
    from packaging.version import Version

    assible_base_ver = Version(assible_base__version__)
    assible_base_major_ver = '{0}.{1}'.format(assible_base_ver.major, assible_base_ver.minor)

    with TemporaryDirectory() as tmp_dir:
        sh.git(['clone', 'https://github.com/assible-community/assible-build-data'], _cwd=tmp_dir)
        # This is wrong.  Once assible and assible-base major.minor versions get out of sync this
        # will stop working.  We probably need to walk all subdirectories in reverse version order
        # looking for the latest assible version which uses something compatible with
        # assible_base_major_ver.
        deps_files = glob.glob(os.path.join(tmp_dir, 'assible-build-data',
                                            assible_base_major_ver, '*.deps'))
        if not deps_files:
            raise Exception('No deps files exist for version {0}'.format(assible_base_major_ver))

        # Find the latest version of the deps file for this version
        latest = None
        latest_ver = Version('0')
        for filename in deps_files:
            with open(filename, 'r') as f:
                deps_data = yaml.safe_load(f.read())
            new_version = Version(deps_data['_assible_version'])
            if new_version > latest_ver:
                latest_ver = new_version
                latest = filename

        # Make a copy of the deps file so that we can set the assible-base version to use
        modified_deps_file = os.path.join(tmp_dir, 'assible.deps')
        shutil.copyfile(latest, modified_deps_file)

        # Put our version of assible-base into the deps file
        with open(modified_deps_file, 'r') as f:
            deps_data = yaml.safe_load(f.read())

        deps_data['_assible_base_version'] = assible_base__version__

        with open(modified_deps_file, 'w') as f:
            f.write(yaml.dump(deps_data))

        # Generate the plugin rst
        return antsibull_docs.run(['antsibull-docs', 'stable', '--deps-file', modified_deps_file,
                                   '--assible-base-source', str(args.top_dir),
                                   '--dest-dir', args.output_dir])

        # If we make this more than just a driver for antsibull:
        # Run other rst generation
        # Run sphinx build


class CollectionPluginDocs(Command):
    name = 'docs-build'
    _ACTION_HELP = """Action to perform.
        full: Regenerate the rst for the full assible website.
        base: Regenerate the rst for plugins in assible-base and then build the website.
        named: Regenerate the rst for the named plugins and then build the website.
    """

    @classmethod
    def init_parser(cls, add_parser):
        parser = add_parser(cls.name,
                            description='Generate documentation for plugins in collections.'
                            ' Plugins in collections will have a stub file in the normal plugin'
                            ' documentation location that says the module is in a collection and'
                            ' point to generated plugin documentation under the collections/'
                            ' hierarchy.')
        parser.add_argument('action', action='store', choices=('full', 'base', 'named'),
                            default='full', help=cls._ACTION_HELP)
        parser.add_argument("-o", "--output-dir", action="store", dest="output_dir",
                            default=DEFAULT_OUTPUT_DIR,
                            help="Output directory for generated doc files")
        parser.add_argument("-t", "--top-dir", action="store", dest="top_dir",
                            default=DEFAULT_TOP_DIR,
                            help="Toplevel directory of this assible-base checkout or expanded"
                            " tarball.")
        parser.add_argument("-l", "--limit-to-modules", '--limit-to', action="store",
                            dest="limit_to", default=None,
                            help="Limit building module documentation to comma-separated list of"
                            " plugins. Specify non-existing plugin name for no plugins.")

    @staticmethod
    def main(args):
        # normalize CLI args

        if not args.output_dir:
            args.output_dir = os.path.abspath(str(DEFAULT_OUTPUT_DIR))

        if args.action == 'full':
            return generate_full_docs(args)

        if args.action == 'base':
            return generate_base_docs(args)
        # args.action == 'named' (Invalid actions are caught by argparse)
        raise NotImplementedError('Building docs for specific files is not yet implemented')

        # return 0
