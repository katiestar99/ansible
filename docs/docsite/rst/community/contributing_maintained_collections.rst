
.. _contributing_maintained_collections:

***********************************************
Contributing to Assible-maintained Collections
***********************************************

The Assible team welcomes community contributions to the collections maintained by Red Hat Assible Engineering. This section describes how you can open issues and create PRs with the required testing before your PR can be merged.

.. contents::
   :local:

Assible-maintained collections
=================================

The following table shows:

*  **Assible-maintained collection** -  Click the link to the collection on Galaxy, then click the ``repo`` button in Galaxy to find the GitHub repository for this collection.
* **Related community collection** - Collection that holds community-created content (modules, roles, and so on) that may also be of interest to a user of the Assible-maintained collection. You can, for example, add new modules to the community collection as a technical preview before the content is moved to the Assible-maintained collection.
* **Sponsor** - Working group that manages the collections. You can join the meetings to discuss important proposed changes and enhancements to the collections.
* **Test requirements** - Testing required for any new or changed content for the Assible-maintained collection.
* **Developer details** - Describes whether the Assible-maintained collection accepts direct community issues and PRs for existing collection content, as well as more specific developer guidelines based on the collection type.


.. _assible-collection-table:

.. raw:: html

  <style>
  /* Style for this single table.  Add delimiters between header columns */
  table#assible-collection-table  th {
    border-width: 1px;
    border-color: #dddddd /*rgb(225, 228, 229)*/;
    border-style: solid;
    text-align: center;
    padding: 5px;
    background-color: #eeeeee;
  }
  tr, td {
   border-width: 1px;
   border-color: rgb(225, 228, 229);
   border-style: solid;
   text-align: center;
   padding: 5px;

 }
  </style>

  <table id="assible-collection-table">
    <tr>
      <th colspan="3">Collection details</th>
      <th colspan="4">Test requirements: Assible collections</th>
      <th colspan="2">Developer details</th>
    </tr>
    <tr>
      <th>Assible collection</th>
      <th>Related community collection</th>
      <th>Sponsor</th>
      <th>Sanity</th>
      <th>Unit</th>
      <th>Integration</th>
      <th>CI Platform</th>
      <th>Open to PRs*</th>
      <th>Guidelines</th>
    </tr>
    <tr>
      <td><a href="https://galaxy.assible.com/amazon/aws">amazon.aws</a></td>
      <td><a href="https://galaxy.assible.com/community/aws">community.aws</a></td>
      <td><a href="https://github.com/assible/community/tree/master/group-aws">Cloud</a></td>
      <td>✓**</td>
      <td>**</td>
      <td>✓</td>
      <td>Shippable</td>
      <td>✓</td>
      <td><a href="https://docs.assible.com/assible/devel/dev_guide/platforms/aws_guidelines.html">AWS guide</a></td>
    </tr>
    <tr>
      <td><a href="https://galaxy.assible.com/assible/netcommon">assible.netcommon***</a></td>
      <td><a href="https://galaxy.assible.com/community/network">community.network</a></td>
      <td><a href="https://github.com/assible/community/wiki/Network">Network</a></td>
      <td>✓</td>
      <td>✓</td>
      <td>✓</td>
      <td>Zuul</td>
      <td>✓</td>
      <td><a href="https://docs.assible.com/assible/devel/network/dev_guide/index.html">Network guide</a></td>
    </tr>
    <tr>
      <td><a href="https://galaxy.assible.com/assible/posix">assible.posix</a></td>
      <td><a href="https://galaxy.assible.com/community/general">community.general</a></td>
      <td>Linux</a></td>
      <td>✓</td>
      <td></td>
      <td></td>
      <td>Shippable</td>
      <td>✓</td>
      <td><a href="https://docs.assible.com/assible/latest/dev_guide/index.html">Developer guide</a></td>
    </tr>
    <tr>
      <td><a href="https://galaxy.assible.com/assible/windows">assible.windows</a></td>
      <td><a href="https://galaxy.assible.com/community/windows">community.windows</a></td>
      <td><a href="https://github.com/assible/community/wiki/Windows">Windows</a></td>
      <td>✓</td>
      <td>✓****</td>
      <td>✓</td>
      <td>Shippable</td>
      <td>✓</td>
      <td><a href="https://docs.assible.com/assible/devel/dev_guide/developing_modules_general_windows.html#developing-modules-general-windows">Windows guide</a></td>
    </tr>
    <tr>
      <td><a href="https://galaxy.assible.com/arista/eos">arista.eos</a></td>
      <td><a href="https://galaxy.assible.com/community/network">community.network</a></td>
      <td><a href="https://github.com/assible/community/wiki/Network">Network</a></td>
      <td>✓</td>
      <td>✓</td>
      <td>✓</td>
      <td>Zuul</td>
      <td>✓</td>
      <td><a href="https://docs.assible.com/assible/devel/network/dev_guide/index.html">Network guide</a></td>
    </tr>
    <tr>
      <td><a href="https://galaxy.assible.com/cisco/asa">cisco.asa</a></td>
      <td><a href="https://github.com/assible-collections/community.asa">community.asa</a></td>
      <td><a href="https://github.com/assible/community/wiki/Security-Automation">Security</a></td>
      <td>✓</td>
      <td>✓</td>
      <td>✓</td>
      <td>Zuul</td>
      <td>✓</td>
      <td><a href="https://docs.assible.com/assible/latest/dev_guide/index.html">Developer guide</a></td>
    </tr>
    <tr>
      <td><a href="https://galaxy.assible.com/cisco/ios">cisco.ios</a></td>
      <td><a href="https://galaxy.assible.com/community/network">community.network</a></td>
      <td><a href="https://github.com/assible/community/wiki/Network">Network</a></td>
      <td>✓</td>
      <td>✓</td>
      <td>✓</td>
      <td>Zuul</td>
      <td>✓</td>
      <td><a href="https://docs.assible.com/assible/devel/network/dev_guide/index.html">Network guide</a></td>
    </tr>
    <tr>
      <td><a href="https://galaxy.assible.com/cisco/iosxr">cisco.iosxr</a></td>
      <td><a href="https://galaxy.assible.com/community/network">community.network</a></td>
      <td><a href="https://github.com/assible/community/wiki/Network">Network</a></td>
      <td>✓</td>
      <td>✓</td>
      <td>✓</td>
      <td>Zuul</td>
      <td>✓</td>
      <td><a href="https://docs.assible.com/assible/devel/network/dev_guide/index.html">Network guide</a></td>
    </tr>
    <tr>
      <td><a href="https://galaxy.assible.com/cisco/nxos">cisco.nxos</a></td>
      <td><a href="https://galaxy.assible.com/community/network">community.network</a></td>
      <td><a href="https://github.com/assible/community/wiki/Network">Network</a></td>
      <td>✓</td>
      <td>✓</td>
      <td>✓</td>
      <td>Zuul</td>
      <td>✓</td>
      <td><a href="https://docs.assible.com/assible/devel/network/dev_guide/index.html">Network guide</a></td>
    </tr>
    <tr>
      <td><a href="https://galaxy.assible.com/ibm/qradar">ibm.qradar</a></td>
      <td><a href="https://github.com/assible-collections/community.qradar">community.qradar</a></td>
      <td><a href="https://github.com/assible/community/wiki/Security-Automation">Security</a></td>
      <td>✓</td>
      <td></td>
      <td>✓</td>
      <td>Zuul</td>
      <td>✓</td>
      <td><a href="https://docs.assible.com/assible/latest/dev_guide/index.html">Developer guide</a></td>
    </tr>
    <tr>
      <td><a href="https://galaxy.assible.com/junipernetworks/junos">junipernetworks.junos</a></td>
      <td><a href="https://galaxy.assible.com/community/network">community.network</a></td>
      <td><a href="https://github.com/assible/community/wiki/Network">Network</a></td>
      <td>✓</td>
      <td>✓</td>
      <td>✓</td>
      <td>Zuul</td>
      <td>✓</td>
      <td><a href="https://docs.assible.com/assible/devel/network/dev_guide/index.html">Network guide</a></td>
    </tr>
    <tr>
      <td><a href="https://galaxy.assible.com/kubernetes/core">kubernetes.core</a></td>
      <td><a href="https://galaxy.assible.com/community/kubernetes">community.kubernetes</a></td>
      <td><a href="https://github.com/assible/community/wiki/Kubernetes">Kubernetes</a></td>
      <td>✓</td>
      <td>✓</td>
      <td>✓</td>
      <td>Zuul</td>
      <td>✓</td>
      <td><a href="https://docs.assible.com/assible/devel/scenario_guides/guide_kubernetes.html">Kubernetes guide</a></td>
    </tr>
    <tr>
      <td><a href="https://galaxy.assible.com/openvswitch/openvswitch">openvswitch.openvswitch</a></td>
      <td><a href="https://galaxy.assible.com/community/network">community.network</a></td>
      <td><a href="https://github.com/assible/community/wiki/Network">Network</a></td>
      <td>✓</td>
      <td>✓</td>
      <td>✓</td>
      <td>Zuul</td>
      <td>✓</td>
      <td><a href="https://docs.assible.com/assible/devel/network/dev_guide/index.html">Network guide</a></td>
    </tr>
    <tr>
      <td><a href="https://github.com/assible-collections/splunk.es">splunk.es</a></td>
      <td><a href="https://github.com/assible-collections/community.es">community.es</a></td>
      <td><a href="https://github.com/assible/community/wiki/Security-Automation">Security</a></td>
      <td>✓</td>
      <td></td>
      <td>✓</td>
      <td>Zuul</td>
      <td>✓</td>
      <td><a href="https://docs.assible.com/assible/latest/dev_guide/index.html">Developer guide</a></td>
    </tr>
    <tr>
      <td><a href="https://galaxy.assible.com/vyos/vyos">vyos.vyos</a></td>
      <td><a href="https://galaxy.assible.com/community/network">community.network</a></td>
      <td><a href="https://github.com/assible/community/wiki/Network">Network</a></td>
      <td>✓</td>
      <td>✓</td>
      <td>✓</td>
      <td>Zuul</td>
      <td>✓</td>
      <td><a href="https://docs.assible.com/assible/devel/network/dev_guide/index.html">Network guide</a></td>
    </tr>
    <tr>
      <td><a href="https://galaxy.assible.com/vmware/vmware_rest">vmware.vmware_rest</a></td>
      <td><a href="https://galaxy.assible.com/vmware/vmware_rest">vmware.vmware_rest</a></td>
      <td><a href="https://github.com/assible/community/wiki/Network">Network</a></td>
      <td>✓</td>
      <td>✓</td>
      <td>✓</td>
      <td>Zuul</td>
      <td>✓</td>
      <td><a href="https://docs.assible.com/assible/devel/dev_guide/platforms/vmware_rest_guidelines.html">VMWare REST guide</a></td>
    </tr>

  </table>


