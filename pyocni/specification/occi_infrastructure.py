# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

# Copyright (C) 2011 Houssem Medhioub - Institut Mines-Telecom
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library.  If not, see <http://www.gnu.org/licenses/>.

"""
Created on Feb 25, 2011

@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@version: 0.1.1
@license: LGPL - Lesser General Public License
"""

# ====================================================================
# OCCI Infrastructure version 1.1
# ====================================================================

from pyocni.specification.occi_core import Attribute, Category, Kind, Mixin, Resource, Link, Action
#==== INFO: enum is under Python licence
from pyocni.pyocni_tools.Enum import Enum


class Compute(Resource):
    """

    The Compute type represents a generic information processing resource, e.g. a virtual machine.
    Compute inherits the Resource base type defined in OCCI Core Model

    """
    # Enumeration for CPU Architecture of the instance
    _cpu_architecture = Enum('x86', 'x64')
    # Enumeration for current state of the instance
    _compute_state = Enum('active', 'inactive', 'suspended')

    # Start action
    _action_start_category = Category(term='start',
                                      scheme='http://schemas.ogf/occi/infrastructure/compute/action',
                                      title='Start a compute resource',
                                      attributes=())
    _action_start = Action(_action_start_category)

    # Stop action
    _action_stop_category = Category(term='stop',
                                     scheme='http://schemas.ogf/occi/infrastructure/compute/action',
                                     title='Stop a compute resource',
                                     attributes=(Attribute(name='method', mutable=True), ))
    _action_stop = Action(_action_stop_category)

    # Restart action
    _action_restart_category = Category(term='restart',
                                        scheme='http://schemas.ogf/occi/infrastructure/compute/action',
                                        title='Restart a compute resource',
                                        attributes=(Attribute(name='method', mutable=True), ))
    _action_restart = Action(_action_restart_category)

    # Suspend action
    _action_suspend_category = Category(term='suspend',
                                        scheme='http://schemas.ogf/occi/infrastructure/compute/action',
                                        title='Suspend a compute resource',
                                        attributes=(Attribute(name='method', mutable=True), ))
    _action_suspend = Action(_action_suspend_category)

    # The kind instance assigned to the compute type
    _kind = Kind(term='compute',
                 scheme='http://schemas.ogf.org/occi/infrastructure',
                 entity_type=Resource,
                 title='compute resource',
                 attributes=(Attribute(name='occi.compute.architecture', mutable=True),
                             Attribute(name='occi.compute.cores', mutable=True),
                             Attribute(name='occi.compute.hostname', mutable=True),
                             Attribute(name='occi.compute.speed', mutable=True),
                             Attribute(name='occi.compute.memory', mutable=True),
                             Attribute(name='occi.compute.state', required=True)),
                 actions=(_action_start,
                          _action_stop,
                          _action_restart,
                          _action_suspend),
                 related=(Resource._kind, ),
                 entities=())

    def __init__(self, occi_core_id, occi_compute_state, kind=_kind, occi_core_title='', mixins=[], occi_core_summary='',
                 links=[], occi_compute_architecture='', occi_compute_cores=0, occi_compute_hostname='',
                 occi_compute_speed=0.0, occi_compute_memory=0):
        super(Compute, self).__init__(occi_core_id=occi_core_id,
                                      kind=kind,
                                      occi_core_title=occi_core_title,
                                      mixins=mixins,
                                      occi_core_summary=occi_core_summary,
                                      links=links)
        # CPU architecture of the instance
        # occi.compute.architecture
        # @AttributeType Enum {x86, x64}
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.occi_compute_architecture = occi_compute_architecture

        # Number of CPU cores assigned to the instance
        # occi.compute.cores
        # @AttributeType integer
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.occi_compute_cores = occi_compute_cores

        # Fully Qualified DNS hostname for the instance
        # occi.compute.hostname
        # @AttributeType string
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.occi_compute_hostname = occi_compute_hostname

        # CPU Clock frequency (speed) in gigahertz
        # occi.compute.speed
        # @AttributeType Float, 10expo(9) (GHz)
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.occi_compute_speed = occi_compute_speed

        # Maximum RAM in gigabytes allocated to the instance
        # occi.compute.memory
        # @AttributeType Float, 10expo(9) (GiB)
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.occi_compute_memory = occi_compute_memory

        # Current state of the instance
        # occi.compute.state
        # @AttributeType Enum {active, inactive, suspended}
        # @AttributeMultiplicity 1
        # @AttributeMutability immutable
        self.occi_compute_state = occi_compute_state or self._compute_state.inactive


