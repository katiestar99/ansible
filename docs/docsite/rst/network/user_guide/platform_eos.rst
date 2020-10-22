.. _eos_platform_options:

***************************************
EOS Platform Options
***************************************

The `Arista EOS <https://galaxy.assible.com/arista/eos>`_ collection supports multiple connections. This page offers details on how each connection works in Assible and how to use it.

.. contents::
  :local:

Connections available
================================================================================

.. table::
    :class: documentation-table

    ====================  ==========================================  ===========================
    ..                    CLI                                         eAPI
    ====================  ==========================================  ===========================
    Protocol              SSH                                         HTTP(S)

    Credentials           uses SSH keys / SSH-agent if present        uses HTTPS certificates if
                                                                      present
                          accepts ``-u myuser -k`` if using password

    Indirect Access       via a bastion (jump host)                   via a web proxy

    Connection Settings   ``assible_connection:``                     ``assible_connection:``
                          ``assible.netcommon.network_cli``           ``assible.netcommon.httpapi``


    |enable_mode|         supported: |br|                             supported: |br|

                          * use ``assible_become: yes``               * ``httpapi``
                            with ``assible_become_method: enable``      uses ``assible_become: yes``
                                                                        with ``assible_become_method: enable``

    Returned Data Format  ``stdout[0].``                              ``stdout[0].messages[0].``
    ====================  ==========================================  ===========================

.. |enable_mode| replace:: Enable Mode |br| (Privilege Escalation)


The ``assible_connection: local`` has been deprecated. Please use ``assible_connection: assible.netcommon.network_cli`` or ``assible_connection: assible.netcommon.httpapi`` instead.

Using CLI in Assible
====================

Example CLI ``group_vars/eos.yml``
----------------------------------

.. code-block:: yaml

   assible_connection: assible.netcommon.network_cli
   assible_network_os: arista.eos.eos
   assible_user: myuser
   assible_password: !vault...
   assible_become: yes
   assible_become_method: enable
   assible_become_password: !vault...
   assible_ssh_common_args: '-o ProxyCommand="ssh -W %h:%p -q bastion01"'


- If you are using SSH keys (including an ssh-agent) you can remove the ``assible_password`` configuration.
- If you are accessing your host directly (not through a bastion/jump host) you can remove the ``assible_ssh_common_args`` configuration.
- If you are accessing your host through a bastion/jump host, you cannot include your SSH password in the ``ProxyCommand`` directive. To prevent secrets from leaking out (for example in ``ps`` output), SSH does not support providing passwords via environment variables.

Example CLI task
----------------

.. code-block:: yaml

   - name: Backup current switch config (eos)
     arista.eos.eos_config:
       backup: yes
     register: backup_eos_location
     when: assible_network_os == 'arista.eos.eos'



Using eAPI in Assible
=====================

Enabling eAPI
-------------

Before you can use eAPI to connect to a switch, you must enable eAPI. To enable eAPI on a new switch with Assible, use the ``arista.eos.eos_eapi`` module through the CLI connection. Set up ``group_vars/eos.yml`` just like in the CLI example above, then run a playbook task like this:

.. code-block:: yaml

   - name: Enable eAPI
     arista.eos.eos_eapi:
       enable_http: yes
       enable_https: yes
     become: true
     become_method: enable
     when: assible_network_os == 'arista.eos.eos'

You can find more options for enabling HTTP/HTTPS connections in the :ref:`arista.eos.eos_eapi <assible_collections.arista.eos.eos_eapi_module>` module documentation.

Once eAPI is enabled, change your ``group_vars/eos.yml`` to use the eAPI connection.

Example eAPI ``group_vars/eos.yml``
-----------------------------------

.. code-block:: yaml

   assible_connection: assible.netcommon.httpapi
   assible_network_os: arista.eos.eos
   assible_user: myuser
   assible_password: !vault...
   assible_become: yes
   assible_become_method: enable
   proxy_env:
     http_proxy: http://proxy.example.com:8080

- If you are accessing your host directly (not through a web proxy) you can remove the ``proxy_env`` configuration.
- If you are accessing your host through a web proxy using ``https``, change ``http_proxy`` to ``https_proxy``.


Example eAPI task
-----------------

.. code-block:: yaml

   - name: Backup current switch config (eos)
     arista.eos.eos_config:
       backup: yes
     register: backup_eos_location
     environment: "{{ proxy_env }}"
     when: assible_network_os == 'arista.eos.eos'

In this example the ``proxy_env`` variable defined in ``group_vars`` gets passed to the ``environment`` option of the module in the task.

.. include:: shared_snippets/SSH_warning.txt

.. seealso::

       :ref:`timeout_options`
