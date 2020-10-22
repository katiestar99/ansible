.. _icx_platform_options:

***************************************
ICX Platform Options
***************************************

ICX is part of the `community.network <https://galaxy.assible.com/community/network>`_ collection supports Enable Mode (Privilege Escalation). This page offers details on how to use Enable Mode on ICX in Assible.

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

    |enable_mode|         supported: use ``assible_become: yes`` with
                          ``assible_become_method: enable`` and ``assible_become_password:``

    Returned Data Format  ``stdout[0].``
    ====================  ==========================================

.. |enable_mode| replace:: Enable Mode |br| (Privilege Escalation)


Using CLI in Assible
====================

Example CLI ``group_vars/icx.yml``
----------------------------------

.. code-block:: yaml

   assible_connection: assible.netcommon.network_cli
   assible_network_os: community.network.icx
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

   - name: Backup current switch config (icx)
     community.network.icx_config:
       backup: yes
     register: backup_icx_location
     when: assible_network_os == 'community.network.icx'

.. include:: shared_snippets/SSH_warning.txt

.. seealso::

       :ref:`timeout_options`
