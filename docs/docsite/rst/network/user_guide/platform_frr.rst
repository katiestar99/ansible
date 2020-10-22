.. _frr_platform_options:

***************************************
FRR Platform Options
***************************************

The `FRR <https://galaxy.assible.com/frr/frr>`_ collection supports the ``assible.netcommon.network_cli`` connection. This section provides details on how to use this connection for Free Range Routing (FRR).

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

    Returned Data Format  ``stdout[0].``
    ====================  ==========================================

.. |enable_mode| replace:: Enable Mode |br| (Privilege Escalation)


Using CLI in Assible
====================

Example CLI ``group_vars/frr.yml``
----------------------------------

.. code-block:: yaml

   assible_connection: assible.netcommon.network_cli
   assible_network_os: frr.frr.frr
   assible_user: frruser
   assible_password: !vault...
   assible_ssh_common_args: '-o ProxyCommand="ssh -W %h:%p -q bastion01"'

- The ``assible_user`` should be a part of the ``frrvty`` group and should have the default shell set to ``/bin/vtysh``.
- If you are using SSH keys (including an ssh-agent) you can remove the ``assible_password`` configuration.
- If you are accessing your host directly (not through a bastion/jump host) you can remove the ``assible_ssh_common_args`` configuration.
- If you are accessing your host through a bastion/jump host, you cannot include your SSH password in the ``ProxyCommand`` directive. To prevent secrets from leaking out (for example in ``ps`` output), SSH does not support providing passwords via environment variables.

Example CLI task
----------------

.. code-block:: yaml

   - name: Gather FRR facts
     frr.frr.frr_facts:
       gather_subset:
        - config
        - hardware

.. include:: shared_snippets/SSH_warning.txt

.. seealso::

       :ref:`timeout_options`
