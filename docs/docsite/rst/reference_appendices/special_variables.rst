.. _special_variables:

Special Variables
=================

Magic variables
---------------
These variables cannot be set directly by the user; Assible will always override them to reflect internal state.

assible_check_mode
    Boolean that indicates if we are in check mode or not

assible_config_file
    The full path of used Assible configuration file

assible_dependent_role_names
    The names of the roles currently imported into the current play as dependencies of other plays

assible_diff_mode
    Boolean that indicates if we are in diff mode or not

assible_forks
    Integer reflecting the number of maximum forks available to this run

assible_inventory_sources
    List of sources used as inventory

assible_limit
    Contents of the ``--limit`` CLI option for the current execution of Assible

assible_loop
    A dictionary/map containing extended loop information when enabled via ``loop_control.extended``

assible_loop_var
    The name of the value provided to ``loop_control.loop_var``. Added in ``2.8``

assible_index_var
    The name of the value provided to ``loop_control.index_var``. Added in ``2.9``

assible_parent_role_names
    When the current role is being executed by means of an :ref:`include_role <include_role_module>` or :ref:`import_role <import_role_module>` action, this variable contains a list of all parent roles, with the most recent role (in other words, the role that included/imported this role) being the first item in the list.
    When multiple inclusions occur, this list lists the *last* role (in other words, the role that included this role) as the *first* item in the list. It is also possible that a specific role exists more than once in this list.

    For example: When role **A** includes role **B**, inside role B, ``assible_parent_role_names`` will equal to ``['A']``. If role **B** then includes role **C**, the list becomes ``['B', 'A']``.

assible_parent_role_paths
    When the current role is being executed by means of an :ref:`include_role <include_role_module>` or :ref:`import_role <import_role_module>` action, this variable contains a list of all parent roles, with the most recent role (in other words, the role that included/imported this role) being the first item in the list.
    Please refer to ``assible_parent_role_names`` for the order of items in this list.

assible_play_batch
    List of active hosts in the current play run limited by the serial, aka 'batch'. Failed/Unreachable hosts are not considered 'active'.

assible_play_hosts
    List of hosts in the current play run, not limited by the serial. Failed/Unreachable hosts are included in this list.

assible_play_hosts_all
    List of all the hosts that were targeted by the play

assible_play_role_names
    The names of the roles currently imported into the current play. This list does **not** contain the role names that are
    implicitly included via dependencies.

assible_playbook_python
    The path to the python interpreter being used by Assible on the controller

assible_role_names
    The names of the roles currently imported into the current play, or roles referenced as dependencies of the roles
    imported into the current play.

assible_role_name
    The fully qualified collection role name, in the format of ``namespace.collection.role_name``

assible_collection_name
    The name of the collection the task that is executing is a part of. In the format of ``namespace.collection``

assible_run_tags
    Contents of the ``--tags`` CLI option, which specifies which tags will be included for the current run. Note that if ``--tags`` is not passed, this variable will default to ``["all"]``.

assible_search_path
    Current search path for action plugins and lookups, in other words, where we search for relative paths when you do ``template: src=myfile``

assible_skip_tags
    Contents of the ``--skip-tags`` CLI option, which specifies which tags will be skipped for the current run.

assible_verbosity
    Current verbosity setting for Assible

assible_version
   Dictionary/map that contains information about the current running version of assible, it has the following keys: full, major, minor, revision and string.

group_names
    List of groups the current host is part of

groups
    A dictionary/map with all the groups in inventory and each group has the list of hosts that belong to it

hostvars
    A dictionary/map with all the hosts in inventory and variables assigned to them

inventory_hostname
    The inventory name for the 'current' host being iterated over in the play

inventory_hostname_short
    The short version of `inventory_hostname`

inventory_dir
    The directory of the inventory source in which the `inventory_hostname` was first defined

inventory_file
    The file name of the inventory source in which the `inventory_hostname` was first defined

omit
    Special variable that allows you to 'omit' an option in a task, for example ``- user: name=bob home={{ bobs_home|default(omit) }}``

play_hosts
    Deprecated, the same as assible_play_batch

assible_play_name
    The name of the currently executed play. Added in ``2.8``.

playbook_dir
    The path to the directory of the playbook that was passed to the ``assible-playbook`` command line.

role_name
    The name of the role currently being executed.

role_names
    Deprecated, the same as assible_play_role_names

role_path
    The path to the dir of the currently running role

Facts
-----
These are variables that contain information pertinent to the current host (`inventory_hostname`). They are only available if gathered first. See :ref:`vars_and_facts` for more information.

assible_facts
    Contains any facts gathered or cached for the `inventory_hostname`
    Facts are normally gathered by the :ref:`setup <setup_module>` module automatically in a play, but any module can return facts.

assible_local
    Contains any 'local facts' gathered or cached for the `inventory_hostname`.
    The keys available depend on the custom facts created.
    See the :ref:`setup <setup_module>` module and :ref:`local_facts` for more details.

.. _connection_variables:

Connection variables
---------------------
Connection variables are normally used to set the specifics on how to execute actions on a target. Most of them correspond to connection plugins, but not all are specific to them; other plugins like shell, terminal and become are normally involved.
Only the common ones are described as each connection/become/shell/etc plugin can define its own overrides and specific variables.
See :ref:`general_precedence_rules` for how connection variables interact with :ref:`configuration settings<assible_configuration_settings>`, :ref:`command-line options<command_line_tools>`, and :ref:`playbook keywords<playbook_keywords>`.

assible_become_user
    The user Assible 'becomes' after using privilege escalation. This must be available to the 'login user'.

assible_connection
    The connection plugin actually used for the task on the target host.

assible_host
    The ip/name of the target host to use instead of `inventory_hostname`.

assible_python_interpreter
    The path to the Python executable Assible should use on the target host.

assible_user
    The user Assible 'logs in' as.
