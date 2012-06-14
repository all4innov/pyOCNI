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
Created on Nov 10, 2011

@author: Houssem Medhioub
@author: Marouane Mechteri (for OpenFlow mixin)
@author: Hareesh Puthalath (for L3VPN mixin)
@author: Daniel Turull (for libnetvirt mixin)
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@version: 0.1.2
@license: LGPL - Lesser General Public License
"""

#====================================================================
#                        OCNI version 0.5
#====================================================================

from pyocni.specification.occi_core import Attribute, Category, Kind, Mixin, Resource, Link, Action
# ==== INFO: enum is under Python licence
from pyocni.pyocni_tools.Enum import Enum
# from datetime import datetime


class Availability(object):
    """
        Represent the entity of the availability interval

    """

    def __init__(self, ocni_availability_start='', ocni_availability_end=''):
        # start = datetime(year=2010, month=11, day=1, hour=14, minute=40, second=0)
        self.ocni_availability_start = ocni_availability_start
        self.ocni_availability_end = ocni_availability_end

    pass


class CloNeNode(Resource):
    """

    A networking resource of the Flash Network Slice

    """

    # Enumeration for current state of the instance
    _CloNeNode_state = Enum('active', 'inactive')

    # Start action
    _action_start_category = Category(term='start',
                                      scheme='http://schemas.ogf/occi/ocni/CloNeNode/action',
                                      title='Start a CloNeNode resource',
                                      attributes=())
    _action_start = Action(_action_start_category)

    # Stop action
    _action_stop_category = Category(term='stop',
                                     scheme='http://schemas.ogf/occi/ocni/CloNeNode/action',
                                     title='Stop a CloNeNode resource',
                                     attributes=())
    _action_stop = Action(_action_stop_category)

    # Restart action
    _action_restart_category = Category(term='restart',
                                        scheme='http://schemas.ogf/occi/ocni/CloNeNode/action',
                                        title='Restart a CloNeNode resource',
                                        attributes=())
    _action_restart = Action(_action_restart_category)

    # The kind instance assigned to the CloNeNode type
    _kind = Kind(term='CloNeNode',
                 scheme='http://schemas.ogf.org/occi/ocni',
                 entity_type=Resource,
                 title='Clone Node resource',
                 attributes=(
                     Attribute(name='ocni.clonenode.availability', type='pyocni.specification.ocni.Availability',
                               multiplicity='0.*', mutable=True),
                     Attribute(name='ocni.clonenode.location', mutable=True),
                     Attribute(name='ocni.clonenode.state', required=True)),
                 actions=(_action_start,
                          _action_stop,
                          _action_restart),
                 related=(Resource._kind, ),
                 entities=())

    def __init__(self, occi_core_id, ocni_clonenode_state, kind=_kind, occi_core_title='', mixins=[],
                 occi_core_summary='', links=[], ocni_clonenode_availability=(Availability(),),
                 ocni_clonenode_location=''):
        super(CloNeNode, self).__init__(occi_core_id=occi_core_id,
                                        kind=kind,
                                        occi_core_title=occi_core_title,
                                        mixins=mixins,
                                        occi_core_summary=occi_core_summary,
                                        links=links)
        # The proportion of time this entity is in a functioning condition
        # availability
        # @AttributeType Availability
        # @AttributeMultiplicity 0..*
        # @AttributeMutability mutable
        self.ocni_clonenode_availability = ocni_clonenode_availability

        # Current location of the instance
        # location
        # @AttributeType String
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.ocni_clonenode_location = ocni_clonenode_location

        # Current state of the instance
        # state
        # @AttributeType Enum {active, inactive}
        # @AttributeMultiplicity 1
        # @AttributeMutability immutable
        self.ocni_clonenode_state = ocni_clonenode_state or self._CloNeNode_state.inactive


class CloNeLink(Resource):
    """

    A network link of the Flash Network Slice

    """

    # Enumeration for current state of the instance
    _CloNeLink_state = Enum('active', 'inactive')

    # Enumeration for the routing scheme of the instance
    _CloNeLink_routing_scheme = Enum('unicast', 'multicast', 'broadcast', 'geocast')

    # UP action
    _action_up_category = Category(term='up',
                                   scheme='http://schemas.ogf/occi/ocni/CloNeLink/action',
                                   title='turn UP a CloNeLink',
                                   attributes=())
    _action_up = Action(_action_up_category)

    # DOWN action
    _action_down_category = Category(term='down',
                                     scheme='http://schemas.ogf/occi/ocni/CloNeLink/action',
                                     title='turn DOWN a CloNeLink',
                                     attributes=())
    _action_down = Action(_action_down_category)

    # The kind instance assigned to the CloNeLink type
    _kind = Kind(term='CloNeLink',
                 scheme='http://schemas.ogf.org/occi/ocni',
                 entity_type=Resource,
                 title='CloNeLink resource',
                 attributes=(
                     Attribute(name='ocni.clonelink.availability', type='pyocni.specification.ocni.Availability',
                               multiplicity='0.*', mutable=True),
                     Attribute(name='ocni.clonelink.state', required=True),
                     Attribute(name='ocni.clonelink.bandwidth', mutable=True),
                     Attribute(name='ocni.clonelink.latency', mutable=True),
                     Attribute(name='ocni.clonelink.jitter', mutable=True),
                     Attribute(name='ocni.clonelink.loss', mutable=True),
                     Attribute(name='ocni.clonelink.routing_scheme', mutable=True)),
                 actions=(_action_up,
                          _action_down),
                 related=(Resource._kind, ),
                 entities=())

    def __init__(self, occi_core_id, ocni_clonelink_state, kind=_kind, occi_core_title='', mixins=[],
                 occi_core_summary='', links=[], ocni_clonelink_availability=(Availability(),),
                 ocni_clonelink_bandwidth='', ocni_clonelink_latency='', ocni_clonelink_jitter='',
                 ocni_clonelink_loss='', ocni_clonelink_routing_scheme=''):
        super(CloNeLink, self).__init__(occi_core_id=occi_core_id,
                                        kind=kind,
                                        occi_core_title=occi_core_title,
                                        mixins=mixins,
                                        occi_core_summary=occi_core_summary,
                                        links=links)
        # The proportion of time this entity is in a functioning condition
        # availability
        # @AttributeType Availability
        # @AttributeMultiplicity 0..*
        # @AttributeMutability mutable
        self.ocni_clonelink_availability = ocni_clonelink_availability

        # Current state of the instance
        # state
        # @AttributeType Enum {active, inactive}
        # @AttributeMultiplicity 1
        # @AttributeMutability immutable
        self.ocni_clonelink_state = ocni_clonelink_state or self._CloNeLink_state.inactive

        # The data transfer rate of the instance's channel capacity
        # bandwidth
        # @AttributeType bits/second
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.ocni_clonelink_bandwidth = ocni_clonelink_bandwidth

        # Time delay for packet delivery of the instance
        # latency
        # @AttributeType Time
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.ocni_clonelink_latency = ocni_clonelink_latency

        # Variations in delay of packet delivery of the instance
        # jitter
        # @AttributeType Time
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.ocni_clonelink_jitter = ocni_clonelink_jitter

        # % of dropped packets of the instance
        # loss
        # @AttributeType %
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.ocni_clonelink_loss = ocni_clonelink_loss

        # The transmission type of the instance
        # routing_scheme
        # @AttributeType Enum {unicast, multicast, broadcast, geocast}
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.ocni_clonelink_routing_scheme = ocni_clonelink_routing_scheme


class FNS(Resource):
    """

    A resource that provides a network service

    """

    # Enumeration for current state of the instance
    _FNS_state = Enum('active', 'inactive')

    # Start action
    _action_start_category = Category(term='start',
                                      scheme='http://schemas.ogf/occi/ocni/FNS/action',
                                      title='Start a FNS resource',
                                      attributes=())
    _action_start = Action(_action_start_category)

    # Stop action
    _action_stop_category = Category(term='stop',
                                     scheme='http://schemas.ogf/occi/ocni/FNS/action',
                                     title='Stop a FNS resource',
                                     attributes=())
    _action_stop = Action(_action_stop_category)

    # Restart action
    _action_restart_category = Category(term='restart',
                                        scheme='http://schemas.ogf/occi/ocni/FNS/action',
                                        title='Restart a FNS resource',
                                        attributes=())
    _action_restart = Action(_action_restart_category)

    # The kind instance assigned to the FNS type
    _kind = Kind(term='FNS',
                 scheme='http://schemas.ogf.org/occi/ocni',
                 entity_type=Resource,
                 title='Flash Network Slice resource',
                 attributes=(Attribute(name='ocni.fns.availability', type='pyocni.specification.ocni.Availability',
                                       multiplicity='0.*', mutable=True),
                             Attribute(name='ocni.fns.state', required=True),
                             Attribute(name='ocni.fns.resources', multiplicity='1.*', mutable=True)),
                 actions=(_action_start,
                          _action_stop,
                          _action_restart),
                 related=(Resource._kind, ),
                 entities=())

    def __init__(self, occi_core_id, ocni_fns_state, kind=_kind, occi_core_title='', mixins=[],
                 occi_core_summary='', links=[], ocni_fns_availability=(Availability(),), ocni_fns_resources=('',)):
        super(FNS, self).__init__(occi_core_id=occi_core_id,
                                  kind=kind,
                                  occi_core_title=occi_core_title,
                                  mixins=mixins,
                                  occi_core_summary=occi_core_summary,
                                  links=links)

        # The proportion of time this entity is in a functioning condition
        # availability
        # @AttributeType Availability
        # @AttributeMultiplicity 0..*
        # @AttributeMutability mutable
        self.ocni_fns_availability = ocni_fns_availability

        # Current state of the instance
        # state
        # @AttributeType Enum {active, inactive}
        # @AttributeMultiplicity 1
        # @AttributeMutability immutable
        self.ocni_fns_state = ocni_fns_state or self._FNS_state.inactive

        # The resource instances composing the FNS instance
        # resources
        # @AttributeType resource
        # @AttributeMultiplicity 1..*
        # @AttributeMutability mutable
        self.ocni_fns_resources = ocni_fns_resources


class CloNeComputeLink(Link):
    """

    Connects a CloNeNode instance to a Compute instance

    """

    # Enumeration for current state of the instance
    _CloNeComputeLink_state = Enum('active', 'inactive')

    # The kind instance assigned to the CloNeComputeLink type
    _kind = Kind(term='CloNeComputeLink',
                 scheme='http://schemas.ogf.org/occi/ocni',
                 entity_type=Link,
                 title='CloNe Compute link',
                 attributes=(
                     Attribute(name='ocni.clonecomputelink.availability', type='pyocni.specification.ocni.Availability',
                               multiplicity='0.*', mutable=True),
                     Attribute(name='ocni.clonecomputelink.state', required=True)),
                 actions=(),
                 related=(Link._kind, ),
                 entities=())

    def __init__(self, occi_core_id, occi_core_source, occi_core_target, ocni_clonecomputelink_state, kind=_kind,
                 occi_core_title='', mixins=[], ocni_clonecomputelink_availability=(Availability(),)):
        super(CloNeComputeLink, self).__init__(occi_core_id=occi_core_id,
                                               kind=kind,
                                               occi_core_source=occi_core_source,
                                               occi_core_target=occi_core_target,
                                               occi_core_title=occi_core_title,
                                               mixins=mixins)

        # The proportion of time this entity is in a functioning condition
        # availability
        # @AttributeType Availability
        # @AttributeMultiplicity 0..*
        # @AttributeMutability mutable
        self.ocni_clonecomputelink_availability = ocni_clonecomputelink_availability

        # Current state of the instance
        # state
        # @AttributeType Enum {active, inactive}
        # @AttributeMultiplicity 1
        # @AttributeMutability immutable
        self.ocni_clonecomputelink_state = ocni_clonecomputelink_state or self._CloNeComputeLink_state.inactive


class CloNeStorageLink(Link):
    """

    Connects a CloNeNode instance to a Storage instance

    """
    # Enumeration for current state of the instance
    _CloNeStorageLink_state = Enum('active', 'inactive')

    # The kind instance assigned to the CloNeStorageLink type
    _kind = Kind(term='CloNeStorageLink',
                 scheme='http://schemas.ogf.org/occi/ocni',
                 entity_type=Link,
                 title='CloNe Storage link',
                 attributes=(
                     Attribute(name='ocni.clonestoragelink.availability', type='pyocni.specification.ocni.Availability',
                               multiplicity='0.*', mutable=True),
                     Attribute(name='ocni.clonestoragelink.state', required=True)),
                 actions=(),
                 related=(Link._kind, ),
                 entities=())

    def __init__(self, occi_core_id, occi_core_source, occi_core_target, ocni_clonestoragelink_state, kind=_kind,
                 occi_core_title='', mixins=[], ocni_clonestoragelink_availability=(Availability(),)):
        super(CloNeStorageLink, self).__init__(occi_core_id=occi_core_id,
                                               kind=kind,
                                               occi_core_source=occi_core_source,
                                               occi_core_target=occi_core_target,
                                               occi_core_title=occi_core_title,
                                               mixins=mixins)

        # The proportion of time this entity is in a functioning condition
        # availability
        # @AttributeType Availability
        # @AttributeMultiplicity 0..*
        # @AttributeMutability mutable
        self.ocni_clonestoragelink_availability = ocni_clonestoragelink_availability

        # Current state of the instance
        # state
        # @AttributeType Enum {active, inactive}
        # @AttributeMultiplicity 1
        # @AttributeMutability immutable
        self.ocni_clonestoragelink_state = ocni_clonestoragelink_state or self._CloNeStorageLink_state.inactive


class CloNeNetworkInterface(Link):
    """

    Connects a CloNeNode instance to a CloNeLink instance

    """

    # Enumeration for current state of the instance
    _CloNeNetworkInterface_state = Enum('active', 'inactive')

    # The kind instance assigned to the CloNeNetworkInterface type
    _kind = Kind(term='CloNeNetworkInterface',
                 scheme='http://schemas.ogf.org/occi/ocni',
                 entity_type=Link,
                 title='CloNe Network Interface link',
                 attributes=(Attribute(name='ocni.clonenetworkinterface.availability',
                                       multiplicity='0.*', type='pyocni.specification.ocni.Availability', mutable=True),
                             Attribute(name='ocni.clonenetworkinterface.state', required=True)),
                 actions=(),
                 related=(Link._kind, ),
                 entities=())

    def __init__(self, occi_core_id, occi_core_source, occi_core_target, ocni_clonenetworkinterface_state, kind=_kind,
                 occi_core_title='', mixins=[], ocni_clonenetworkinterface_availability=(Availability(),)):
        super(CloNeNetworkInterface, self).__init__(occi_core_id=occi_core_id,
                                                    kind=kind,
                                                    occi_core_source=occi_core_source,
                                                    occi_core_target=occi_core_target,
                                                    occi_core_title=occi_core_title,
                                                    mixins=mixins)

        # The proportion of time this entity is in a functioning condition
        # availability
        # @AttributeType Availability
        # @AttributeMultiplicity 0..*
        # @AttributeMutability mutable
        self.ocni_clonenetworkinterface_availability = ocni_clonenetworkinterface_availability

        # Current state of the instance
        # state
        # @AttributeType Enum {active, inactive}
        # @AttributeMultiplicity 1
        # @AttributeMutability immutable
        self.ocni_clonenetworkinterface_state = ocni_clonenetworkinterface_state or self._CloNeNetworkInterface_state.inactive


class FNSInterface(Link):
    """

    Connects a FlashNetworkSlice instance to a Resource instance

    """

    # Enumeration for current state of the instance
    _FNSInterface_state = Enum('active', 'inactive')

    # The kind instance assigned to the FNSInterface type
    _kind = Kind(term='FNSInterface',
                 scheme='http://schemas.ogf.org/occi/ocni',
                 entity_type=Link,
                 title='FNS Interface link',
                 attributes=(
                     Attribute(name='ocni.fnsinterface.availability', type='pyocni.specification.ocni.Availability',
                               multiplicity='0.*', mutable=True),
                     Attribute(name='ocni.fnsinterface.state', required=True)),
                 actions=(),
                 related=(Link._kind, ),
                 entities=())

    def __init__(self, occi_core_id, occi_core_source, occi_core_target, ocni_fnsinterface_state, kind=_kind,
                 occi_core_title='', mixins=[], ocni_fnsinterface_availability=(Availability(),)):
        super(FNSInterface, self).__init__(occi_core_id=occi_core_id,
                                           kind=kind,
                                           occi_core_source=occi_core_source,
                                           occi_core_target=occi_core_target,
                                           occi_core_title=occi_core_title,
                                           mixins=mixins)

        # The proportion of time this entity is in a functioning condition
        # availability
        # @AttributeType Availability
        # @AttributeMultiplicity 0..*
        # @AttributeMutability mutable
        self.ocni_fnsinterface_availability = ocni_fnsinterface_availability

        # Current state of the instance
        # state
        # @AttributeType Enum {active, inactive}
        # @AttributeMultiplicity 1
        # @AttributeMutability immutable
        self.ocni_fnsinterface_state = ocni_fnsinterface_state or self._FNSInterface_state.inactive


class Ethernet(Mixin):
    """

    Ethernet Mixin

    """

    def __init__(self, ocni_ethernet_mac_address=''):
        super(Ethernet, self).__init__(term='Ethernet',
                                       scheme='http://schemas.ogf.org/occi/ocni',
                                       title='Ethernet mixin',
                                       attributes=(Attribute(name='ocni.ethernet.mac_address', mutable=True), ),
                                       actions=(),
                                       related=(),
                                       entities=[])

        # The unique identifier assigned to instance's network interface
        # mac_address
        # @AttributeType MAC-address
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.ocni_ethernet_mac_address = ocni_ethernet_mac_address


class IPv4(Mixin):
    """

    IPv4 Mixin

    """

    # Enumeration for the address allocation mechanism
    _IPv4_allocation = Enum('dynamic', 'static')

    # Enumeration for the IP visibility
    _IPv4_visibility = Enum('public', 'private')

    def __init__(self, ocni_ipv4_ip_address='', ocni_ipv4_netmask='', ocni_ipv4_gateway='', ocni_ipv4_allocation='',
                 ocni_ipv4_visibility=''):
        super(IPv4, self).__init__(term='IPv4',
                                   scheme='http://schemas.ogf.org/occi/ocni',
                                   title='Ethernet mixin',
                                   attributes=(Attribute(name='ocni.ipv4.ip_address', mutable=True),
                                               Attribute(name='ocni.ipv4.netmask', mutable=True),
                                               Attribute(name='ocni.ipv4.gateway', mutable=True),
                                               Attribute(name='ocni.ipv4.allocation', mutable=True),
                                               Attribute(name='ocni.ipv4.visibility', mutable=True)),
                                   actions=(),
                                   related=(),
                                   entities=[])

        # The Internet Protocol (IP) of the instance
        # ip_address
        # @AttributeType IPv4 address, CIDR notation
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.ocni_ipv4_ip_address = ocni_ipv4_ip_address

        # The network mask of the instance
        # netmask
        # @AttributeType IPv4 address, CIDR notation
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.ocni_ipv4_netmask = ocni_ipv4_netmask

        # The gateway of the instance
        # gateway
        # @AttributeType IPv4 address, CIDR notation
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.ocni_ipv4_gateway = ocni_ipv4_gateway

        # The address allocation mechanism of the instance
        # allocation
        # @AttributeType Enum {dynamic, static}
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.ocni_ipv4_allocation = ocni_ipv4_allocation

        # The visibility of the instance
        # visibility
        # @AttributeType Enum {public, private}
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.ocni_ipv4_visibility = ocni_ipv4_visibility


class OpenFlowCloNeNode(Mixin):
    """

    OpenFlow Mixin that can be applied on CloNeNode

    """

    def __init__(self, ocni_openflowclonenode_datapath_id='', ocni_openflowclonenode_ports=('',),
                 ocni_openflowclonenode_of_controller=('',), ocni_openflowclonenode_of_controller_port=''):
        super(OpenFlowCloNeNode, self).__init__(term='OpenFlowCloNeNode',
                                                scheme='http://schemas.ogf.org/occi/ocni',
                                                title='OpenFlow CloNeNode mixin',
                                                attributes=(Attribute(name='ocni.openflowclonenode.datapath_id'),
                                                            Attribute(name='ocni.openflowclonenode.ports',
                                                                      multiplicity='0.*', mutable=True),
                                                            Attribute(name='ocni.openflowclonenode.of_controller',
                                                                      multiplicity='0.*', mutable=True),
                                                            Attribute(name='ocni.openflowclonenode.of_controller_port',
                                                                      mutable=True)),
                                                actions=(),
                                                related=(),
                                                entities=[])

        # OpenFlow switch identifier
        # datapath_id
        # @AttributeType String
        # @AttributeMultiplicity 0..1
        # @AttributeMutability immutable
        self.ocni_openflowclonenode_datapath_id = ocni_openflowclonenode_datapath_id

        # List of ports included in the OpenFlow datapath
        # ports
        # @AttributeType Integer
        # @AttributeMultiplicity 0..*
        # @AttributeMutability mutable
        self.ocni_openflowclonenode_ports = ocni_openflowclonenode_ports

        # The address of the OpenFlow Controller
        # of_controller
        # @AttributeType IPv4 address
        # @AttributeMultiplicity 0..*
        # @AttributeMutability mutable
        self.ocni_openflowclonenode_of_controller = ocni_openflowclonenode_of_controller

        # The port number of the OpenFlow Controller
        # of_controller_port
        # @AttributeType Integer
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.ocni_openflowclonenode_of_controller_port = ocni_openflowclonenode_of_controller_port


class OpenFlowCloNeLink(Mixin):
    """

    OpenFlow Mixin that can be applied on CloNeLink

    """

    def __init__(self, ocni_openflowclonelink_Ether_src='', ocni_openflowclonelink_Ether_dst='',
                 ocni_openflowclonelink_IPv4_src='',
                 ocni_openflowclonelink_IPv4_dst='', ocni_openflowclonelink_IPv4_proto='',
                 ocni_openflowclonelink_VLAN_id='', ocni_openflowclonelink_src_port='',
                 ocni_openflowclonelink_dst_port=''):
        super(OpenFlowCloNeLink, self).__init__(term='OpenFlowCloNeLink',
                                                scheme='http://schemas.ogf.org/occi/ocni',
                                                title='OpenFlow CloNeLink mixin',
                                                attributes=(
                                                    Attribute(name='ocni.openflowclonelink.Ether_src', mutable=True),
                                                    Attribute(name='ocni.openflowclonelink.Ether_dst', mutable=True),
                                                    Attribute(name='ocni.openflowclonelink.IPv4_src', mutable=True),
                                                    Attribute(name='ocni.openflowclonelink.IPv4_dst', mutable=True),
                                                    Attribute(name='ocni.openflowclonelink.IPv4_proto', mutable=True),
                                                    Attribute(name='ocni.openflowclonelink.VLAN_id', mutable=True),
                                                    Attribute(name='ocni.openflowclonelink.src_port', mutable=True),
                                                    Attribute(name='ocni.openflowclonelink.dst_port', mutable=True)),
                                                actions=(),
                                                related=(),
                                                entities=[])

        # Ethernet source address
        # Ether_src
        # @AttributeType MAC address
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.ocni_openflowclonelink_Ether_src = ocni_openflowclonelink_Ether_src

        # Ethernet destination address
        # Ether_dst
        # @AttributeType MAC address
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.ocni_openflowclonelink_Ether_dst = ocni_openflowclonelink_Ether_dst

        # IPv4 source address (Can be subnet mask or arbitrary bitmask)
        # Ether_src
        # @AttributeType IPv4 address
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.ocni_openflowclonelink_IPv4_src = ocni_openflowclonelink_IPv4_src

        # IPv4 destination address (Can be subnet mask or arbitrary bitmask)
        # IPv4_dst
        # @AttributeType IPv4 address
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.ocni_openflowclonelink_IPv4_dst = ocni_openflowclonelink_IPv4_dst

        # IPv4 protocol
        # IPv4_proto
        # @AttributeType Integer
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.ocni_openflowclonelink_IPv4_proto = ocni_openflowclonelink_IPv4_proto

        # VLAN identifier
        # VLAN_id
        # @AttributeType Integer
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.ocni_openflowclonelink_VLAN_id = ocni_openflowclonelink_VLAN_id

        # Transport source port (TCP/UDP/SCTP/ICMP)
        # src_port
        # @AttributeType Integer
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.ocni_openflowclonelink_src_port = ocni_openflowclonelink_src_port

        # Transport destination port (TCP/UDP/SCTP/ICMP)
        # dst_port
        # @AttributeType Integer
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.ocni_openflowclonelink_dst_port = ocni_openflowclonelink_dst_port


class OpenFlowCloNeNetworkInterface(Mixin):
    """

    OpenFlow Mixin that can be applied on CloNeNetworkInterface.
    This mixin is used when the configuration of the OpenFlow switches is done manually

    """

    def __init__(self, ocni_openflowclonenetworkinterface_datapath_id='',
                 ocni_openflowclonenetworkinterface_ports=('',)):
        super(OpenFlowCloNeNetworkInterface, self).__init__(term='OpenFlowCloNeNetworkInterface',
                                                            scheme='http://schemas.ogf.org/occi/ocni',
                                                            title='OpenFlow CloNe Network Interface mixin',
                                                            attributes=(Attribute(
                                                                name='ocni.openflowclonenetworkinterface.datapath_id',
                                                                multiplicity='0.*', mutable=True),
                                                                        Attribute(
                                                                            name='ocni.openflowclonenetworkinterface.ports',
                                                                            multiplicity='0.*', mutable=True)),
                                                            actions=(),
                                                            related=(),
                                                            entities=[])

        # List of OpenFlow switchs to configure
        # datapath_id
        # @AttributeType String
        # @AttributeMultiplicity 0..*
        # @AttributeMutability immutable
        self.ocni_openflowclonenetworkinterface_datapath_id = ocni_openflowclonenetworkinterface_datapath_id

        # The configured switch ports
        # ports
        # @AttributeType Integer
        # @AttributeMultiplicity 0..*
        # @AttributeMutability mutable
        self.ocni_openflowclonenetworkinterface_ports = ocni_openflowclonenetworkinterface_ports


class l3vpn_service_type(object):
    """

    A type that is used by L3VPN Mixin

    """

    def __init__(self, ocni_l3vpn_service_type_type='', ocni_l3vpn_service_type_layer='',
                 ocni_l3vpn_service_type_class_of_service=''):
        self.ocni_l3vpn_service_type_type = ocni_l3vpn_service_type_type
        self.ocni_l3vpn_service_type_layer = ocni_l3vpn_service_type_layer
        self.ocni_l3vpn_service_type_class_of_service = ocni_l3vpn_service_type_class_of_service

    pass


class l3vpn_service_description(object):
    """

    A type that is used by L3VPN Mixin

    """

    def __init__(self, ocni_l3vpn_service_description_endpoint_id='', ocni_l3vpn_service_description_in_bandwidth='',
                 ocni_l3vpn_service_description_out_bandwidth='',
                 ocni_l3vpn_service_description_max_in_bandwidth='',
                 ocni_l3vpn_service_description_max_out_bandwidth='',
                 ocni_l3vpn_service_description_latency='',
                 ocni_l3vpn_service_description_max_latency=''):
        self.ocni_l3vpn_service_description_endpoint_id = ocni_l3vpn_service_description_endpoint_id
        self.ocni_l3vpn_service_description_in_bandwidth = ocni_l3vpn_service_description_in_bandwidth
        self.ocni_l3vpn_service_description_out_bandwidth = ocni_l3vpn_service_description_out_bandwidth
        self.ocni_l3vpn_service_description_max_in_bandwidth = ocni_l3vpn_service_description_max_in_bandwidth
        self.ocni_l3vpn_service_description_max_out_bandwidth = ocni_l3vpn_service_description_max_out_bandwidth
        self.ocni_l3vpn_service_description_latency = ocni_l3vpn_service_description_latency
        self.ocni_l3vpn_service_description_max_latency = ocni_l3vpn_service_description_max_latency


class l3vpn_elastisity(object):
    """

    A type that is used by L3VPN Mixin

    """

    def __init__(self, ocni_l3vpn_elastisity_supported='', ocni_l3vpn_elastisity_reconfiguration_time=''):
        self.ocni_l3vpn_elastisity_supported = ocni_l3vpn_elastisity_supported
        self.ocni_l3vpn_elastisity_reconfiguration_time = ocni_l3vpn_elastisity_reconfiguration_time


class l3vpn_scalability(object):
    """

    A type that is used by L3VPN Mixin

    """

    def __init__(self, ocni_l3vpn_scalability_supported='', ocni_l3vpn_scalability_setup_time=''):
        self.ocni_l3vpn_scalability_supported = ocni_l3vpn_scalability_supported
        self.ocni_l3vpn_scalability_setup_time = ocni_l3vpn_scalability_setup_time


class l3vpn(Mixin):
    """

    A Layer 3 VPN Mixin

    """

    def __init__(self, ocni_l3vpn_infrastructure_request_id='', ocni_l3vpn_customer_id='',
                 ocni_l3vpn_service_type=l3vpn_service_type(),
                 ocni_l3vpn_service_description=(l3vpn_service_description(),), ocni_l3vpn_elastisity=l3vpn_elastisity(),
                 ocni_l3vpn_scalability=l3vpn_scalability()):
        super(l3vpn, self).__init__(term='L3VPN',
                                    scheme='http://schemas.ogf.org/occi/ocni',
                                    title='Layer 3 VPN mixin',
                                    attributes=(Attribute(name='ocni.l3vpn.infrastructure_request_id', mutable=True),
                                                Attribute(name='ocni.l3vpn.customer_id', mutable=True),
                                                Attribute(name='ocni.l3vpn.service_type',
                                                          type='pyocni.specification.ocni.l3vpn_service_type',
                                                          mutable=True),
                                                Attribute(name='ocni.l3vpn.service_description',
                                                          type='pyocni.specification.ocni.l3vpn_service_description',
                                                          multiplicity='0.*', mutable=True),
                                                Attribute(name='ocni.l3vpn.elastisity',
                                                          type='pyocni.specification.ocni.l3vpn_elastisity',
                                                          mutable=True),
                                                Attribute(name='ocni.l3vpn.scalability',
                                                          type='pyocni.specification.ocni.l3vpn_scalability',
                                                          mutable=True)),
                                    actions=(),
                                    related=(),
                                    entities=[])

        # ... infrastructure_request_id
        # infrastructure_request_id
        # @AttributeType String
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.ocni_l3vpn_infrastructure_request_id = ocni_l3vpn_infrastructure_request_id

        # ... customer_id
        # customer_id
        # @AttributeType String
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.ocni_l3vpn_customer_id = ocni_l3vpn_customer_id

        # ... service_type
        # service_type
        # @AttributeType L3VPN_service_type
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.ocni_l3vpn_service_type = ocni_l3vpn_service_type

        # ... service_description
        # service_description
        # @AttributeType L3VPN_service_description
        # @AttributeMultiplicity 0..*
        # @AttributeMutability mutable
        self.ocni_l3vpn_service_description = ocni_l3vpn_service_description

        # ... elastisity
        # elastisity
        # @AttributeType L3VPN_elastisity
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.ocni_l3vpn_elastisity = ocni_l3vpn_elastisity

        # ... scalability
        # scalability
        # @AttributeType L3VPN_scalability
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.ocni_l3vpn_scalability = ocni_l3vpn_scalability
        
class libnetvirt_endpoint(object):
    """

    A type that is used by libnetvirt Mixin

    """

    def __init__(self, ocni_libnetvirt_endpoint_uuid='', ocni_libnetvirt_endpoint_swid='',
                ocni_libnetvirt_endpoint_port='',  ocni_libnetvirt_endpoint_vlan='', 
                ocni_libnetvirt_endpoint_mpls='',):
        self.ocni_libnetvirt_endpoint_uuid = ocni_libnetvirt_endpoint_uuid
        self.ocni_libnetvirt_endpoint_swid = ocni_libnetvirt_endpoint_swid
        self.ocni_libnetvirt_endpoint_port = ocni_libnetvirt_endpoint_port
        self.ocni_libnetvirt_endpoint_vlan = ocni_libnetvirt_endpoint_vlan
        self.ocni_libnetvirt_endpoint_mpls = ocni_libnetvirt_endpoint_mpls
           
    def __repr__(self, *args, **kwargs):
        return repr([self.ocni_libnetvirt_endpoint_uuid, 
                    self.ocni_libnetvirt_endpoint_swid, 
                    self.ocni_libnetvirt_endpoint_port]) 
        
    def __hash__(self, *args, **kwargs):
        return long(self.ocni_libnetvirt_endpoint_uuid)
    
    def __eq__(self, other) :
        return self.ocni_libnetvirt_endpoint_uuid == other.ocni_libnetvirt_endpoint_uuid

class libnetvirt_constraint(object):
    """

    A type that is used by libnetvirt Mixin

    """

    def __init__(self, ocni_libnetvirt_constraint_src='', ocni_libnetvirt_constraint_dst='',
                ocni_libnetvirt_constraint_min_bandwidth='',  ocni_libnetvirt_constraint_max_bandwidth=''):
        self.ocni_libnetvirt_constraint_src = ocni_libnetvirt_constraint_src
        self.ocni_libnetvirt_constraint_dst = ocni_libnetvirt_constraint_src
        self.ocni_libnetvirt_constraint_min_bandwidth = ocni_libnetvirt_constraint_min_bandwidth
        self.ocni_libnetvirt_constraint_max_bandwidth = ocni_libnetvirt_constraint_max_bandwidth

           
    def __repr__(self, *args, **kwargs):
        return repr([self.ocni_libnetvirt_constraint_src, 
                    self.ocni_libnetvirt_constraint_dst, 
                    self.ocni_libnetvirt_constraint_min_bandwidth,
                    self.ocni_libnetvirt_constraint_max_bandwidth
                    ]) 
    
    
 
class libnetvirt(Mixin):
    """

    Libnetvirt Mixin

    """

    def __init__(self, ocni_libnetvirt_uuid='',
                 ocni_libnetvirt_of_controller='127.0.0.1',
                 ocni_libnetvirt_of_controller_port='2000',
                 ocni_libnetvirt_endpoint=(libnetvirt_endpoint(),),
                 ocni_libnetvirt_constraint=(libnetvirt_constraint(),)):
        super(libnetvirt, self).__init__(term='libnetvirt',
                                    scheme='http://schemas.ogf.org/occi/ocni',
                                    title='Libnetvirt mixin',
                                    attributes=(Attribute(name='ocni.libnetvirt.uuid', mutable=True, required=True),
                                                Attribute(name='ocni.libnetvirt.of_controller', mutable=True, multiplicity='0..1', required=False),
                                                Attribute(name='ocni.libnetvirt.of_controller_port', mutable=True, multiplicity='0..1', required=False),
                                                Attribute(name='ocni.libnetvirt.endpoint',
                                                          multiplicity='1..*',
                                                          type='pyocni.specification.ocni.libnetvirt_endpoint',
                                                          mutable=True),
                                                Attribute(name='ocni.libnetvirt.constraint',
                                                          multiplicity='*',
                                                          type='pyocni.specification.ocni.libnetvirt_constraint',
                                                          required=False,
                                                          mutable=True)
                                                ),
                                    actions=(),
                                    related=(),
                                    entities=[])

        # ... uuid
        # ocni_libnetvirt_uuid
        # @AttributeType Integer
        # @AttributeMultiplicity 1
        # @AttributeMutability mutable
        self.ocni_libnetvirt_uuid = ocni_libnetvirt_uuid

        # ... of_controller
        # ocni_libnetvirt_of_controller
        # @AttributeType String
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.ocni_libnetvirt_of_controller = ocni_libnetvirt_of_controller

        # ... of_controller_port
        # of_controller_port
        # @AttributeType Integer
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.ocni_libnetvirt_of_controller_port = ocni_libnetvirt_of_controller_port

        # ... endpoint
        # endpoint
        # @AttributeType endpoint_description
        # @AttributeMultiplicity 0..*
        # @AttributeMutability mutable
        self.ocni_libnetvirt_endpoint = ocni_libnetvirt_endpoint
        
        self.ocni_libnetvirt_constraint = ocni_libnetvirt_constraint



if __name__ == '__main__':
    #a = Availability(datetime(year=2011, month=11, day=1, hour=14, minute=40, second=0),datetime(year=2011, month=11, day=1, hour=14, minute=40, second=0))
    #a = Availability()
    #print a.start
    #print a.end
    pass
