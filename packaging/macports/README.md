This portfile installs assible from the git repository, it will install the
latest and greatest version of assible. This portfile does not install the
required dependencies to run in accelerated mode.

## Installing the stable version of assible via macports

If you wish to run a stable version of assible please do the following

First update your macports repo to the latest versions

  $ sudo port sync

Then install assible

  $ sudo port install assible

## Installing the devel version of assible via macports

To use this Portfile to install the development version of assible one should
follow the instructions at
<http://guide.macports.org/#development.local-repositories>

The basic idea is to add the _assible/packaging/macports_ directory to your
_/opt/local/etc/macports/sources.conf_ file. You should have something similar
to this at the end of the file

  file:///Users/jtang/develop/assible/packaging/macports
  rsync://rsync.macports.org/release/tarballs/ports.tar [default]

In the _assible/packaging/macports_ directory, do this

  $ portindex

Once the index is created the _Portfile_ will override the one in the upstream
macports repository.

Installing newer development versions should involve an uninstall, clean,
install process or else the Portfile will need its version number/epoch
bumped.
