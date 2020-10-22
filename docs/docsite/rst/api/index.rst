:orphan:

*************************
Assible API Documentation
*************************

The Assible API is under construction. These stub references for attributes, classes, functions, methods, and modules will be documented in future.
The :ref:`module utilities <assible.module_utils>` included in ``assible.module_utils.basic`` and ``AssibleModule`` are documented under Reference & Appendices.

.. contents::
   :local:

Attributes
==========

.. py:attribute:: AssibleModule.params

The parameters accepted by the module.

.. py:attribute:: assible.module_utils.basic.ASSIBLE_VERSION

.. py:attribute:: assible.module_utils.basic.SELINUX_SPECIAL_FS

Deprecated in favor of assibleModule._selinux_special_fs.

.. py:attribute:: AssibleModule.assible_version

.. py:attribute:: AssibleModule._debug

.. py:attribute:: AssibleModule._diff

.. py:attribute:: AssibleModule.no_log

.. py:attribute:: AssibleModule._selinux_special_fs

(formerly assible.module_utils.basic.SELINUX_SPECIAL_FS)

.. py:attribute:: AssibleModule._syslog_facility

.. py:attribute:: self.playbook

.. py:attribute:: self.play

.. py:attribute:: self.task

.. py:attribute:: sys.path


Classes
=======

.. py:class:: ``assible.module_utils.basic.AssibleModule``
   :noindex:

The basic utilities for AssibleModule.

.. py:class:: AssibleModule

The main class for an Assible module.


Functions
=========

.. py:function:: assible.module_utils.basic._load_params()

Load parameters.


Methods
=======

.. py:method:: AssibleModule.log()

Logs the output of Assible.

.. py:method:: AssibleModule.debug()

Debugs Assible.

.. py:method:: Assible.get_bin_path()

Retrieves the path for executables.

.. py:method:: AssibleModule.run_command()

Runs a command within an Assible module.

.. py:method:: module.fail_json()

Exits and returns a failure.

.. py:method:: module.exit_json()

Exits and returns output.


Modules
=======

.. py:module:: assible.module_utils

.. py:module:: assible.module_utils.basic
  :noindex:


.. py:module:: assible.module_utils.url
