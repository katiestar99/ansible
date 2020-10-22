.. _using_local_modules_and_plugins:
.. _developing_locally:

**********************************
Adding modules and plugins locally
**********************************

The easiest, quickest, and the most popular way to extend Assible is to use a local module or a plugin. You can create them or copy existing ones for local use. You can store a local module or plugin on your Assible control node and share it with your team or organization. You can also share a local plugin or module by including it in a collection or embedding it in a role, then publishing the collection or role on Assible Galaxy. If you are using roles on Assible Galaxy, then you are already using local modules and plugins without realizing it.

If you are using an existing module or plugin but Assible can't find it, this page is all you need. However, if you want to create a plugin or a module, go to :ref:`developing_plugins` and :ref:`developing_modules_general` topics and then return to this page to know how to add it locally.

Extending Assible with local modules and plugins offers lots of shortcuts such as:

* You can copy other people's modules and plugins.
* When writing a new module, you can choose any programming language you like.
* You do not have to clone any repositories.
* You do not have to open a pull request.
* You do not have to add tests (though we recommend that you do!).

To save a local module or plugin such that Assible can find and use it, add the module or plugin in the appropriate directory (the directories are specified in later parts of this topic).

.. contents::
   :local:

.. _modules_vs_plugins:

Modules and plugins: what is the difference?
============================================
If you are looking to add local functionality to Assible, you might wonder whether you need a module or a plugin. Here is a quick overview to help you decide between the two:

* Modules are reusable, standalone scripts that can be used by the Assible API, the :command:`assible` command, or the :command:`assible-playbook` command. Modules provide a defined interface. Each module accepts arguments and returns information to Assible by printing a JSON string to stdout before exiting. Modules execute on the target system (usually that means on a remote system) in separate processes.
* :ref:`Plugins <plugins_lookup>` augment Assible's core functionality and execute on the control node within the ``/usr/bin/assible`` process. Plugins offer options and extensions for the core features of Assible - transforming data, logging output, connecting to inventory, and more.

.. _local_modules:

Adding a module locally
=======================
Assible automatically loads all executable files found in certain directories as modules.

For local modules, use the name of the file as the module name: for example, if the module file is ``~/.assible/plugins/modules/local_users.py``, use ``local_users`` as the module name.

To load your local modules automatically and make them available to all playbooks and roles, add them in any of these locations:

* any directory added to the ``ASSIBLE_LIBRARY`` environment variable (``$ASSIBLE_LIBRARY`` takes a colon-separated list like ``$PATH``)
* ``~/.assible/plugins/modules/``
* ``/usr/share/assible/plugins/modules/``

After you save your module file in one of these locations, Assible loads it and you can use it in any local task, playbook, or role.

To confirm that ``my_custom_module`` is available:

* type ``assible localhost -m my_custom_module``. You should see the output for that module.

or

* type ``assible-doc -t module my_custom_module``. You should see the documentation for that module.

.. note::

   Currently, the ``assible-doc`` command can parse module documentation only from modules written in Python. If you have a module written in a programming language other than Python, please write the documentation in a Python file adjacent to the module file.

You can limit the availability of your local module. If you want to use a local module only with selected playbooks or only with a single role, load it in one of the following locations:

* In a selected playbook or playbooks: Store the module in a subdirectory called ``library`` in the directory that contains those playbooks.
* In a single role: Store the module in a subdirectory called ``library`` within that role.

.. _distributing_plugins:
.. _local_plugins:

Adding a plugin locally
=======================
Assible loads plugins automatically too, and loads each type of plugin separately from a directory named for the type of plugin. Here's the full list of plugin directory names:

    * action_plugins*
    * cache_plugins
    * callback_plugins
    * connection_plugins
    * filter_plugins*
    * inventory_plugins
    * lookup_plugins
    * shell_plugins
    * strategy_plugins
    * test_plugins*
    * vars_plugins

.. note::

	After you add the plugins and verify that they are available for use, you can see the documentation for all the plugins except for the ones marked with an asterisk (*) above.

To load your local plugins automatically, add them in any of these locations:

* any directory added to the relevant ``ASSIBLE_plugin_type_PLUGINS`` environment variable (these variables, such as ``$ASSIBLE_INVENTORY_PLUGINS`` and ``$ASSIBLE_VARS_PLUGINS`` take colon-separated lists like ``$PATH``)
* the directory named for the correct ``plugin_type`` within ``~/.assible/plugins/`` - for example, ``~/.assible/plugins/callback``
* the directory named for the correct ``plugin_type`` within ``/usr/share/assible/plugins/`` - for example, ``/usr/share/assible/plugins/action``

After your plugin file is in one of these locations, Assible loads it and you can use it in any local module, task, playbook, or role. Alternatively, you can edit your ``assible.cfg`` file to add directories that contain local plugins. For details about adding directories of local plugins, see :ref:`assible_configuration_settings`.

To confirm that ``plugins/plugin_type/my_custom_plugin`` is available:

* type ``assible-doc -t <plugin_type> my_custom_lookup_plugin``. For example, ``assible-doc -t lookup my_custom_lookup_plugin``. You should see the documentation for that plugin. This works for all plugin types except the ones marked with ``*`` in the list above  - see :ref:`assible-doc` for more details.

You can limit the availability of your local plugin. If you want to use a local plugin only with selected playbooks or only with a single role, load it in one of the following locations:

* In a selected playbook or playbooks: Store the plugin in a subdirectory for the correct ``plugin_type`` (for example, ``callback_plugins`` or ``inventory_plugins``) in the directory that contains the playbooks.
* In a single role: Store the plugin in a subdirectory for the correct ``plugin_type`` (for example, ``cache_plugins`` or ``strategy_plugins``) within that role. When shipped as part of a role, the plugin is available as soon as the role is executed.
