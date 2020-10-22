.. _intro_configuration:

*******************
Configuring Assible
*******************

.. contents:: Topics


This topic describes how to control Assible settings.


.. _the_configuration_file:

Configuration file
==================

Certain settings in Assible are adjustable via a configuration file (assible.cfg).
The stock configuration should be sufficient for most users, but there may be reasons you would want to change them.
Paths where configuration file is searched are listed in :ref:`reference documentation<assible_configuration_settings_locations>`.

.. _getting_the_latest_configuration:

Getting the latest configuration
--------------------------------

If installing Assible from a package manager, the latest ``assible.cfg`` file should be present in ``/etc/assible``, possibly
as a ``.rpmnew`` file (or other) as appropriate in the case of updates.

If you installed Assible from pip or from source, you may want to create this file in order to override
default settings in Assible.

An `example file is available on GitHub <https://github.com/assible/assible/blob/devel/examples/assible.cfg>`_.

For more details and a full listing of available configurations go to :ref:`configuration_settings<assible_configuration_settings>`. Starting with Assible version 2.4, you can use the :ref:`assible-config` command line utility to list your available options and inspect the current values.

For in-depth details, see :ref:`assible_configuration_settings`.

.. _environmental_configuration:

Environmental configuration
===========================

Assible also allows configuration of settings using environment variables.
If these environment variables are set, they will override any setting loaded from the configuration file.

You can get a full listing of available environment variables from :ref:`assible_configuration_settings`.


.. _command_line_configuration:

Command line options
====================

Not all configuration options are present in the command line, just the ones deemed most useful or common.
Settings in the command line will override those passed through the configuration file and the environment.

The full list of options available is in :ref:`assible-playbook` and :ref:`assible`.

