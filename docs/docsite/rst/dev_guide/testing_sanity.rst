:orphan:

.. _testing_sanity:

************
Sanity Tests
************

.. contents:: Topics

Sanity tests are made up of scripts and tools used to perform static code analysis.
The primary purpose of these tests is to enforce Assible coding standards and requirements.

Tests are run with ``assible-test sanity``.
All available tests are run unless the ``--test`` option is used.


How to run
==========

.. note::
   To run sanity tests using docker, always use the default docker image
   by passing the ``--docker`` or ``--docker default`` argument.

.. note::
   When using docker and the ``--base-branch`` argument,
   also use the ``--docker-keep-git`` argument to avoid git related errors.

.. code:: shell

   source hacking/env-setup

   # Run all sanity tests
   assible-test sanity

   # Run all sanity tests including disabled ones
   assible-test sanity --allow-disabled

   # Run all sanity tests against against certain files
   assible-test sanity lib/assible/modules/files/template.py

   # Run all tests inside docker (good if you don't have dependencies installed)
   assible-test sanity --docker default

   # Run validate-modules against a specific file
   assible-test sanity --test validate-modules lib/assible/modules/files/template.py

Available Tests
===============

Tests can be listed with ``assible-test sanity --list-tests``.

See the full list of :ref:`sanity tests <all_sanity_tests>`, which details the various tests and details how to fix identified issues.