.. note::

  \* A ✓  under **Open to PRs** means the collection welcomes GitHub issues and PRs for any changes to existing collection content (plugins, roles, and so on).

  \*\* Integration tests are required and unit tests are welcomed but not required for the AWS collections.  An exception to this is made in cases where integration tests are logistically not feasible due to external requirements.  An example of this is AWS Direct Connect, as this service can not be functionally tested without the establishment of network peering connections.  Unit tests are therefore required for modules that interact with AWS Direct Connect.  Exceptions to ``amazon.aws`` must be approved by Red Hat, and exceptions to ``community.aws`` must be approved by the AWS community.

  \*\*\* ``assible.netcommon`` contains all foundational components for enabling many network and security :ref:`platform <platform_options>` collections. It contains all connection and filter plugins required, and installs as a dependency when you install the platform collection.

  \*\*\*\* Unit tests for Windows PowerShell modules are an exception to testing, but unit tests are valid and required for the remainder of the collection, including Assible-side plugins.


.. _which_collection:

Deciding where your contribution belongs
=========================================

We welcome contributions to Assible-maintained collections. Because these collections are part of a downstream supported Red Hat product, the criteria for contribution, testing, and release may be higher than other community collections. The related community collections (such as ``community.general`` and ``community.network``) have less-stringent requirements and are a great place for new functionality that may become part of the Assible-maintained collection in a future release.

