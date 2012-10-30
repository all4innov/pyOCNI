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

import pyocni.pyocni_tools.config as config
import pyocni.junglers.managers.backendManager as backend_m
from pyocni.dataBakers.resource_dataBaker import ResourceDataBaker
from postMan.the_post_man import PostMan

from pyocni.pyocni_tools.config import return_code

from pyocni.junglers.managers.linkManager import LinkManager
from pyocni.junglers.managers.resourceManager import ResourceManager

try:
    import simplejson as json
except ImportError:
    import json

# getting the Logger
logger = config.logger


#=======================================================================================================================
#                                           SingleEntityManager
#=======================================================================================================================

class SingleEntityJungler(object):
    """

    """

    def __init__(self):
        self.manager_r = ResourceManager()
        self.manager_l = LinkManager()
        self.rd_baker = ResourceDataBaker()
        self.PostMan = PostMan()

    def channel_put_single_resource(self, jBody, path_url):
        """
        Creates a new resource or performs a full description update of the resource
        Args:
            @param jBody: Data contained in the request body
            @param path_url: URL of the request
        """

        #Step[1]: Get the data necessary from the database

        db_occi_ids_locs, db_resources_nb = self.rd_baker.bake_to_put_single(path_url)

        if db_occi_ids_locs is None or db_resources_nb is None:
            return "An error has occurred, please check log for more details", return_code['Internal Server Error']
        else:
            if db_resources_nb is 0:
                #Step[2a]: This is a create a new resource request

                if jBody.has_key('resources'):
                    logger.debug("===== Channel_put_single_resources ==== : Resource custom creation channeled")
                    entity, resp_code_r = self.manager_r.register_custom_resource(jBody['resources'][0], path_url,
                        db_occi_ids_locs)
                else:
                    resp_code_r = return_code['OK, and location returned']

                if jBody.has_key('links'):
                    logger.debug("===== Channel_put_single_resources ==== : Link custom creation channeled")
                    entity, resp_code_l = self.manager_l.register_custom_link(jBody['links'][0], path_url,
                        db_occi_ids_locs)
                else:
                    resp_code_l = return_code['OK, and location returned']

                if resp_code_r is not return_code['OK, and location returned'] \
                or resp_code_l is not return_code['OK, and location returned']:
                    return "An error has occurred, please check log for more details", return_code['Bad Request']

                self.PostMan.save_custom_resource(entity)
                logger.debug("===== Channel_put_single_resource ==== : Finished (2a) with success")
                backend_m.create_entity(entity)

                #Step[3a]: Return the locations of the resources
                return entity['OCCI_Location'], return_code['OK, and location returned']

            else:
                #Step[2b]: This is an update resource request (More data is needed)

                olddoc = self.rd_baker.bake_to_put_single_updateCase(path_url)
                if olddoc is None:
                    return "An error has occurred, please check log for more details", return_code['Bad Request']
                else:
                    if jBody.has_key('resources'):
                        logger.debug("===== Channel_put_single_resources ==== : Resource full update channeled")
                        entity, resp_code_r = self.manager_r.update_resource(olddoc['OCCI_Description'],
                            jBody['resources'][0], db_occi_ids_locs)
                    else:
                        resp_code_r = return_code['OK, and location returned']

                    if jBody.has_key('links'):
                        logger.debug("===== Channel_put_single_resources ==== : Link full update channeled")
                        entity, resp_code_l = self.manager_l.update_link(olddoc['OCCI_Description'], jBody['links'][0],
                            db_occi_ids_locs)
                    else:
                        resp_code_l = return_code['OK, and location returned']

                    if resp_code_r is not return_code['OK, and location returned'] \
                    or resp_code_l is not return_code['OK, and location returned']:
                        return "An error has occurred, please check log for more details", return_code['Bad Request']

                    olddoc['OCCI_Description'] = entity

                    self.PostMan.save_updated_docs_in_db(olddoc)

                    logger.debug("===== Channel_post_single_resource ==== : Finished (2b) with success")
                    #return the locations of the resources

                    backend_m.update_entity(entity, entity)

                    return olddoc['OCCI_Location'], return_code['OK, and location returned']

    def channel_get_single_resource(self, path_url):
        """
        Retrieve the description of a resource related to the URL provided
        Args:
            @param path_url: URL of the request
        """
        res, entity = self.rd_baker.bake_to_get_single_res(path_url)

        if res is None:
            return "An error has occured, please check logs for more details", return_code['Internal Server Error']

        elif res is 0:
            logger.warning("===== Channel_get_single_resource ==== : Resource not found")

        else:
            logger.debug("===== Channel_get_single_resource ==== : Finished with success")

            #backend_m.read_entity(entity,entity['kind'])

            return res, return_code['OK']

    def channel_post_single_resource(self, jBody, path_url):
        """
        Performs a partial description update of the resource
        Args:
            @param jBody: Data contained in the request body
            @param path_url: URL of the request
        """

        db_occi_ids_locs, old_doc = self.rd_baker.bake_to_post_single(path_url)

        if old_doc is 0:
            logger.error("===== Channel_post_single_resource ==== : Resource not found")
            return "An error has occurred, please check logs for more details", return_code['Internal Server Error']

        else:
            old_data = old_doc['OCCI_Description']
            entity = dict()

            #This is an update of a resource

            if jBody.has_key('resources'):
                logger.debug("===== Channel_post_single_resource ==== : Resource was found and channeled")
                entity, resp_code_r = self.manager_r.partial_resource_update(old_doc['OCCI_Description'],
                    jBody['resources'][0])

            else:
                logger.debug("===== Channel_post_single_resource ==== : No Resource was found")
                resp_code_r = return_code['OK, and location returned']

            if jBody.has_key('links'):
                logger.debug("===== Channel_post_single_resource ==== : Link was found and channeled")
                entity, resp_code_l = self.manager_l.partial_link_update(old_doc['OCCI_Description'], jBody['links'][0],
                    db_occi_ids_locs)
            else:
                logger.debug("===== Channel_post_single_resource ==== : No Link was found")
                resp_code_l = return_code['OK, and location returned']

            if resp_code_r is not return_code['OK, and location returned'] \
            or resp_code_l is not return_code['OK, and location returned']:
                return "An error has occurred, please check log for more details", return_code['Bad Request']

            old_doc['OCCI_Description'] = entity
            self.PostMan.save_updated_docs_in_db(old_doc)
            #            self.PostMan.database.save_doc(old_doc,force_update=True, all_or_nothing=True)
            logger.debug("===== Channel_post_single_resource ==== : Finished with success")
            backend_m.update_entity(old_data, entity)
            #return the locations of the resources
            return old_doc['OCCI_Location'], return_code['OK, and location returned']

    def channel_delete_single_resource(self, path_url):
        """
        Delete a resource instance
        Args:
            @param path_url: URL of the resource
        """
        res, res_value = self.rd_baker.bake_to_delete_single_resource(path_url)

        if res is None:
            return "An error has occured, please check logs for more details", return_code['Internal Server Error']

        elif res is 0:
            logger.warning("===== Channel_delete_single_resource ==== : Resource not found")
        else:
            self.PostMan.delete_single_resource_in_db(res_value)

            #get the kind to get the provider
            entity = res_value['OCCI_Description']

            #send the request to the appropriate provider
            backend_m.delete_entity(entity, entity['kind'])
            logger.debug("===== Channel_delete_single_resource ==== : Finished with success")
            return "", return_code['OK']

    def channel_triggered_action_single(self, jBody, path_url, triggered_action):
        """
        Trigger the action on the resource
        Args:
            @param jBody: Data provided
            @param path_url: URL of the request
            @param triggered_action: Action name to trigger
        """

        nb_res, value_res = self.rd_baker.bake_to_trigger_action_on_single_resource(path_url)
        if nb_res is None:
            return "An error has occurred, please check log for more details", return_code['Internal Server Error']

        elif nb_res is 0:
            return "An error has occurred, please check log for more details", return_code['Not Found']

        else:
            provider = self.rd_baker.bake_to_get_provider(value_res[0])

            if provider is None:
                return "An error has occurred, please check log for more details", return_code['Internal Server Error']

            else:
                resp, resp_code = backend_m.trigger_action_on_a_resource(path_url, jBody['action'][0],
                    provider['local'][0])
                logger.debug("===== Channel_triggered_action_single ==== : Finished with success")
                return resp, return_code['OK']


#=======================================================================================================================
#                                           Independent Functions
#=======================================================================================================================

def associate_entities_to_mixins(mix_ids, db_docs):
    """
    Add a collection of mixins to entities
    Args:
        @param mix_ids: OCCI IDs of mixins
        @param db_docs: documents of the entities already contained in the database
    """

    for doc in db_docs:
        doc['OCCI_Description']['mixins'] = mix_ids
    logger.debug("Associate mixin : Mixin associated with success")
    return db_docs, return_code['OK']





