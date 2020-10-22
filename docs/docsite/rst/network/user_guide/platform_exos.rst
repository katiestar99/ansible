.. _exos_platform_options:

***************************************
EXOS Platform Options
***************************************

Extreme EXOS is part of the `community.network <https://galaxy.assible.com/community/network>`_ collection and supports multiple connections. This page offers details on how each connection works in Assible and how to use it.

.. contents::
  :local:

Connections available
================================================================================


.. table::
    :class: documentation-table

    ====================  ==========================================  =========================
    ..                    CLI                                         EXOS-API
    ====================  ==========================================  =========================
    Protocol              SSH                                         HTTP(S)

    Credentials           uses SSH keys / SSH-agent if present        uses HTTPS certificates if present

                          accepts ``-u myuser -k`` if using password

    Indirect Access       via a bastion (jump host)                   via a web proxy

    Connection Settings   ``assible_connection:``                     ``assible_connection:``
                            ``assible.netcommon.network_cli``           ``assible.netcommon.httpapi``

    |enable_mode|         not supported by EXOS                       not supported by EXOS

    Returned Data Format  ``stdout[0].``                              ``stdout[0].messages[0].``
    ====================  ==========================================  =========================

.. |enable_mode| replace:: Enable Mode |br| (Privilege Escalation)

EXOS does not support ``assible_connection: local``. You must use ``assible_connection: assible.netcommon.network_cli`` or ``assible_connection: assible.netcommon.httpapi``.

Using CLI in Assible
====================

Example CLI ``group_vars/exos.yml``
-----------------------------------

.. code-block:: yaml

   assible_connection: assible.netcommon.network_cli
   assible_network_os: community.network.exos
   assible_user: myuser
   assible_password: !vault...
   assible_ssh_common_args: '-o ProxyCommand="ssh -W %h:%p -q bastion01"'


- If you are using SSH keys (including an ssh-agent) you can remove the ``assible_password`` configuration.
- If you are accessing your host directly (not through a bastion/jump host) you can remove the ``assible_ssh_common_args`` configuration.
- If you are accessing your host through a bastion/jump host, you cannot include your SSH password in the ``ProxyCommand`` directive. To prevent secrets from leaking out (for example in ``ps`` output), SSH does not support providing passwords via environment variables.

Example CLI task
----------------

.. code-block:: yaml

   - name: Retrieve EXOS OS version
     community.network.exos_command:
       commands: show version
     when: assible_network_os == 'community.network.exos'



Using EXOS-API in Assible
=========================

Example EXOS-API ``group_vars/exos.yml``
----------------------------------------

.. code-block:: yaml

   assible_connection: assible.netcommon.httpapi
   assible_network_os: community.network.exos
   assible_user: myuser
   assible_password: !vault...
   proxy_env:
     http_proxy: http://proxy.example.com:8080

- If you are accessing your host directly (not through a web proxy) you can remove the ``proxy_env`` configuration.
- If you are accessing your host through a web proxy using ``https``, change ``http_proxy`` to ``https_proxy``.


Example EXOS-API task
---------------------

.. code-block:: yaml

   - name: Retrieve EXOS OS version
     community.network.exos_command:
       commands: show version
     when: assible_network_os == 'community.network.exos'

In this example the ``proxy_env`` variable defined in ``group_vars`` gets passed to the ``environment`` option of the module used in the task.

.. include:: shared_snippets/SSH_warning.txt

.. seealso::

       :ref:`timeout_options`