class Network(Resource):
    """

    The network type represents a L2 networking entity (e.g. virtual switch).
    It can be extended using the mixin mechanism (or sub-typed) to support L3/L4 capabilities such as TCP/IP etc.

    """

    # Enumeration for current state of the instance
    _network_state = Enum('active', 'inactive')

    # UP action
    _action_up_category = Category(term='up',
                                   scheme='http://schemas.ogf/occi/infrastructure/network/action',
                                   title='turn UP a network',
                                   attributes=())
    _action_up = Action(_action_up_category)

    # DOWN action
    _action_down_category = Category(term='down',
                                     scheme='http://schemas.ogf/occi/infrastructure/network/action',
                                     title='turn DOWN a network',
                                     attributes=())
    _action_down = Action(_action_down_category)

    # The kind instance assigned to the network type
    _kind = Kind(term='network',
                 scheme='http://schemas.ogf.org/occi/infrastructure',
                 entity_type=Resource,
                 title='network resource',
                 attributes=(Attribute(name='occi.network.vlan', mutable=True),
                             Attribute(name='occi.network.label', mutable=True),
                             Attribute(name='occi.network.state', required=True)),
                 actions=(_action_up,
                          _action_down),
                 related=(Resource._kind, ),
                 entities=())

    def __init__(self, occi_core_id, occi_network_state, kind=_kind, occi_core_title='', mixins=[], occi_core_summary='',
                 links=[], occi_network_vlan=0, occi_network_label=''):
        super(Network, self).__init__(occi_core_id=occi_core_id,
                                      kind=kind,
                                      occi_core_title=occi_core_title,
                                      mixins=mixins,
                                      occi_core_summary=occi_core_summary,
                                      links=links)
        # 802.1q VLAN identifier (e.g. 343)
        # occi.network.vlan
        # @AttributeType integer: 0-4095
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.occi_network_vlan = occi_network_vlan

        # Tag based VLANs (e.g. external-dmz)
        # occi.network.label
        # @AttributeType Token
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.occi_network_label = occi_network_label

        # Current state of the instance
        # occi.network.state
        # @AttributeType Enum {active, inactive}
        # @AttributeMultiplicity 1
        # @AttributeMutability immutable
        self.occi_network_state = occi_network_state or self._network_state.inactive


class Storage(Resource):
    """

    The storage type represent resources that record information to a data storage device.

    """

    # Enumeration for current state of the instance
    _storage_state = Enum('online', 'offline', 'backup', 'snapshot', 'resize', 'degraded')

    # online action
    _action_online_category = Category(term='online',
                                       scheme='http://schemas.ogf/occi/infrastructure/storage/action',
                                       title='turn Online a storage',
                                       attributes=())
    _action_online = Action(_action_online_category)

    # offline action
    _action_offline_category = Category(term='offline',
                                        scheme='http://schemas.ogf/occi/infrastructure/storage/action',
                                        title='turn Offline a storage',
                                        attributes=())
    _action_offline = Action(_action_offline_category)

    # backup action
    _action_backup_category = Category(term='backup',
                                       scheme='http://schemas.ogf/occi/infrastructure/storage/action',
                                       title='backup a storage',
                                       attributes=())
    _action_backup = Action(_action_backup_category)

    # snapshot action
    _action_snapshot_category = Category(term='snapshot',
                                         scheme='http://schemas.ogf/occi/infrastructure/storage/action',
                                         title='snapshot a storage',
                                         attributes=())
    _action_snapshot = Action(_action_snapshot_category)

    # resize action
    _action_resize_category = Category(term='resize',
                                       scheme='http://schemas.ogf/occi/infrastructure/storage/action',
                                       title='resize a storage',
                                       attributes=(Attribute(name='size', required=True, mutable=True), ))
    _action_resize = Action(_action_resize_category)

    # The kind instance assigned to the storage type
    _kind = Kind(term='storage',
                 scheme='http://schemas.ogf.org/occi/infrastructure',
                 entity_type=Resource,
                 title='storage resource',
                 attributes=(Attribute(name='occi.storage.size', required=True, mutable=True),
                             Attribute(name='occi.storage.state', required=True)),
                 actions=(_action_online,
                          _action_offline,
                          _action_backup,
                          _action_snapshot,
                          _action_resize),
                 related=(Resource._kind, ),
                 entities=())

    def __init__(self, occi_core_id, occi_storage_size, occi_storage_state, kind=_kind, occi_core_title='', mixins=[],
                 occi_core_summary='', links=[]):
        super(Storage, self).__init__(occi_core_id=occi_core_id,
                                      kind=kind,
                                      occi_core_title=occi_core_title,
                                      mixins=mixins,
                                      occi_core_summary=occi_core_summary,
                                      links=links)

        # Storage size in gigabytes of the instance
        # occi.storage.size
        # @AttributeType Float, 10expo(9) (GiB)
        # @AttributeMultiplicity 1
        # @AttributeMutability mutable
        self.occi_storage_size = occi_storage_size or 0

        # Current state of the instance
        # occi.storage.state
        # @AttributeType Enum(online, offline, backup, snapshot, resize, degraded)
        # @AttributeMultiplicity 1
        # @AttributeMutability immutable
        self.occi_storage_state = occi_storage_state or self._storage_state.offline


