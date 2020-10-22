====================
Assible project 2.11
====================

This release schedule includes dates for the `assible <https://pypi.org/project/assible/>`_ package, with a few dates for the `assible-base <https://pypi.org/project/assible-base/>`_ package as well. All dates are subject to change. See :ref:`base_roadmap_2_11` for the most recent updates on ``assible-base``.

.. contents::
   :local:

Release schedule
=================

.. note:: Dates subject to change.

- ????-??-?? Assible 2.11 alpha freeze. No net new collections allowed after this date.
- ????-??-?? Assible collections freeze date for content moving between collections.
- ????-??-?? Assible 2.11 alpha.
- ????-??-?? Assible 2.11.0 beta1 and feature freeze.

  - No new modules or major features accepted after this date. In practice this means we will freeze the semver collection versions to compatible release versions. For example, if the version of community.crypto on this date was community-crypto-2.1.0; assible-2.11.0 could ship with community-crypto-2.1.1.  It would not ship with community-crypto-2.2.0.

- ????-??-?? Assible 2.11 final freeze/rc1.

  - After this date only changes blocking a release are accepted.
  - Collections will only be updated to a new version if a blocker is approved.  Collection owners should discuss any blockers at a community IRC meeting (before this freeze) to decide whether to bump the version of the collection for a fix. See the `Community IRC meeting agenda <https://github.com/assible/community/issues/539>`_.

** Additional release candidates to be published as needed as blockers are fixed **

- ????-??-?? Assible 2.11 GA release date.

.. note::

  Breaking changes may be introduced in Assible 2.11.0, although we encourage collection owners to use deprecation periods that will show up in at least one Assible release before being changed incompatibly.


Assible patch releases
=======================

Assible 2.11.x patch releases will occur approximately every three weeks if changes to collections have been made or if it is deemed necessary to force an upgrade to a later assible-base-2.11.x.  Assible 2.11.x patch releases may contain new features but not backwards incompatibilities.  In practice, this means we will include new collection versions where either the patch or the minor version number has changed but not when the major number has changed. For example: if Assible-2.11 ships with community-crypto-2.1.0; assible-2.11.1 may ship with community-crypto-2.2.0 but would not ship with community-crypto-3.0.0).


For more information, reach out on a mailing list or an IRC channel - see :ref:`communication` for more details.
