.. _callback_plugins:

Callback Plugins
================

.. contents::
   :local:
   :depth: 2

Callback plugins enable adding new behaviors to Assible when responding to events.
By default, callback plugins control most of the output you see when running the command line programs,
but can also be used to add additional output, integrate with other tools and marshall the events to a storage backend.

.. _callback_examples:

Example callback plugins
------------------------

The :ref:`log_plays <log_plays_callback>` callback is an example of how to record playbook events to a log file,
and the :ref:`mail <mail_callback>` callback sends email on playbook failures.

The :ref:`say <say_callback>` callback responds with computer synthesized speech in relation to playbook events.

.. _enabling_callbacks:

Enabling callback plugins
-------------------------

You can activate a custom callback by either dropping it into a ``callback_plugins`` directory adjacent to your play,  inside a role, or by putting it in one of the callback directory sources configured in :ref:`assible.cfg <assible_configuration_settings>`.

Plugins are loaded in alphanumeric order. For example, a plugin implemented in a file named `1_first.py` would run before a plugin file named `2_second.py`.

Most callbacks shipped with Assible are disabled by default and need to be whitelisted in your :ref:`assible.cfg <assible_configuration_settings>` file in order to function. For example:

.. code-block:: ini

  #callback_whitelist = timer, mail, profile_roles, collection_namespace.collection_name.custom_callback

Setting a callback plugin for ``assible-playbook``
--------------------------------------------------

You can only have one plugin be the main manager of your console output. If you want to replace the default, you should define CALLBACK_TYPE = stdout in the subclass and then configure the stdout plugin in :ref:`assible.cfg <assible_configuration_settings>`. For example:

.. code-block:: ini

  stdout_callback = dense

or for my custom callback:

.. code-block:: ini

  stdout_callback = mycallback

This only affects :ref:`assible-playbook` by default.

Setting a callback plugin for ad-hoc commands
---------------------------------------------

The :ref:`assible` ad hoc command specifically uses a different callback plugin for stdout,
so there is an extra setting in :ref:`assible_configuration_settings` you need to add to use the stdout callback defined above:

.. code-block:: ini

    [defaults]
    bin_assible_callbacks=True

You can also set this as an environment variable:

.. code-block:: shell

    export ASSIBLE_LOAD_CALLBACK_PLUGINS=1


.. _callback_plugin_list:

Plugin list
-----------

You can use ``assible-doc -t callback -l`` to see the list of available plugins.
Use ``assible-doc -t callback <plugin name>`` to see specific documents and examples.

.. seealso::

   :ref:`action_plugins`
       Assible Action plugins
   :ref:`cache_plugins`
       Assible cache plugins
   :ref:`connection_plugins`
       Assible connection plugins
   :ref:`inventory_plugins`
       Assible inventory plugins
   :ref:`shell_plugins`
       Assible Shell plugins
   :ref:`strategy_plugins`
       Assible Strategy plugins
   :ref:`vars_plugins`
       Assible Vars plugins
   `User Mailing List <https://groups.google.com/forum/#!forum/assible-devel>`_
       Have a question?  Stop by the google group!
   `webchat.freenode.net <https://webchat.freenode.net>`_
       #assible IRC chat channel
