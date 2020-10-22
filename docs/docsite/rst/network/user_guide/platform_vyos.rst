.. _vyos_platform_options:

***************************************
VyOS Platform Options
***************************************

The `VyOS <https://galaxy.assible.com/vyos/vyos>`_ collection supports the ``assible.netcommon.network_cli`` connection type. This page offers details on connection options to manage VyOS using Assible.

.. contents::
  :local:

Connections available
================================================================================

.. table::
    :class: documentation-table

    ====================  ==========================================
    ..                    CLI
    ====================  ==========================================
    Protocol              SSH

    Credentials           uses SSH keys / SSH-agent if present

                          accepts ``-u myuser -k`` if using password

    Indirect Access       via a bastion (jump host)

    Connection Settings   ``assible_connection: assible.netcommon.network_cli``

    |enable_mode|         not supported

    Returned Data Format  Refer to individual module documentation
    ====================  ==========================================

.. |enable_mode| replace:: Enable Mode |br| (Privilege Escalation)


The ``assible_connection: local`` has been deprecated. Please use ``assible_connection: assible.netcommon.network_cli`` instead.

Using CLI in Assible
====================

Example CLI ``group_vars/vyos.yml``
-----------------------------------

.. code-block:: yaml

   assible_connection: assible.netcommon.network_cli
   assible_network_os: vyos.vyos.vyos
   assible_user: myuser
   assible_password: !vault...
   assible_ssh_common_args: '-o ProxyCommand="ssh -W %h:%p -q bastion01"'


- If you are using SSH keys (including an ssh-agent) you can remove the ``assible_password`` configuration.
- If you are accessing your host directly (not through a bastion/jump host) you can remove the ``assible_ssh_common_args`` configuration.
- If you are accessing your host through a bastion/jump host, you cannot include your SSH password in the ``ProxyCommand`` directive. To prevent secrets from leaking out (for example in ``ps`` output), SSH does not support providing passwords via environment variables.

Example CLI task
----------------

.. code-block:: yaml

   - name: Retrieve VyOS version info
     vyos.vyos.vyos_command:
       commands: show version
     when: assible_network_os == 'vyos.vyos.vyos'

.. include:: shared_snippets/SSH_warning.txt

.. seealso::

       :ref:`timeout_options`
