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
Created on Jun 01, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@author: Daniel Turull (DELETE and PUT of OperationResource class)
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Telecom - Telecom SudParis
@version: 1.0
@license: LGPL - Lesser General Public License
"""
from pyocni.crud_Interfaces.categoryInterfaces import KindInterface,MixinInterface,ActionInterface
from pyocni.crud_Interfaces.locationInterfaces import ResourceInterface,LinkInterface
import pyocni.pyocni_tools.config as config
import pyocni.pyocni_tools.DoItYourselfWebOb as url_mapper
import eventlet
from pyocni.registry import categoryManager,locationManager
from eventlet import wsgi
from pyocni.registry.registry import backend_registry, serialization_registry
from pyocni.pyocni_tools import ask_user_details as shell_ask
from pyocni.backend.dummy_backend import dummy_backend
from pyocni.backend.openflow_backend import openflow_backend
from pyocni.backend.l3vpn_backend import l3vpn_backend
from pyocni.backend.opennebula_backend import opennebula_backend
from pyocni.backend.openstack_backend import openstack_backend
from pyocni.backend.libnetvirt_backend import libnetvirt_backend


# getting the Logger
logger = config.logger

# getting IP and Port of the OCCI server
OCNI_IP = config.OCNI_IP
OCNI_PORT = config.OCNI_PORT


# ======================================================================================
# the Backend registry
# ======================================================================================

#result = shell_ask.query_yes_no_quit(" \n_______________________________________________________________\n"
#                                     "   Do you want to register the dummy backend ?", "yes")
#if result == 'yes':
#    backend_registry().register_backend(dummy_backend())
#result = shell_ask.query_yes_no_quit(" \n_______________________________________________________________\n"
#                                     "   Do you want to register the OpenFlow backend ?", "no")
#if result == 'yes':
#    backend_registry().register_backend(openflow_backend())
#result = shell_ask.query_yes_no_quit(" \n_______________________________________________________________\n"
#                                     "    Do you want to register the L3VPN backend ?", "no")
#if result == 'yes':
#    backend_registry().register_backend(l3vpn_backend())
#result = shell_ask.query_yes_no_quit(" \n_______________________________________________________________\n"
#                                     "    Do you want to register the OpenNebula backend ?", "no")
#if result == 'yes':
#    backend_registry().register_backend(opennebula_backend())
#result = shell_ask.query_yes_no_quit(" \n_______________________________________________________________\n"
#                                     "    Do you want to register the OpenStack backend ?", "no")
#if result == 'yes':
#    backend_registry().register_backend(openstack_backend())
#result = shell_ask.query_yes_no_quit(" \n_______________________________________________________________\n"
#                                     "    Do you want to register the libnetvirt backend ?", "no")
#if result == 'yes':
#    backend_registry().register_backend(libnetvirt_backend())


# ======================================================================================
# The OCNI Server
# ======================================================================================


class ocni_server(object):
    """

    The main OCNI REST server

    """

    operationKind = url_mapper.rest_controller(KindInterface)
    operationMixin = url_mapper.rest_controller(MixinInterface)
    operationAction = url_mapper.rest_controller(ActionInterface)
    operationResource = url_mapper.rest_controller(ResourceInterface)
    operationLink = url_mapper.rest_controller(LinkInterface)

    app = url_mapper.Router()

    #===== Kind Routes =====

    app.add_route('/-/kind/',controller=operationKind)
    app.add_route('/-/kind/{user_id}/{doc_id}',controller=operationKind)
    app.add_route('/-/mixin/',controller = operationMixin)
    app.add_route('/-/mixin/{user_id}/{doc_id}',controller=operationMixin)
    app.add_route('/-/action/',controller = operationAction)
    app.add_route('/-/action/{user_id}/{doc_id}',controller=operationAction)
    app.add_route('/-/resource/',controller=operationResource)
    app.add_route('/-/resource/{user_id}/{doc_id}',controller=operationResource)
    app.add_route('/-/link/',controller= operationLink)
    app.add_route('/-/link/{user_id}/{doc_id}',controller=operationLink)

    def run_server(self):
        """

        to run the server

        """
        result = shell_ask.query_yes_no_quit(" \n_______________________________________________________________\n"
                                             "   Do you want to purge all databases (DB  reinitialization)?", "no")
        if result == 'yes':
            locationManager.purgeLocationDBs()
            categoryManager.purgeCategoryDBs()

        print ("\n______________________________________________________________________________________\n"
               "The OCNI server is running at: " + config.OCNI_IP + ":"+config.OCNI_PORT)
        wsgi.server(eventlet.listen((config.OCNI_IP, int(config.OCNI_PORT))), self.app)

        print ("\n______________________________________________________________________________________\n"
               "Closing correctly 'locations' and 'objects' Databases: ")



if __name__ == '__main__':

    ocni_server_instance = ocni_server()
    ocni_server_instance.run_server()

