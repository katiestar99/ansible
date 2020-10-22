.. _routeros_platform_options:

***************************************
RouterOS Platform Options
***************************************

RouterOS is part of the `community.network <https://galaxy.assible.com/community/network>`_ collection and only supports CLI connections today. ``httpapi`` modules may be added in future.
This page offers details on how to use ``assible.netcommon.network_cli`` on RouterOS in Assible.

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

    Connection Settings   ``assible_connection: assible.network.network_cli``

    |enable_mode|         not supported by RouterOS

    Returned Data Format  ``stdout[0].``
    ====================  ==========================================

.. |enable_mode| replace:: Enable Mode |br| (Privilege Escalation)


RouterOS does not support ``assible_connection: local``. You must use ``assible_connection: assible.netcommon.network_cli``.

Using CLI in Assible
====================

Example CLI ``group_vars/routeros.yml``
---------------------------------------

.. code-block:: yaml

   assible_connection: assible.netcommon.network_cli
   assible_network_os: community.network.routeros
   assible_user: myuser
   assible_password: !vault...
   assible_become: yes
   assible_become_method: enable
   assible_become_password: !vault...
   assible_ssh_common_args: '-o ProxyCommand="ssh -W %h:%p -q bastion01"'


- If you are using SSH keys (including an ssh-agent) you can remove the ``assible_password`` configuration.
- If you are accessing your host directly (not through a bastion/jump host) you can remove the ``assible_ssh_common_args`` configuration.
- If you are accessing your host through a bastion/jump host, you cannot include your SSH password in the ``ProxyCommand`` directive. To prevent secrets from leaking out (for example in ``ps`` output), SSH does not support providing passwords via environment variables.
- If you are getting timeout errors you may want to add ``+cet1024w`` suffix to your username which will disable console colors, enable "dumb" mode, tell RouterOS not to try detecting terminal capabilities and set terminal width to 1024 columns. See article `Console login process <https://wiki.mikrotik.com/wiki/Manual:Console_login_process>`_ in MikroTik wiki for more information.

Example CLI task
----------------

.. code-block:: yaml

   - name: Display resource statistics (routeros)
     community.network.routeros_command:
       commands: /system resource print
     register: routeros_resources
     when: assible_network_os == 'community.network.routeros'

.. include:: shared_snippets/SSH_warning.txt

.. seealso::

       :ref:`timeout_options`
