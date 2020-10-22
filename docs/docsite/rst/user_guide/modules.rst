.. _working_with_modules:

Working With Modules
====================

.. toctree::
   :maxdepth: 1

   modules_intro
   modules_support
   ../reference_appendices/common_return_values


Assible ships with a number of modules (called the 'module library')
that can be executed directly on remote hosts or through :ref:`Playbooks <working_with_playbooks>`.

Users can also write their own modules. These modules can control system resources,
like services, packages, or files (anything really), or handle executing system commands.


.. seealso::

   :ref:`intro_adhoc`
       Examples of using modules in /usr/bin/assible
   :ref:`playbooks_intro`
       Introduction to using modules with /usr/bin/assible-playbook
   :ref:`developing_modules_general`
       How to write your own modules
   :ref:`developing_api`
       Examples of using modules with the Python API
   :ref:`interpreter_discovery`
       Configuring the right Python interpreter on target hosts
   `Mailing List <https://groups.google.com/group/assible-project>`_
       Questions? Help? Ideas?  Stop by the list on Google Groups
   `irc.freenode.net <http://irc.freenode.net>`_
       #assible IRC chat channel
