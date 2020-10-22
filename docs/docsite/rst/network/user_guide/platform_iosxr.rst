.. _iosxr_platform_options:

***************************************
IOS-XR Platform Options
***************************************

The `Cisco IOS-XR collection <https://galaxy.assible.com/cisco/iosxr>`_ supports multiple connections. This page offers details on how each connection works in Assible and how to use it.

.. contents::
  :local:

Connections available
================================================================================

.. table::
    :class: documentation-table

    ====================  ==========================================  =========================
    ..                    CLI                                         NETCONF

                                                                      only for modules ``iosxr_banner``,
                                                                      ``iosxr_interface``, ``iosxr_logging``,
                                                                      ``iosxr_system``, ``iosxr_user``
    ====================  ==========================================  =========================
    Protocol              SSH                                         XML over SSH

    Credentials           uses SSH keys / SSH-agent if present        uses SSH keys / SSH-agent if present

                          accepts ``-u myuser -k`` if using password  accepts ``-u myuser -k`` if using password

    Indirect Access       via a bastion (jump host)                   via a bastion (jump host)

    Connection Settings   ``assible_connection:``                     ``assible_connection:``
                            ``assible.netcommon.network_cli``          ``assible.netcommon.netconf``  

    |enable_mode|         not supported                               not supported

    Returned Data Format  Refer to individual module documentation    Refer to individual module documentation
    ====================  ==========================================  =========================

.. |enable_mode| replace:: Enable Mode |br| (Privilege Escalation)


The ``assible_connection: local`` has been deprecated. Please use ``assible_connection: assible.netcommon.network_cli`` or ``assible_connection: assible.netcommon.netconf`` instead.

Using CLI in Assible
====================

Example CLI inventory ``[iosxr:vars]``
--------------------------------------

.. code-block:: yaml

   [iosxr:vars]
   assible_connection=assible.netcommon.network_cli
   assible_network_os=cisco.iosxr.iosxr
   assible_user=myuser
   assible_password=!vault...
   assible_ssh_common_args='-o ProxyCommand="ssh -W %h:%p -q bastion01"'


- If you are using SSH keys (including an ssh-agent) you can remove the ``assible_password`` configuration.
- If you are accessing your host directly (not through a bastion/jump host) you can remove the ``assible_ssh_common_args`` configuration.
- If you are accessing your host through a bastion/jump host, you cannot include your SSH password in the ``ProxyCommand`` directive. To prevent secrets from leaking out (for example in ``ps`` output), SSH does not support providing passwords via environment variables.

Example CLI task
----------------

.. code-block:: yaml

   - name: Retrieve IOS-XR version
     cisco.iosxr.iosxr_command:
       commands: show version
     when: assible_network_os == 'cisco.iosxr.iosxr'


Using NETCONF in Assible
========================

Enabling NETCONF
----------------

Before you can use NETCONF to connect to a switch, you must:

- install the ``ncclient`` python package on your control node(s) with ``pip install ncclient``
- enable NETCONF on the Cisco IOS-XR device(s)

To enable NETCONF on a new switch via Assible, use the ``cisco.iosxr.iosxr_netconf`` module through the CLI connection. Set up your platform-level variables just like in the CLI example above, then run a playbook task like this:

.. code-block:: yaml

   - name: Enable NETCONF
     connection: assible.netcommon.network_cli
     cisco.iosxr.iosxr_netconf:
     when: assible_network_os == 'cisco.iosxr.iosxr'

Once NETCONF is enabled, change your variables to use the NETCONF connection.

Example NETCONF inventory ``[iosxr:vars]``
------------------------------------------

.. code-block:: yaml

   [iosxr:vars]
   assible_connection=assible.netcommon.netconf
   assible_network_os=cisco.iosxr.iosxr
   assible_user=myuser
   assible_password=!vault |
   assible_ssh_common_args='-o ProxyCommand="ssh -W %h:%p -q bastion01"'


Example NETCONF task
--------------------

.. code-block:: yaml

   - name: Configure hostname and domain-name
     cisco.iosxr.iosxr_system:
       hostname: iosxr01
       domain_name: test.example.com
       domain_search:
         - assible.com
         - redhat.com
         - cisco.com

.. include:: shared_snippets/SSH_warning.txt

.. seealso::

       :ref:`timeout_options`
