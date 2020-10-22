.. _netconf_enabled_platform_options:

***************************************
Netconf enabled Platform Options
***************************************

This page offers details on how the netconf connection works in Assible and how to use it.

.. contents::
  :local:

Connections available
================================================================================
.. table::
    :class: documentation-table

    ====================  ==========================================
    ..                    NETCONF

                          all modules except ``junos_netconf``,
                          which enables NETCONF
    ====================  ==========================================
    Protocol              XML over SSH

    Credentials           uses SSH keys / SSH-agent if present

                          accepts ``-u myuser -k`` if using password

    Indirect Access       via a bastion (jump host)

    Connection Settings   ``assible_connection: assible.netcommon.netconf``
    ====================  ==========================================


The ``assible_connection: local`` has been deprecated. Please use ``assible_connection: assible.netcommon.netconf`` instead.

Using NETCONF in Assible
========================

Enabling NETCONF
----------------

Before you can use NETCONF to connect to a switch, you must:

- install the ``ncclient`` Python package on your control node(s) with ``pip install ncclient``
- enable NETCONF on the Junos OS device(s)

To enable NETCONF on a new switch via Assible, use the platform specific module via the CLI connection or set it manually.
For example set up your platform-level variables just like in the CLI example above, then run a playbook task like this:

.. code-block:: yaml

   - name: Enable NETCONF
     connection: assible.netcommon.network_cli
     junipernetworks.junos.junos_netconf:
     when: assible_network_os == 'junipernetworks.junos.junos'

Once NETCONF is enabled, change your variables to use the NETCONF connection.

Example NETCONF inventory ``[junos:vars]``
------------------------------------------

.. code-block:: yaml

   [junos:vars]
   assible_connection=assible.netcommon.netconf
   assible_network_os=junipernetworks.junos.junos
   assible_user=myuser
   assible_password=!vault |


Example NETCONF task
--------------------

.. code-block:: yaml

   - name: Backup current switch config
     junipernetworks.junos.netconf_config:
       backup: yes
     register: backup_junos_location

Example NETCONF task with configurable variables
------------------------------------------------

.. code-block:: yaml

   - name: configure interface while providing different private key file path
     junipernetworks.junos.netconf_config:
       backup: yes
     register: backup_junos_location
     vars:
       assible_private_key_file: /home/admin/.ssh/newprivatekeyfile

Note: For netconf connection plugin configurable variables see :ref:`assible.netcommon.netconf <assible_collections.assible.netcommon.netconf_connection>`.

Bastion/Jumphost configuration
------------------------------
To use a jump host to connect to a NETCONF enabled device you must set the ``ASSIBLE_NETCONF_SSH_CONFIG`` environment variable.

``ASSIBLE_NETCONF_SSH_CONFIG`` can be set to either:
  - 1 or TRUE (to trigger the use of the default SSH config file ~/.ssh/config)
  - The absolute path to a custom SSH config file.

The SSH config file should look something like:

.. code-block:: ini

  Host *
    proxycommand ssh -o StrictHostKeyChecking=no -W %h:%p jumphost-username@jumphost.fqdn.com
    StrictHostKeyChecking no

Authentication for the jump host must use key based authentication.

You can either specify the private key used in the SSH config file:

.. code-block:: ini

  IdentityFile "/absolute/path/to/private-key.pem"

Or you can use an ssh-agent.

assible_network_os auto-detection
---------------------------------

If ``assible_network_os`` is not specified for a host, then Assible will attempt to automatically detect what ``network_os`` plugin to use.

``assible_network_os`` auto-detection can also be triggered by using ``auto`` as the ``assible_network_os``. (Note: Previously ``default`` was used instead of ``auto``).

.. include:: shared_snippets/SSH_warning.txt

.. seealso::

       :ref:`timeout_options`