class NetworkInterface(Link):
    """

    The network_interface type represents an L2 client device (e.g. network adapter).
    It can be extended using the mix-in mechanism or sub-typed to support L3/L4 capabilities such as TCP/IP etc.
    network_interface inherits the link base type defined in the OCCI Core Model.

    """

    # Enumeration for current state of the instance
    _network_interface_state = Enum('active', 'inactive')

    # The kind instance assigned to the network_interface type
    _kind = Kind(term='networkinterface',
                 scheme='http://schemas.ogf.org/occi/infrastructure',
                 entity_type=Link,
                 title='network interface link',
                 attributes=(Attribute(name='occi.networkinterface.interface', required=True),
                             Attribute(name='occi.networkinterface.mac', required=True, mutable=True),
                             Attribute(name='occi.networkinterface.state', required=True)),
                 actions=(),
                 related=(Link._kind, ),
                 entities=())

    def __init__(self, occi_core_id, occi_core_source, occi_core_target, occi_networkinterface_interface,
                 occi_networkinterface_mac, occi_networkinterface_state, kind=_kind, occi_core_title='', mixins=[]):
        super(NetworkInterface, self).__init__(occi_core_id=occi_core_id,
                                               kind=kind,
                                               occi_core_source=occi_core_source,
                                               occi_core_target=occi_core_target,
                                               occi_core_title=occi_core_title,
                                               mixins=mixins)

        # identifier that relates the link to the link's device interface
        # occi.networkinterface.interface
        # @AttributeType string
        # @AttributeMultiplicity 1
        # @AttributeMutability immutable
        self.occi_networkinterface_interface = occi_networkinterface_interface

        # MAC address associated with the link's device interface
        # occi.networkinterface.mac
        # @AttributeType string
        # @AttributeMultiplicity 1
        # @AttributeMutability mutable
        self.occi_networkinterface_mac = occi_networkinterface_mac

        # Current state of the instance
        # occi.networkinterface.state
        # @AttributeType Enum(active, inactive)
        # @AttributeMultiplicity 1
        # @AttributeMutability immutable
        self.occi_networkinterface_state = occi_networkinterface_state or self._network_interface_state.inactive


class StorageLink(Link):
    """

    The storage_link type represents a link from a resource to a target storage instance.
    This enables a storage instance be attached to a compute instance, with all the prerequisite low-level
        operations handled by the OCCI implementation.
    storage inherits the link base type defined in the OCCI Core Model.

    """

    # Enumeration for current state of the instance
    _storage_link_state = Enum('active', 'inactive')

    # The kind instance assigned to the storage_link type
    _kind = Kind(term='storagelink',
                 scheme='http://schemas.ogf.org/occi/infrastructure',
                 entity_type=Link,
                 title='storage link',
                 attributes=(Attribute(name='occi.storagelink.deviceid', required=True, mutable=True),
                             Attribute(name='occi.storagelink.mountpoint', mutable=True),
                             Attribute(name='occi.storagelink.state', required=True)),
                 actions=(),
                 related=(Link._kind, ),
                 entities=())

    def __init__(self, occi_core_id, occi_core_source, occi_core_target, occi_storagelink_deviceid,
                 occi_storagelink_state, occi_storagelink_mountpoint='', kind=_kind, occi_core_title='', mixins=[]):
        super(StorageLink, self).__init__(occi_core_id=occi_core_id,
                                          kind=kind,
                                          occi_core_source=occi_core_source,
                                          occi_core_target=occi_core_target,
                                          occi_core_title=occi_core_title,
                                          mixins=mixins)

        # Device identifier as defined by the OCCI service provider
        # occi.storagelink.deviceid
        # @AttributeType string
        # @AttributeMultiplicity 1
        # @AttributeMutability mutable
        self.occi_storagelink_deviceid = occi_storagelink_deviceid

        # point to where the storage is mounted in the guest OS
        # occi.storagelink.mountpoint
        # @AttributeType string
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.occi_storagelink_mountpoint = occi_storagelink_mountpoint

        # Current state of the instance
        # occi.storagelink.state
        # @AttributeType Enum(active, inactive)
        # @AttributeMultiplicity 1
        # @AttributeMutability immutable
        self.occi_storagelink_state = occi_storagelink_state or self._storage_link_state.inactive


