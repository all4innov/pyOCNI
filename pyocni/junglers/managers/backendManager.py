#  Copyright 2010-2012 Institut Mines-Telecom
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""
Created on Jun 12, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@license: Apache License, Version 2.0
"""

try:
    import simplejson as json
except ImportError:
    import json

import imp

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


def choose_appropriate_provider(provider):

    """
    Retrieves the provider of the resource to use its backend

        @param provider: provider name
    """
    backend = None
    backends_json_data = open(config.BACKENDS_FILE)
    backends_list = json.load(backends_json_data)
    backends_json_data.close()

    for i in backends_list["backends"]:
        if i["name"] == provider:

            backend_instance = imp.load_source('', i["path"])
            backend = backend_instance.backend()

    return backend

def get_provider_of_a_kind(kind):

    """
    Get the provider name
    @param kind: OCCI_ID of the kind
    """
    database = config.prepare_PyOCNI_db()

    provider = None

    #Step[1]: Extract the kind description
    try:
        query = database.view('/db_views/my_providers', key=kind)

    except Exception as e:
        logger.error("===== Get_provider_of_a_kind : =====" + e.message)
        return provider

    if query.count() is 0:
        logger.error("===== Get_provider_of_a_kind : No such kind =====")
        return provider

    #Step[2]: return the provider name
    else:
        provider = query.first()['value']

    return provider['local'][0]

#======================================================================================================================
#                                               Actions on single entities
#======================================================================================================================

def delete_entity(entity,kind):
    """
    Dispatches the delete request to the backend
    @param entity: resource to be deleted
    @param kind: OCCI ID of the resource's kind
    """

    #Step[1]: retrieve the provider name
    provider = get_provider_of_a_kind(kind)
    #Step[2]: Dynamically load the backend
    backend = choose_appropriate_provider(provider)
    #Step[3]: Perform the delete method
    backend.delete(entity)


def create_entity(entity):
    """
    Dispatches the create request to the appropriate backend
    @param entity: OCCI description of the entity
    """
    #Step[1]: get the provider
    kind = entity['OCCI_Description']['kind']
    provider = get_provider_of_a_kind(kind)
    #Step[2]: load the backend
    backend = choose_appropriate_provider(provider)
    #Step[3]: perform the create method
    backend.create(entity['OCCI_Description'])


def update_entity(old_data, new_data):
    """
    Dispatches the update request to the appropriate backend
    @param old_data: old OCCI description
    @param new_data: new OCCI description
    """
    #Step[1]: get the provider name
    kind = old_data['kind']
    provider = get_provider_of_a_kind(kind)
    #Step[2]: load the backend
    backend = choose_appropriate_provider(provider)
    #Step[3]: perform the update method
    backend.update(old_data,new_data)


def read_entity(entity,kind):
    """
    Dispatches the read request to the appropriate provider
    @param entity: OCCI description
    @param kind: resource kind
    """

    #Step[1]: get the provider name
    provider = get_provider_of_a_kind(kind)
    #Step[2]: load the backend
    backend = choose_appropriate_provider(provider)
    #Step[3]: perform the read method
    backend.read(entity)


def trigger_action_on_a_resource(path_url, action, provider,attributes):
    """
    Dispatches an action triggering request to the appropriate provider backend
     Args:
        @param path_url: Resource URL Path
        @param action: Action description
        @param provider: Provider of the resource
        @param attributes: Attributes sent with the request
    """
    #Step[1]: Retrieve the appropriate provider backend
    backend = choose_appropriate_provider(provider)
    if backend is not None:
        #Step[2]: Call the action methods of the backend with the action name and attributes
        backend.action(path_url,action,attributes)
        return "", return_code['Accepted']
    else:
        logger.error("trigger action_on_resource : Unknown provider")
        return " An error has occurred, please check logs for more details", return_code['Not Found']

#======================================================================================================================
#                                               Actions on multiple entities
#======================================================================================================================

#Note: This is basically a multiple "call on a single resource"

def create_entities(entities):
    """
    perform create entity method on a list of entities
    @param entities: list of entities
    """

    for i in range(len(entities)):
        create_entity(entities[i])


def update_entities(old_docs, new_docs):
    """
    perform update entities method on a list of entities
    @param old_docs: old entities OCCI description
    @param new_docs: new entities OCCI description
    """

    for i in range(len(old_docs)):
        update_entity(old_docs[i],new_docs[i])


def read_entities(entities):
    """
    perform read entity method on a list of entities
    @param entities: list of entities
    """
    for i in range(len(entities)):
        read_entity(entities[i],entities[i]['kind'])


def trigger_action_on_multi_resource(data):
    """
    Trigger the action on multiple resource
    Args:
        @param data: Data provided for triggering the action
    """
    for item in data:
        trigger_action_on_a_resource(item['resource_url'],item['action'],item['provider'][0])
    return "",return_code['OK']


if __name__ == "__main__":
    choose_appropriate_provider("dummy_backend")