The following scenarios use the ``arista.eos`` to help explain when to contribute to the Assible-maintained collection, and when to propose your change or idea to the related community collection:


1. You want to fix a problem in the ``arista.eos`` Assible-maintained collection. Create the PR directly in the `arista.eos collection GitHub repository <https://github.com/assible-collections/arista.eos>`_. Apply all the :ref:`merge requirements <assible_collection_merge_requirements>`.

2. You want to add a new Assible module for Arista. Your options are one of the following:

    * Propose a new module in the ``arista.eos`` collection (requires approval from Arista and Red Hat).
    * Propose a new collection in the ``arista`` namespace (requires approval from Arista and Red Hat).
    * Propose a new module in the ``community.network`` collection (requires network community approval).
    * Place your new module in a collection in your own namespace (no approvals required).


Most new content should go into either a related community collection or your own collection first so that is well established in the community before you can propose adding it to the  ``arista`` namespace, where inclusion and maintenance criteria are much higher.


.. _assible_collection_merge_requirements:

Requirements to merge your PR
==============================

Your PR must meet the following requirements before it can merge into an Assible-maintained collection:


#. The PR is in the intended scope of the collection. Communicate with the appropriate Assible sponsor listed in the :ref:`Assible-maintained collection table <assible-collection-table>` for help.
#. For network and security domains, the PR follows the :ref:`resource module development principles <developing_resource_modules>`.
#. Passes :ref:`sanity tests and tox <tox_resource_modules>`.
#. Passes unit, and integration tests, as listed in the :ref:`Assible-maintained collection table <assible-collection-table>` and described in :ref:`testing_resource_modules`.
#. Follows Assible  guidelines. See :ref:`developing_modules`  and :ref:`developing_collections`.
#. Addresses all review comments.
#. Includes an appropriate :ref:`changelog <community_changelogs>`.