class IPNetworking(Mixin):
    """

    Mixin
    In order to support L3/L4 capabilities (e.g. IP, TCP etc.) an OCCI mixin is herewith defined.

    """

    # Enumeration for the address allocation mechanism
    _ip_networking_state = Enum('dynamic', 'static')

    def __init__(self, occi_network_address='', occi_network_gateway='',
                 occi_network_allocation=_ip_networking_state.static):
        super(IPNetworking, self).__init__(term='ipnetwork',
                                           scheme='http://schemas.ogf.org/occi/infrastructure/network',
                                           title='ip network mixin',
                                           attributes=(Attribute(name='occi.network.address', mutable=True),
                                                       Attribute(name='occi.network.gateway', mutable=True),
                                                       Attribute(name='occi.network.allocation', mutable=True)),
                                           actions=(),
                                           related=(),
                                           entities=[])

        # Internet protocol (IP) network address (e.g. 192.168.0.1/24, fc@@::/7)
        # occi.network.address
        # @AttributeType IPv4 or IPV6 Address range, CIDR notation
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.occi_network_address = occi_network_address

        # Internet Protocol (IP) network address (e.g. 192.168.0.1, fc00::)
        # occi.network.gateway
        # @AttributeType IPv4 or IPV6 Address
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.occi_network_gateway = occi_network_gateway

        # Address allocation mechanism: dynamic e.g. uses the dynamic host configuration protocol,
        #    static e.g. uses user supplied static network configurations
        # occi.network.allocation
        # @AttributeType Enum {dynamic, static}
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.occi_network_allocation = occi_network_allocation


class IPNetworkInterface(Mixin):
    """

    Mixin
    In order to support L3/L4 capabilities (e.g. IP, TCP etc.) with the network_interface type,
        an OCCI mixin instance is herewith defined.

    """

    # Enumeration for the address allocation mechanism
    _ip_network_interface_state = Enum('dynamic', 'static')

    def __init__(self, occi_networkinterface_address='', occi_networkinterface_gateway='',
                 occi_networkinterface_allocation=_ip_network_interface_state.static):
        super(IPNetworkInterface, self).__init__(term='ipnetworkinterface',
                                                 scheme='http://schemas.ogf.org/occi/infrastructure/networkinterface',
                                                 title='ip network interface mixin',
                                                 attributes=(
                                                     Attribute(name='occi.networkinterface.address', required=True,
                                                               mutable=True),
                                                     Attribute(name='occi.networkinterface.gateway', mutable=True),
                                                     Attribute(name='occi.networkinterface.allocation', required=True,
                                                               mutable=True)),
                                                 actions=(),
                                                 related=(),
                                                 entities=[])
        # Internet Protocol (IP network address (e.g. 192.168.0.1/24, fc00::/7) of the link
        # occi.networkinterface.address
        # @AttributeType IPv4 or IPV6 Address
        # @AttributeMultiplicity 1
        # @AttributeMutability mutable
        self.occi_networkinterface_address = occi_networkinterface_address

        # Internet Protocol (IP network address (e.g. 192.168.0.1/24, fc00::/7)
        # occi.networkinterface.gateway
        # @AttributeType IPv4 or IPV6 Address
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.occi_networkinterface_gateway = occi_networkinterface_gateway

        # Address allocation mechanism: dynamic e.g. uses the dynamic host configuration protocol,
        #    static e.g. uses user supplied static network configurations
        # occi.networkinterface.allocation
        # @AttributeType Enum {dynamic, static}
        # @AttributeMultiplicity 1
        # @AttributeMutability mutable
        self.occi_networkinterface_allocation = occi_networkinterface_allocation


class os_tpl(Mixin):
    """

    Mixin
    OCCI OS Template Mixin
    OS (Operating System) Templates allow clients specific what operating system must be installed
        on a requested Compute resource.
    A implementation-defined OS Template Mixin MUST be related to the OCCI OS Template Mixin
        in order to give absolute type information.


    """

    def __init__(self):
        super(os_tpl, self).__init__(term='os_tpl',
                                     scheme='http://schemas.ogf.org/occi/infrastructure',
                                     title='OCCI OS template mixin',
                                     attributes=(),
                                     actions=(),
                                     related=(),
                                     entities=[])
        pass


class resource_tpl(Mixin):
    """

    Mixin
    OCCI Resource template Mixin
    A resource Template is a provider defined Mixin instance that refers to a preset Resource configuration.
    The Mixin.attributes (inherits from Category) is empty for a Template Mixin.
    An implementation-defined Resource Template Mixin MUST be related to the OCCI Resource Template Mixin
        in order to give absolute type information.

    """

    def __init__(self):
        super(resource_tpl, self).__init__(term='resource_tpl',
                                           scheme='http://schemas.ogf.org/occi/infrastructure',
                                           title='OCCI resource template mixin',
                                           attributes=(),
                                           actions=(),
                                           related=(),
                                           entities=[])
        pass

if __name__ == '__main__':
    pass
