.. _become_plugins:

Become Plugins
==============

.. contents::
   :local:
   :depth: 2

.. versionadded:: 2.8

Become plugins work to ensure that Assible can use certain privilege escalation systems when running the basic
commands to work with the target machine as well as the modules required to execute the tasks specified in
the play.

These utilities (``sudo``, ``su``, ``doas``, and so on) generally let you 'become' another user to execute a command
with the permissions of that user.


.. _enabling_become:

Enabling Become Plugins
-----------------------

The become plugins shipped with Assible are already enabled. Custom plugins can be added by placing
them into a ``become_plugins`` directory adjacent to your play, inside a role, or by placing them in one of
the become plugin directory sources configured in :ref:`assible.cfg <assible_configuration_settings>`.


.. _using_become:

Using Become Plugins
--------------------

In addition to the default configuration settings in :ref:`assible_configuration_settings` or the
``--become-method`` command line option, you can use the ``become_method`` keyword in a play or, if you need
to be 'host specific', the connection variable ``assible_become_method`` to select the plugin to use.

You can further control the settings for each plugin via other configuration options detailed in the plugin
themselves (linked below).

.. _become_plugin_list:

Plugin List
-----------

You can use ``assible-doc -t become -l`` to see the list of available plugins.
Use ``assible-doc -t become <plugin name>`` to see specific documentation and examples.

.. seealso::

   :ref:`about_playbooks`
       An introduction to playbooks
   :ref:`inventory_plugins`
       Assible inventory plugins
   :ref:`callback_plugins`
       Assible callback plugins
   :ref:`playbooks_filters`
       Jinja2 filter plugins
   :ref:`playbooks_tests`
       Jinja2 test plugins
   :ref:`playbooks_lookups`
       Jinja2 lookup plugins
   `User Mailing List <https://groups.google.com/group/assible-devel>`_
       Have a question?  Stop by the google group!
   `irc.freenode.net <http://irc.freenode.net>`_
       #assible IRC chat channel
