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
Created on Jun 12, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@version: 0.3
@license: LGPL - Lesser General Public License
"""
from pyocni.backends import dummy_backend,l3vpn_backend,libnetvirt_backend,openflow_backend,opennebula_backend,openstack_backend
import pyocni.pyocni_tools.config as config
try:
    import simplejson as json
except ImportError:
    import json
from pyocni.pyocni_tools.config import return_code
# getting the Logger
logger = config.logger

try:
    import simplejson as json
except ImportError:
    import json


def trigger_action_on_multi_resource(data):
    """
    Trigger the action on multiple resource
    Args:
        @param data: Data provided for triggering the action
    """
    for item in data:
        trigger_action_on_a_resource(item['resource_url'],item['action'],item['provider'][0])
    return "",return_code['OK']

def choose_appropriate_provider(provider):

    backend = None

    if provider == "dummy":
        backend = dummy_backend.dummy_backend()
    elif provider == "l3vpn":
        backend = l3vpn_backend.l3vpn_backend()
    elif provider == "libnetvirt":
        backend = libnetvirt_backend.libnetvirt_backend()
    elif provider == "openflow":
        backend = openflow_backend.openflow_backend()
    elif provider == "opennebula":
        backend = opennebula_backend.opennebula_backend()
    elif provider == "openstack":
        backend = openstack_backend.openstack_backend()

    return backend

def trigger_action_on_a_resource(path_url,action,provider,attributes):
    """
    Send the action triggering request to the appropriate provider
     Args:
        @param path_url: Resource URL Path
        @param action: Action description
        @param provider: Provider of the resource
        @param attributes: Attributes sent with the request
    """
    backend = choose_appropriate_provider(provider)
    if backend is not None:

        backend.action(path_url,action,attributes)
        return "", return_code['Accepted']
    else:
        logger.error("trigger action_on_resource : Unknown provider")
        return " An error has occurred, please check logs for more details", return_code['Not Found']

def get_provider_of_a_kind(kind):

    database = config.prepare_PyOCNI_db()

    provider = None
    try:
        query = database.view('/db_views/my_providers', key=kind)

    except Exception as e:
        logger.error("get_provider_of_a_kind : " + e.message)
        print "----------------------------------------------"
        return provider

    if query.count() is 0:
        logger.error("get_provider_of_a_kind : No such provider")
        return provider
    else:
        provider = query.first()['value']

    return provider['local'][0]



def delete_entity(entity,kind):

    provider = get_provider_of_a_kind(kind)
    backend = choose_appropriate_provider(provider)
    backend.delete(entity)


def create_entity(entity,res_adr):

    kind = entity['OCCI_Description']['kind']
    provider = get_provider_of_a_kind(kind)
    backend = choose_appropriate_provider(provider)
    backend.create(entity['OCCI_Description'],res_adr)


def update_entity(old_data, new_data):

    kind = old_data['kind']
    provider = get_provider_of_a_kind(kind)
    backend = choose_appropriate_provider(provider)
    backend.update(old_data,new_data)


def read_entity(entity,kind):

    provider = get_provider_of_a_kind(kind)
    backend = choose_appropriate_provider(provider)
    backend.read(entity)

def create_entities(entities,res_adrs):

    for i in range(len(entities)):
        create_entity(entities[i],res_adrs[i])


def update_entities(old_docs, new_docs):


    for i in range(len(old_docs)):
        update_entity(old_docs[i],new_docs[i])


def read_entities(entities):

        for i in range(len(entities)):
            read_entity(entities[i],entities[i]['kind'])
