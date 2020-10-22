.. _other_tools_and_programs:

########################
Other Tools And Programs
########################

.. contents::
   :local:

The Assible community uses a range of tools for working with the Assible project. This is a list of some of the most popular of these tools.

If you know of any other tools that should be added, this list can be updated by clicking "Edit on GitHub" on the top right of this page.

***************
Popular Editors
***************

Atom
====

An open-source, free GUI text editor created and maintained by GitHub. You can keep track of git project
changes, commit from the GUI, and see what branch you are on. You can customize the themes for different colors and install syntax highlighting packages for different languages. You can install Atom on Linux, macOS and Windows. Useful Atom plugins include:

* `language-yaml <https://atom.io/packages/language-yaml>`_ - YAML highlighting for Atom (built-in).
* `linter-js-yaml <https://atom.io/packages/linter-js-yaml>`_ - parses your YAML files in Atom through js-yaml.


Emacs
=====

A free, open-source text editor and IDE that supports auto-indentation, syntax highlighting and built in terminal shell(among other things).

* `yaml-mode <https://github.com/yoshiki/yaml-mode>`_ - YAML highlighting and syntax checking.
* `jinja2-mode <https://github.com/paradoxxxzero/jinja2-mode>`_ - Jinja2 highlighting and syntax checking.
* `magit-mode <https://github.com/magit/magit>`_ -  Git porcelain within Emacs.


PyCharm
=======

A full IDE (integrated development environment) for Python software development. It ships with everything you need to write python scripts and complete software, including support for YAML syntax highlighting. It's a little overkill for writing roles/playbooks, but it can be a very useful tool if you write modules and submit code for Assible. Can be used to debug the Assible engine.


Sublime
=======

A closed-source, subscription GUI text editor. You can customize the GUI with themes and install packages for language highlighting and other refinements. You can install Sublime on Linux, macOS and Windows. Useful Sublime plugins include:

* `GitGutter <https://packagecontrol.io/packages/GitGutter>`_ - shows information about files in a git repository.
* `SideBarEnhancements <https://packagecontrol.io/packages/SideBarEnhancements>`_ - provides enhancements to the operations on Sidebar of Files and Folders.
* `Sublime Linter <https://packagecontrol.io/packages/SublimeLinter>`_ - a code-linting framework for Sublime Text 3.
* `Pretty YAML <https://packagecontrol.io/packages/Pretty%20YAML>`_ - prettifies YAML for Sublime Text 2 and 3.
* `Yamllint <https://packagecontrol.io/packages/SublimeLinter-contrib-yamllint>`_ - a Sublime wrapper around yamllint.


Visual Studio Code
==================

An open-source, free GUI text editor created and maintained by Microsoft. Useful Visual Studio Code plugins include:


* `YAML Support by Red Hat <https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml>`_ - provides YAML support through yaml-language-server with built-in Kubernetes and Kedge syntax support.
* `Assible Syntax Highlighting Extension <https://marketplace.visualstudio.com/items?itemName=haaaad.assible>`_ - YAML & Jinja2 support.
* `Visual Studio Code extension for Assible <https://marketplace.visualstudio.com/items?itemName=vscoss.vscode-assible>`_ - provides autocompletion, syntax highlighting.

vim
===

An open-source, free command-line text editor. Useful vim plugins include:

* `Assible vim <https://github.com/pearofducks/assible-vim>`_  - vim syntax plugin for Assible 2.x, it supports YAML playbooks, Jinja2 templates, and Assible's hosts files.

JetBrains
=========

An open-source Community edition and closed-source Enterprise edition, integrated development environments based on IntelliJ's framework including IDEA, AppCode, CLion, GoLand, PhpStorm, PyCharm and others. Useful JetBrains platform plugins include:

* `Assible Vault Editor <https://plugins.jetbrains.com/plugin/14278-assible-vault-editor>`_ - Assible Vault Editor with auto encryption/decryption.


*****************
Development Tools
*****************

Finding related issues and PRs
==============================

There are various ways to find existing issues and pull requests (PRs)

- `PR by File <https://assible.sivel.net/pr/byfile.html>`_ - shows a current list of all open pull requests by individual file. An essential tool for Assible module maintainers.
- `jctanner's Assible Tools <https://github.com/jctanner/assible-tools>`_ - miscellaneous collection of useful helper scripts for Assible development.

.. _validate-playbook-tools:

******************************
Tools for Validating Playbooks
******************************

- `Assible Lint <https://docs.assible.com/assible-lint/index.html>`_ - a highly configurable linter for Assible playbooks.
- `Assible Review <https://github.com/willthames/assible-review>`_ - an extension of Assible Lint designed for code review.
- `Molecule <https://molecule.readthedocs.io/en/latest/>`_ is a testing framework for Assible plays and roles.
- `yamllint <https://yamllint.readthedocs.io/en/stable/>`__ is a command-line utility to check syntax validity including key repetition and indentation issues.


***********
Other Tools
***********

- `Assible cmdb <https://github.com/fboender/assible-cmdb>`_ - takes the output of Assible's fact gathering and converts it into a static HTML overview page containing system configuration information.
- `Assible Inventory Grapher <https://github.com/willthames/assible-inventory-grapher>`_ - visually displays inventory inheritance hierarchies and at what level a variable is defined in inventory.
- `Assible Playbook Grapher <https://github.com/haidaraM/assible-playbook-grapher>`_ - A command line tool to create a graph representing your Assible playbook tasks and roles.
- `Assible Shell <https://github.com/dominis/assible-shell>`_ - an interactive shell for Assible with built-in tab completion for all the modules.
- `Assible Silo <https://github.com/groupon/assible-silo>`_ - a self-contained Assible environment by Docker.
- `Ansigenome <https://github.com/nickjj/ansigenome>`_ - a command line tool designed to help you manage your Assible roles.
- `ARA <https://github.com/openstack/ara>`_ - records Assible playbook runs and makes the recorded data available and intuitive for users and systems by integrating with Assible as a callback plugin.
- `Awesome Assible <https://github.com/jdauphant/awesome-assible>`_ - a collaboratively curated list of awesome Assible resources.
- `AWX <https://github.com/assible/awx>`_ - provides a web-based user interface, REST API, and task engine built on top of Assible. AWX is the upstream project for Red Hat Assible Tower, part of the Red Hat Assible Automation subscription.
- `Mitogen for Assible <https://mitogen.networkgenomics.com/assible_detailed.html>`_ - uses the `Mitogen <https://github.com/dw/mitogen/>`_ library to execute Assible playbooks in a more efficient way (decreases the execution time).
- `nanvault <https://github.com/marcobellaccini/nanvault>`_ - a standalone tool to encrypt and decrypt files in the Assible Vault format, featuring UNIX-style composability.
- `OpsTools-assible <https://github.com/centos-opstools/opstools-assible>`_ - uses Assible to configure an environment that provides the support of `OpsTools <https://wiki.centos.org/SpecialInterestGroup/OpsTools>`_, namely centralized logging and analysis, availability monitoring, and performance monitoring.
- `TD4A <https://github.com/cidrblock/td4a>`_ - a template designer for automation. TD4A is a visual design aid for building and testing jinja2 templates. It will combine data in yaml format with a jinja2 template and render the output.
- `PHP-Assible <https://github.com/maschmann/php-assible>`_ - an object oriented Assible wrapper for PHP.

