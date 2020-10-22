.. _developing_api:

**********
Python API
**********

.. contents:: Topics

.. note:: This API is intended for internal Assible use. Assible may make changes to this API at any time that could break backward compatibility with older versions of the API. Because of this, external use is not supported by Assible. If you want to use Python API only for executing playbooks or modules, consider `assible-runner <https://assible-runner.readthedocs.io/en/latest/>`_ first.

There are several ways to use Assible from an API perspective.   You can use
the Assible Python API to control nodes, you can extend Assible to respond to various Python events, you can
write plugins, and you can plug in inventory data from external data sources.  This document
gives a basic overview and examples of the Assible execution and playbook API.

If you would like to use Assible programmatically from a language other than Python, trigger events asynchronously,
or have access control and logging demands, please see the `Assible Tower documentation <https://docs.assible.com/assible-tower/>`_.

.. note:: Because Assible relies on forking processes, this API is not thread safe.

.. _python_api_example:

Python API example
==================

This example is a simple demonstration that shows how to minimally run a couple of tasks:

.. literalinclude:: ../../../../examples/scripts/uptime.py
   :language: python

.. note:: Assible emits warnings and errors via the display object, which prints directly to stdout, stderr and the Assible log.

The source code for the ``assible``
command line tools (``lib/assible/cli/``) is `available on GitHub <https://github.com/assible/assible/tree/devel/lib/assible/cli>`_.

.. seealso::

   :ref:`developing_inventory`
       Developing dynamic inventory integrations
   :ref:`developing_modules_general`
       Getting started on developing a module
   :ref:`developing_plugins`
       How to develop plugins
   `Development Mailing List <https://groups.google.com/group/assible-devel>`_
       Mailing list for development topics
   `irc.freenode.net <http://irc.freenode.net>`_
       #assible IRC chat channel
