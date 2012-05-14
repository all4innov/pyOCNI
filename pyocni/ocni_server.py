# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

# Copyright (C) 2011 Houssem Medhioub - Institut Telecom
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
@author: Daniel Turull (DELETE and PUT of OperationResource class)
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Telecom - Telecom SudParis
@version: 0.3
@license: LGPL - Lesser General Public License
"""

import pyocni.pyocni_tools.config as config
from pyocni.pyocni_tools import create_new_class

import  pyocni.serialization.serializer_json as json_serializer
import  pyocni.serialization.serializer_http as http_serializer
import sys
if sys.version_info < (2, 7):
    from pyocni.pyocni_tools.OrderedDict import OrderedDict
else:
    from collections import OrderedDict

import pyocni.pyocni_tools.DoItYourselfWebOb as url_mapper

import eventlet
from eventlet import wsgi

from webob import Request, Response
import uuid
import re

import cStringIO

try:
    import simplejson as json
except ImportError:
    import json

import jsonpickle

import pprint

from  pyocni.specification.occi_core import Category, Kind, Mixin, Action, Entity, Resource, Link
from pyocni.specification.occi_infrastructure import Compute, Network, Storage,\
    NetworkInterface, StorageLink, IPNetworking, IPNetworkInterface

from pyocni.specification.ocni import CloNeNode, CloNeLink, FNS, CloNeComputeLink, CloNeStorageLink, CloNeNetworkInterface,\
    FNSInterface, Ethernet, IPv4, OpenFlowCloNeNode, OpenFlowCloNeLink, OpenFlowCloNeNetworkInterface, l3vpn, libnetvirt 

from pyocni.registry.registry import category_registry, location_registry, backend_registry, serialization_registry



from pyocni.backend.dummy_backend import dummy_backend
from pyocni.backend.openflow_backend import openflow_backend
from pyocni.backend.l3vpn_backend import l3vpn_backend
from pyocni.backend.opennebula_backend import opennebula_backend
from pyocni.backend.openstack_backend import openstack_backend
from pyocni.backend.libnetvirt_backend import libnetvirt_backend

from pyocni.pyocni_tools import ask_user_details as shell_ask

# getting the Logger
logger = config.logger

# getting IP and Port of the OCCI server
OCNI_IP = config.OCNI_IP
OCNI_PORT = config.OCNI_PORT


# ======================================================================================
# HTTP Return Codes
# ======================================================================================
return_code = {'OK': 200,
               'Accepted': 202,
               'Bad Request': 400,
               'Unauthorized': 401,
               'Forbidden': 403,
               'Method Not Allowed': 405,
               'Conflict': 409,
               'Gone': 410,
               'Unsupported Media Type': 415,
               'Internal Server Error': 500,
               'Not Implemented': 501,
               'Service Unavailable': 503}

# ======================================================================================
# Reinialization of the locations registry and objects registry (clear ZODB)
# ======================================================================================
result = shell_ask.query_yes_no_quit(" \n_______________________________________________________________\n"
                                     "   Do you want to purge 'locations' and 'objects' Databases (DB  reinialization)?", "no")
if result == 'yes':
    location_registry().purge_locations_db()
    location_registry().purge_objects_db()


# ======================================================================================
# the category registry
# ======================================================================================

#category_registry = category_registry()

# register OCCI Core kinds
#category_registry().register_kind(Entity._kind)
#category_registry().register_kind(Resource._kind)
#category_registry().register_kind(Link._kind)

# register OCCI Infrastructure kinds
category_registry().register_kind(Compute._kind)
category_registry().register_kind(Network._kind)
category_registry().register_kind(Storage._kind)
category_registry().register_kind(NetworkInterface._kind)
category_registry().register_kind(StorageLink._kind)

# register OCCI Infrastructure mixins
category_registry().register_mixin(IPNetworking())
category_registry().register_mixin(IPNetworkInterface())

# register OCNI kinds
category_registry().register_kind(CloNeNode._kind)
category_registry().register_kind(CloNeLink._kind)
category_registry().register_kind(FNS._kind)
category_registry().register_kind(CloNeComputeLink._kind)
category_registry().register_kind(CloNeStorageLink._kind)
category_registry().register_kind(CloNeNetworkInterface._kind)
category_registry().register_kind(FNSInterface._kind)

# register OCNI mixins
category_registry().register_mixin(Ethernet())
category_registry().register_mixin(IPv4())
category_registry().register_mixin(OpenFlowCloNeNode())
category_registry().register_mixin(OpenFlowCloNeLink())
category_registry().register_mixin(OpenFlowCloNeNetworkInterface())
category_registry().register_mixin(l3vpn())
category_registry().register_mixin(libnetvirt())

# ======================================================================================
# the location registry
# ======================================================================================

#location_registry = location_registry()

# register OCCI Core kind locations
#location_registry().register_location("/resource/", Resource._kind)
#location_registry().register_location("/link/", Link._kind)

# register OCCI Infrastructure kind locations
location_registry().register_location("/compute/", Compute._kind)
location_registry().register_location("/network/", Network._kind)
location_registry().register_location("/storage/", Storage._kind)
location_registry().register_location("/networkinterface/", NetworkInterface._kind)
location_registry().register_location("/storagelink/", StorageLink._kind)

# register OCCI Infrastructure mixin locations
location_registry().register_location("/ipnetworking/", IPNetworking())
location_registry().register_location("/ipnetworkinterface/", IPNetworkInterface())

# register OCNI kind locations
location_registry().register_location("/CloNeNode/", CloNeNode._kind)
location_registry().register_location("/CloNeLink/", CloNeLink._kind)
location_registry().register_location("/FNS/", FNS._kind)
location_registry().register_location("/CloNeComputeLink/", CloNeComputeLink._kind)
location_registry().register_location("/CloNeStorageLink/", CloNeStorageLink._kind)
location_registry().register_location("/CloNeNetworkInterface/", CloNeNetworkInterface._kind)
location_registry().register_location("/FNSInterface/", FNSInterface._kind)

# register OCNI mixin locations
location_registry().register_location("/Ethernet/", Ethernet())
location_registry().register_location("/IPv4/", IPv4())
location_registry().register_location("/OpenFlowCloNeNode/", OpenFlowCloNeNode())
location_registry().register_location("/OpenFlowCloNeLink/", OpenFlowCloNeLink())
location_registry().register_location("/OpenFlowCloNeNetworkInterface/", OpenFlowCloNeNetworkInterface())
location_registry().register_location("/l3vpn/", l3vpn())
location_registry().register_location("/libnetvirt/", libnetvirt())

# ======================================================================================
# the Backend registry
# ======================================================================================

result = shell_ask.query_yes_no_quit(" \n_______________________________________________________________\n"
                                     "   Do you want to register the dummy backend ?", "yes")
if result == 'yes':
    backend_registry().register_backend(dummy_backend())
result = shell_ask.query_yes_no_quit(" \n_______________________________________________________________\n"
                                     "   Do you want to register the OpenFlow backend ?", "no")
if result == 'yes':
    backend_registry().register_backend(openflow_backend())
result = shell_ask.query_yes_no_quit(" \n_______________________________________________________________\n"
                                     "    Do you want to register the L3VPN backend ?", "no")
if result == 'yes':
    backend_registry().register_backend(l3vpn_backend())
result = shell_ask.query_yes_no_quit(" \n_______________________________________________________________\n"
                                     "    Do you want to register the OpenNebula backend ?", "no")
if result == 'yes':
    backend_registry().register_backend(opennebula_backend())
result = shell_ask.query_yes_no_quit(" \n_______________________________________________________________\n"
                                     "    Do you want to register the OpenStack backend ?", "no")
if result == 'yes':
    backend_registry().register_backend(openstack_backend())
result = shell_ask.query_yes_no_quit(" \n_______________________________________________________________\n"
                                     "    Do you want to register the libnetvirt backend ?", "no")
if result == 'yes':
    backend_registry().register_backend(libnetvirt_backend())

class QueryInterface(object):
    """

    Handling the Query Interface

    """

    def __init__(self, req):
        self.req = req
        self.res = Response()
        self.res.content_type = 'application:json:occi'
        self.res.server = 'ocni-server/1.1 (linux) OCNI/1.1'

    def get(self):
        """
        Retrieval of all registered Kinds and Mixins
            Retrieval of a filtered list of Kinds and Mixins
        """
        category_json_serializer = json_serializer.category_serializer()

        _kind_values = list()
        for _kind in category_registry().get_kinds().values():
            _kind_values.append(json.loads(category_json_serializer.to_json(_kind)))

        _mixin_values = list()
        for _mixin in category_registry().get_mixins().values():
            _mixin_values.append(json.loads(category_json_serializer.to_json(_mixin)))

        result_json = _kind_values + _mixin_values

        result_dump = cStringIO.StringIO()
        json.dump(result_json, result_dump, indent=4 * ' ')

        self.res.body = result_dump.getvalue()

        return self.res

    def post(self):
        print self.req
        return 'N/A : No POST verb for a Query Interface'

    def put(self):
        """
        Adding a user defined Mixin

        """
        return 'QueryInterface response from PUT '

    def delete(self):
        """

        Removing a Mixin definition

        """
        return 'QueryInterface response from DELETE'


# ======================================================================================
# Operation on Paths in the Name-space
# ======================================================================================
#
#   Retrieving All resource instances Below a Path (DONE)
#
#   Deletion of all resource instances below a path
class OperationPath(object):
    """

    Operation on Paths in the Name-space

    """

    def __init__(self, req, term='', user=''):
        self.req = req
        self.term = term
        self.user = user
        self.res = Response()
        self.res.content_type = 'application:json:occi'
        self.res.server = 'ocni-server/1.1 (linux) OCNI/1.1'

    def get(self):
        """

        Retrieving All resource instances Below a Path

        """
        _path = '/' + self.term + '/' + self.user + '/'
        res = location_registry().get_locations_under_path(_path)

        self.res.body = jsonpickle.encode(res, unpicklable=False)

        return self.res

    def post(self):
        """

        """
        return self.res

    def put(self):
        """

        """
        return self.res

    def delete(self):
        """

        Deletion of all resource instances below a path

        """
        return self.res


# ======================================================================================
# Operations on Mixins or Kinds
# ======================================================================================
#
#   Retrieving all Resource Instances belonging to Mixin or Kind
#
#   Triggering actions on All Instances of a Mixin or Kind
#
#   Associate resource instances with Mixins
#
#   Unassociated resource instance(s) from a Mixin

# ======================================================================================
# Operations on Resource Instances
# ======================================================================================
#
#   Creating a resource instance (DONE)
#
#   Retrieving a resource instance (DONE)
#
#   Updating a resource instance (DONE)
#
#   Deleting a resource instance (DONE)
#
#   Triggering an Action on a resource instance
class OperationResource(object):
    """

    Handling the Query Interface

    """

    def __init__(self, req, term=None, user=None, id=None):
        self.req = req
        self.user = user
        self.term = term
        self.id = id
        self.res = Response()
        self.res.content_type = 'application:json:occi'
        self.res.server = 'ocni-server/1.1 (linux) OCNI/1.1'

    def get(self):
        """

        Retrieving a resource instance

        """

        resource_json_serializer = json_serializer.resource_serializer()

        _object = location_registry().get_object(self.req.path)

        if _object is not None:
            result_json = json.loads(resource_json_serializer.to_json(_object))

            result_dump = cStringIO.StringIO()
            json.dump(result_json, result_dump, indent=4 * ' ')

            self.res.body = result_dump.getvalue()

            #for _backend in backend_registry().get_backends().values():
            #    _backend.read()
        else:
            #self.res.status = ''
            self.res.body = 'No resource with this PATH'

        return self.res

    def post(self):
        """

        Creating a resource instance

        """

        # =1= getting the resource to create from the json

        resource_json_serializer = json_serializer.resource_serializer()
        _resource = resource_json_serializer.from_json(self.req.body)

        # =2= add the created resource to the registry

        _user_id = 'user1'
        _location = '/' + self.term + '/' + _user_id + '/' + str(_resource.occi_core_id)
        location_registry().register_location(_location, _resource)

        # =3= execute the backend command by sending the resource object
        for _backend in backend_registry().get_backends().values():
            _backend.create(_resource)

        # =4= return OK with the Location of the created resource

        location_result = json.dumps({"location": _location})
        self.res.body = location_result

        return self.res

    def put(self):
        """

        Creating a resource instance by providing the path in the name-space hierarchy (To do)
        Or
        Updating a resource instance (Done)

        """
        # =1= get old resources
        _old_resource = location_registry().get_object(self.req.path)
        # =2= get new resources
        resource_json_serializer = json_serializer.resource_serializer()
        _resource = resource_json_serializer.from_json(self.req.body)

        # =3= unregister old and register new
        location_registry().unregister_location(self.req.path)
        location_registry().register_location(self.req.path, _resource)

        # =4= execute the backend command by sending the resource object
        for _backend in backend_registry().get_backends().values():
            _backend.update(_old_resource, _resource)

        self.res.body = 'Resource ' + self.req.path + ' has been updated'

        return self.res

    def delete(self):
        """

        Deleting a resource instance

        """
        # =1= get resources
        _resource = location_registry().get_object(self.req.path)

        # =2= remove resources
        location_registry().unregister_location(self.req.path)

        # =3= execute the backend command by sending the resource object
        for _backend in backend_registry().get_backends().values():
            _backend.delete(_resource)

        # =4= return OK with the Location of the created resource
        self.res.body = 'Resource with this PATH has been removed'

        return self.res

# ======================================================================================
# Handling Links resource instances
# ======================================================================================
#
#   Creation of a Link during creation of a Resource instance
#
#   Retrieval resource instances of the type Resource with defined Links
#
#   Creation of Link resource instances
#
#   Retrieval of Link resource instances


class ocni_server(object):
    """

    The main ocni REST server

    """

    queryInterface = url_mapper.rest_controller(QueryInterface)
    operationResource = url_mapper.rest_controller(OperationResource)
    operationPath = url_mapper.rest_controller(OperationPath)

    app = url_mapper.Router()
    app.add_route('/-/', controller=queryInterface)
    app.add_route('/{term}/', controller=operationResource)
    app.add_route('/{term}/{user}/{id}', controller=operationResource)
    app.add_route('/{term}/{user}/', controller=operationPath)

    def run_server(self):
        """

        to run the server

        """
        print ("\n______________________________________________________________________________________\n"
               "The OCNI server is running at: ")
        wsgi.server(eventlet.listen((config.OCNI_IP, int(config.OCNI_PORT))), self.app)

        print ("\n______________________________________________________________________________________\n"
               "Closing correctly 'locations' and 'objects' Databases: ")
        location_registry(). close_locations_db()
        location_registry().close_objects_db()

if __name__ == '__main__':
    logger.debug('############ BEGIN OCCI Category rendering ###############')
    c = http_serializer.category_serializer()
    result = c.to_http(Compute._kind)
    logger.debug(result.get('Category'))
    logger.debug('############# END OCCI Category rendering ################')

    logger.debug('############ BEGIN OCCI Link instance rendering ###############')
    network_instance = Network('/network/123', 'active')
    location_registry().register_location("/network/123", network_instance)

    networkinterface_instance = NetworkInterface('456', 'source', '/network/123', '192.168.1.2', '00:00:10:20:30:40',
        'active')
    location_registry().register_location("/link/networkinterface/456", networkinterface_instance)

    l = http_serializer.link_serializer()
    result = l.to_http(NetworkInterface('456', 'source', '/network/123', 'eth0', '00:01:20:50:90:80', 'active'))
    logger.debug(result.get('Link'))
    logger.debug('############# END OCCI Link instance rendering ################')

    logger.debug('############ BEGIN OCCI Action instance rendering ###############')
    compute_instance = Compute('/compute/user1/compute1', 'active', occi_core_title='compute1 created by Houssem')
    location_registry().register_location("/compute/user1/compute1", compute_instance)

    a = http_serializer.action_serializer()
    result = a.to_http(compute_instance, Compute._action_start)
    logger.debug(result.get('Link'))
    logger.debug('############# END OCCI Action instance rendering ################')

    logger.debug('############# Begin OCCI Entity attributes rendering ################')
    att = http_serializer.attributes_serializer()
    result = att.to_http(compute_instance)
    result2 = result.get('X-OCCI-Attribute')
    for r in result2:
        logger.debug('X-OCCI-Attribute' + ': ' + r)
    logger.debug('############# END OCCI Entity attributes rendering ################')

    logger.debug('############# BEGIN OCCI Location-URIs rendering ################')
    location = http_serializer.location_serializer()
    temp = location_registry().locations.values()

    result = location.to_http(temp)
    result2 = result.get('X-OCCI-Location')
    for r in result2:
        logger.debug('X-OCCI-Location' + ': ' + r)
    logger.debug('############# END OCCI Location-URIs rendering ################')

    logger.debug('=======***======= Starting the OCNI server... =======***=======')
    ocni_server_instance = ocni_server()
    ocni_server_instance.run_server()
