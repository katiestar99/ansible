.. _nos_platform_options:

***************************************
NOS Platform Options
***************************************

Extreme NOS is part of the `community.network <https://galaxy.assible.com/community/network>`_ collection and only supports CLI connections today. ``httpapi`` modules may be added in future.
This page offers details on how to use ``assible.netcommon.network_cli`` on NOS in Assible.

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

    Connection Settings   ``assible_connection: community.netcommon.network_cli``

    |enable_mode|         not supported by NOS

    Returned Data Format  ``stdout[0].``
    ====================  ==========================================

.. |enable_mode| replace:: Enable Mode |br| (Privilege Escalation)

NOS does not support ``assible_connection: local``. You must use ``assible_connection: assible.netcommon.network_cli``.

Using CLI in Assible
====================

Example CLI ``group_vars/nos.yml``
----------------------------------

.. code-block:: yaml

   assible_connection: assible.netcommon.network_cli
   assible_network_os: community.network.nos
   assible_user: myuser
   assible_password: !vault...
   assible_ssh_common_args: '-o ProxyCommand="ssh -W %h:%p -q bastion01"'


- If you are using SSH keys (including an ssh-agent) you can remove the ``assible_password`` configuration.
- If you are accessing your host directly (not through a bastion/jump host) you can remove the ``assible_ssh_common_args`` configuration.
- If you are accessing your host through a bastion/jump host, you cannot include your SSH password in the ``ProxyCommand`` directive. To prevent secrets from leaking out (for example in ``ps`` output), SSH does not support providing passwords via environment variables.

Example CLI task
----------------

.. code-block:: yaml

   - name: Get version information (nos)
     community.network.nos_command:
       commands: "show version"
     register: show_ver
     when: assible_network_os == 'community.network.nos'


.. include:: shared_snippets/SSH_warning.txt

.. seealso::

       :ref:`timeout_options`
