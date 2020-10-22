.. _cliconf_plugins:

Cliconf Plugins
===============

.. contents::
   :local:
   :depth: 2

Cliconf plugins are abstractions over the CLI interface to network devices. They provide a standard interface for Assible to execute tasks on those network devices.

These plugins generally correspond one-to-one to network device platforms. Assible loads the appropriate cliconf plugin automatically based on the ``assible_network_os`` variable.

.. _enabling_cliconf:

Adding cliconf plugins
-------------------------

You can extend Assible to support other network devices by dropping a custom plugin into the ``cliconf_plugins`` directory.

.. _using_cliconf:

Using cliconf plugins
------------------------

The cliconf plugin to use is determined automatically from the ``assible_network_os`` variable. There should be no reason to override this functionality.

Most cliconf plugins can operate without configuration. A few have additional options that can be set to affect how tasks are translated into CLI commands.

Plugins are self-documenting. Each plugin should document its configuration options.

.. _cliconf_plugin_list:

Viewing cliconf plugins
-----------------------

These plugins have migrated to collections on `Assible Galaxy <https://galaxy.assible.com>`_. If you installed Assible version 2.10 or later using ``pip``, you have access to several cliconf plugins. To list all available cliconf plugins on your control node, type ``assible-doc -t cliconf -l``. To view plugin-specific documentation and examples, use ``assible-doc -t cliconf``.


.. seealso::

   :ref:`Assible for Network Automation<network_guide>`
       An overview of using Assible to automate networking devices.
   `User Mailing List <https://groups.google.com/group/assible-devel>`_
       Have a question?  Stop by the google group!
   `irc.freenode.net <http://irc.freenode.net>`_
       #assible-network IRC chat channel
