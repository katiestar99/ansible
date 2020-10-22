# This code is part of Assible, but is an independent component.
# This particular file snippet, and this file snippet only, is BSD licensed.
# Modules you write using this snippet, which is embedded dynamically by Assible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# (c) 2017 Red Hat Inc.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


from assible.module_utils.facts.other.facter import FacterFactCollector
from assible.module_utils.facts.other.ohai import OhaiFactCollector

from assible.module_utils.facts.system.apparmor import ApparmorFactCollector
from assible.module_utils.facts.system.caps import SystemCapabilitiesFactCollector
from assible.module_utils.facts.system.chroot import ChrootFactCollector
from assible.module_utils.facts.system.cmdline import CmdLineFactCollector
from assible.module_utils.facts.system.distribution import DistributionFactCollector
from assible.module_utils.facts.system.date_time import DateTimeFactCollector
from assible.module_utils.facts.system.env import EnvFactCollector
from assible.module_utils.facts.system.dns import DnsFactCollector
from assible.module_utils.facts.system.fips import FipsFactCollector
from assible.module_utils.facts.system.local import LocalFactCollector
from assible.module_utils.facts.system.lsb import LSBFactCollector
from assible.module_utils.facts.system.pkg_mgr import PkgMgrFactCollector
from assible.module_utils.facts.system.pkg_mgr import OpenBSDPkgMgrFactCollector
from assible.module_utils.facts.system.platform import PlatformFactCollector
from assible.module_utils.facts.system.python import PythonFactCollector
from assible.module_utils.facts.system.selinux import SelinuxFactCollector
from assible.module_utils.facts.system.service_mgr import ServiceMgrFactCollector
from assible.module_utils.facts.system.ssh_pub_keys import SshPubKeyFactCollector
from assible.module_utils.facts.system.user import UserFactCollector

from assible.module_utils.facts.hardware.base import HardwareCollector
from assible.module_utils.facts.hardware.aix import AIXHardwareCollector
from assible.module_utils.facts.hardware.darwin import DarwinHardwareCollector
from assible.module_utils.facts.hardware.dragonfly import DragonFlyHardwareCollector
from assible.module_utils.facts.hardware.freebsd import FreeBSDHardwareCollector
from assible.module_utils.facts.hardware.hpux import HPUXHardwareCollector
from assible.module_utils.facts.hardware.hurd import HurdHardwareCollector
from assible.module_utils.facts.hardware.linux import LinuxHardwareCollector
from assible.module_utils.facts.hardware.netbsd import NetBSDHardwareCollector
from assible.module_utils.facts.hardware.openbsd import OpenBSDHardwareCollector
from assible.module_utils.facts.hardware.sunos import SunOSHardwareCollector

from assible.module_utils.facts.network.base import NetworkCollector
from assible.module_utils.facts.network.aix import AIXNetworkCollector
from assible.module_utils.facts.network.darwin import DarwinNetworkCollector
from assible.module_utils.facts.network.dragonfly import DragonFlyNetworkCollector
from assible.module_utils.facts.network.fc_wwn import FcWwnInitiatorFactCollector
from assible.module_utils.facts.network.freebsd import FreeBSDNetworkCollector
from assible.module_utils.facts.network.hpux import HPUXNetworkCollector
from assible.module_utils.facts.network.hurd import HurdNetworkCollector
from assible.module_utils.facts.network.linux import LinuxNetworkCollector
from assible.module_utils.facts.network.iscsi import IscsiInitiatorNetworkCollector
from assible.module_utils.facts.network.nvme import NvmeInitiatorNetworkCollector
from assible.module_utils.facts.network.netbsd import NetBSDNetworkCollector
from assible.module_utils.facts.network.openbsd import OpenBSDNetworkCollector
from assible.module_utils.facts.network.sunos import SunOSNetworkCollector

from assible.module_utils.facts.virtual.base import VirtualCollector
from assible.module_utils.facts.virtual.dragonfly import DragonFlyVirtualCollector
from assible.module_utils.facts.virtual.freebsd import FreeBSDVirtualCollector
from assible.module_utils.facts.virtual.hpux import HPUXVirtualCollector
from assible.module_utils.facts.virtual.linux import LinuxVirtualCollector
from assible.module_utils.facts.virtual.netbsd import NetBSDVirtualCollector
from assible.module_utils.facts.virtual.openbsd import OpenBSDVirtualCollector
from assible.module_utils.facts.virtual.sunos import SunOSVirtualCollector

# these should always be first due to most other facts depending on them
_base = [
    PlatformFactCollector,
    DistributionFactCollector,
    LSBFactCollector
]

# These restrict what is possible in others
_restrictive = [
    SelinuxFactCollector,
    ApparmorFactCollector,
    ChrootFactCollector,
    FipsFactCollector
]

# general info, not required but probably useful for other facts
_general = [
    PythonFactCollector,
    SystemCapabilitiesFactCollector,
    PkgMgrFactCollector,
    OpenBSDPkgMgrFactCollector,
    ServiceMgrFactCollector,
    CmdLineFactCollector,
    DateTimeFactCollector,
    EnvFactCollector,
    SshPubKeyFactCollector,
    UserFactCollector
]

# virtual, this might also limit hardware/networking
_virtual = [
    VirtualCollector,
    DragonFlyVirtualCollector,
    FreeBSDVirtualCollector,
    LinuxVirtualCollector,
    OpenBSDVirtualCollector,
    NetBSDVirtualCollector,
    SunOSVirtualCollector,
    HPUXVirtualCollector
]

_hardware = [
    HardwareCollector,
    AIXHardwareCollector,
    DarwinHardwareCollector,
    DragonFlyHardwareCollector,
    FreeBSDHardwareCollector,
    HPUXHardwareCollector,
    HurdHardwareCollector,
    LinuxHardwareCollector,
    NetBSDHardwareCollector,
    OpenBSDHardwareCollector,
    SunOSHardwareCollector
]

_network = [
    DnsFactCollector,
    FcWwnInitiatorFactCollector,
    NetworkCollector,
    AIXNetworkCollector,
    DarwinNetworkCollector,
    DragonFlyNetworkCollector,
    FreeBSDNetworkCollector,
    HPUXNetworkCollector,
    HurdNetworkCollector,
    IscsiInitiatorNetworkCollector,
    NvmeInitiatorNetworkCollector,
    LinuxNetworkCollector,
    NetBSDNetworkCollector,
    OpenBSDNetworkCollector,
    SunOSNetworkCollector
]

# other fact sources
_extra_facts = [
    LocalFactCollector,
    FacterFactCollector,
    OhaiFactCollector
]

# TODO: make config driven
collectors = _base + _restrictive + _general + _virtual + _hardware + _network + _extra_facts
