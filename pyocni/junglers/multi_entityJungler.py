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
Created on May 29, 2012

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
from pyocni.junglers.pathJungler import PathManager
from pyocni.junglers.managers.linkManager import LinkManager
from pyocni.junglers.managers.resourceManager import ResourceManager

try:
    import simplejson as json
except ImportError:
    import json

# getting the Logger
logger = config.logger

#=======================================================================================================================
#                                           MultiEntityManager
#=======================================================================================================================

class MultiEntityJungler(object):
    """
    Handles requests concerning multiple entities

    """

    def __init__(self):

        self.manager_r = ResourceManager()
        self.manager_l = LinkManager()
        self.jungler_p = PathManager()
        self.rd_baker = ResourceDataBaker()
        self.PostMan = PostMan()

    def channel_post_multi_resources(self, jreq, req_path):
        """
        Identifies the post path's goal : create a resource instance or update a mixin collection
        Args:
            @param jreq: Body content of the post request
            @param req_path: Address to which this post request was sent
        """
        #Step[1]: detect the goal of the request

        if jreq.has_key('resources') or jreq.has_key('links'):
            is_kind_loc = True
        else:
            is_kind_loc = False

        if is_kind_loc is True:

            #Step[2a]: This is a create new resources request

            db_occi_ids_locs = self.rd_baker.bake_to_post_multi_resources_2a()

            #Step[3a]: Look for the default attributes to complete the attribute description of the resource:
            default_attributes = self.rd_baker.bake_to_get_default_attributes(req_path)

            if db_occi_ids_locs is None or default_attributes is None:
                return "An error has occurred, please check log for more details", return_code['Internal Server Error']
            else:

                #Step[4a]: Ask the managers to create the new resources

                if jreq.has_key('resources'):
                    logger.debug(
                        "===== Channel_post_multi_resources ==== : Post on kind path to create a new resource channeled")
                    new_resources, resp_code_r = self.manager_r.register_resources(jreq['resources'], req_path,
                        db_occi_ids_locs, default_attributes)
                else:
                    new_resources = list()
                    resp_code_r = return_code['OK, and location returned']

                if jreq.has_key('links'):
                    logger.debug(
                        "===== Channel_post_multi_resources ==== : Post on kind path to create a new link channeled")
                    new_links, resp_code_l = self.manager_l.register_links_explicit(jreq['links'], req_path,
                        db_occi_ids_locs, default_attributes)
                else:
                    new_links = list()
                    resp_code_l = return_code['OK, and location returned']

                if resp_code_r is not return_code['OK, and location returned']\
                or resp_code_l is not return_code['OK, and location returned']:
                    return "An error has occurred, please check log for more details", return_code['Bad Request']

                #Step[5a]: Save the new resources
                entities = new_resources + new_links

                self.PostMan.save_registered_docs_in_db(entities)
                logger.debug("===== Channel_post_multi_resources ==== : Finished (2a) with success")

                locations = list()

                for item in entities:
                    locations.append(item['OCCI_Location'])

                backend_m.create_entities(entities)

                return locations, return_code['OK, and location returned']

                #Step[2b]: This is an associate mixins to resources request

        elif jreq.has_key('X-OCCI-Location'):

            #Step[3b]: Get the necessary data from DB
            nb_res, mix_id = self.rd_baker.bake_to_post_multi_resources_2b(req_path)

            if nb_res is None:
                return "An error has occurred, please check log for more details", return_code['Internal Server Error']
            elif nb_res is 0:
                return "An error has occurred, please check log for more details", return_code['Not Found']
            else:
                to_search_for = jreq['X-OCCI-Location']

                db_docs = self.rd_baker.bake_to_post_multi_resources_2b2(to_search_for)

                if db_docs is 0:
                    return "An error has occurred, please check log for more details", return_code['Not Found']

                elif db_docs is None:
                    return "An error has occurred, please check log for more details", return_code[
                                                                                       'Internal Server Error']

                else:
                    #Step[4b]: Ask the managers to associate mixins to resources
                    logger.debug(
                        "===== Channel_post_multi_resources ==== : Post on mixin path to associate a mixin channeled")
                    updated_entities, resp_code_e = associate_entities_to_a_mixin(mix_id, db_docs)

                    self.PostMan.save_updated_docs_in_db(updated_entities)
                    logger.debug("===== Channel_post_multi_resources ==== : Finished (2b) with success")
                    backend_m.update_entities(db_docs, updated_entities)
                    return "", return_code['OK']
        else:
            return "An error has occurred, please check log for more details", return_code['Bad Request']

    def channel_get_all_entities(self, req_path, jreq):
        """
        Retrieve all entities belonging to a kind or a mixin or get on a path

        Args:
            @param req_path: Address to which this post request was sent
            @param jreq: Data provided for filtering
        """

        #Step[1]: Retrieve the kind/mixin from DB

        res = self.rd_baker.bake_to_channel_get_all_entities(req_path)

        if res is None:
            return "An error has occurred, please check log for more details", return_code['Internal Server Error']

        elif res is 0:

            logger.warning("===== Channel_get_all_multi_entities ===== : This is a get on a path " + req_path)
            #Step[1b]: Get on path to retrieve the entities under that path
            var, resp_code = self.jungler_p.channel_get_on_path(req_path, jreq)
            return var, resp_code

        else:
            q = res.first()
            #Step[2]: Retrieve the entities related to the kind/mixin
            entities = self.rd_baker.bake_to_get_all_entities(q['value'][1], q['value'][0])
            if entities is None:
                return "An error has occurred, please check log for more details", return_code['Internal Server Error']

            else:

                logger.debug("===== Channel_get_all_entities ==== : Finished with success")
                return entities, return_code['OK']

    def channel_get_filtered_entities(self, req_path, terms):
        """
        Retrieve entities belonging to a kind or a mixin matching the terms specified or get entities on a path with filtering
        Args:
            @param req_path: Address to which this post request was sent
            @param terms: Terms to filter entities
        """
        #Step[1]: Get all the entities related to kind/mixin or get on a path with filtering
        entities, ok = self.channel_get_all_entities(req_path, terms)

        if ok == return_code['OK']:
            #Note: We now need the resources OCCI descriptions so we go back to the database
            descriptions_res, descriptions_link = self.rd_baker.bake_to_get_filtered_entities(entities)

            if descriptions_res is None:
                return "An error has occurred, please check log for more details", return_code['Internal Server Error']
            else:
                #Step[2]: Ask the managers to do the filtering
                if terms.has_key('resources'):
                    logger.debug("===== Channel_get_filtered: Resources are sent to filter =====")
                    filtered_res, resp_code_r = self.manager_r.get_filtered_resources(terms['resources'],
                        descriptions_res)
                else:
                    logger.debug("===== Channel_get_filtered: No Resource filter =====")
                    filtered_res = list()
                    resp_code_r = return_code['OK']

                if terms.has_key('links'):
                    logger.debug("===== Channel_get_filtered: Links are sent to filter =====")
                    filtered_links, resp_code_l = self.manager_l.get_filtered_links(terms['links'], descriptions_link)
                else:
                    logger.debug("===== Channel_get_filtered: No Links filter =====")
                    filtered_links = list()
                    resp_code_l = return_code['OK']

                if resp_code_l is not return_code['OK'] or resp_code_r is not return_code['OK']:
                    return "An error has occurred, please check log for more details", return_code['Bad Request']

                result = filtered_res + filtered_links

                logger.debug("===== Channel_get_filtered_entities ==== : Finished with success")

                return result, return_code['OK']


    def channel_put_multi(self, jreq, req_url):
        """
        Update the mixin collection of resources
        Args:

            @param jreq: OCCI_Locations of the resources
            @param req_url: URL of the request
        """

        #Step[1]: Get the necessary data from DB

        nb_res, mix_id = self.rd_baker.bake_to_post_multi_resources_2b(req_url)
        if nb_res is None:
            return "An error has occurred, please check log for more details", return_code['Internal Server Error']
        elif nb_res is 0:
            return "An error has occurred, please check log for more details", return_code['Not Found']
        else:
            to_search_for = jreq['X-OCCI-Location']
            db_docs = self.rd_baker.bake_to_post_multi_resources_2b2(to_search_for)

            if db_docs is 0:
                return "An error has occurred, please check log for more details", return_code['Not Found']

            elif db_docs is None:
                return "An error has occurred, please check log for more details", return_code[
                    'Internal Server Error']

            else:
                #Step[2]: Ask the managers to associate mixins to resources
                logger.debug(
                    "===== Channel_put_multi_resources ==== : Put on mixin path to associate a mixin channeled")
                updated_entities, resp_code_e = associate_entities_to_a_mixin(mix_id, db_docs)

                self.PostMan.save_updated_docs_in_db(updated_entities)

                logger.debug("===== Channel_put_multi_resources ==== : Finished (2b) with success")
                backend_m.update_entities(db_docs, updated_entities)
                return "", return_code['OK']


    def channel_delete_multi(self, jreq, req_url):
        """
        Remove the mixin from the resources
        Args:
            @param jreq: OCCI_Locations of the resources
            @param req_url: URL of the request
        """

        #Step[1]: Get the necessary data from DB

        nb_res, mix_id = self.rd_baker.bake_to_post_multi_resources_2b(req_url)
        if nb_res is None:
            return "An error has occurred, please check log for more details", return_code['Internal Server Error']

        elif nb_res is 0:
            return "An error has occurred, please check log for more details", return_code['Not Found']

        else:
            to_search_for = jreq['X-OCCI-Location']
            db_docs = self.rd_baker.bake_to_post_multi_resources_2b2(to_search_for)

            if db_docs is 0:
                return "An error has occurred, please check log for more details", return_code['Not Found']

            elif db_docs is None:
                return "An error has occurred, please check log for more details", return_code[
                    'Internal Server Error']

            else:
                logger.debug(" ===== Delete_multi_entities : Delete on mixin to Dissociate mixins channeled =====")
                updated_entities, resp_code_e = dissociate_entities_from_a_mixin(mix_id, db_docs)

            if resp_code_e is not return_code['OK']:
                return "An error has occurred, please check log for more details", return_code['Bad Request']

            self.PostMan.save_updated_docs_in_db(updated_entities)

            backend_m.update_entities(db_docs,updated_entities)

            return "", return_code['OK']

    def channel_trigger_actions(self, jBody, req_url, triggered_action):
        """
        Trigger action on a collection of resources related to a kind or mixin
        Args:
            @param jBody: Action provided
            @param req_url: URL of the request
            @param triggered_action: Action name
        """

        #Step[1]: Get the necessary data:

        kind_ids, entities = self.rd_baker.bake_to_channel_trigger_actions(req_url)

        if kind_ids is None:
            return "An error has occurred, please check log for more details", return_code['Internal Server Error']
        if kind_ids is 0:
            return "An error has occured, please check log for more details", return_code['Not Found']
        else:
            providers = list()
            #Step[2]: Get the providers of the instances
            for item in kind_ids:
                provider = self.rd_baker.bake_to_get_provider(item)
                providers.append(provider)

            if jBody.has_key('attributes') is True:

                parameters = jBody['attributes']
            else:
                parameters = None

            #Step[3]: Ask the backend to trigger the action on the resources
            backend_m.trigger_action_on_multi_resource(entities,providers, jBody['actions'][0],parameters)

            return "", return_code['OK']


#=======================================================================================================================
#                                           Independent Functions
#=======================================================================================================================

def associate_entities_to_a_mixin( mix_id, db_docs):
    """
    Add a single mixin to entities
    Args:
        @param mix_id: OCCI ID of the mixin
        @param db_docs: documents of the entities already contained in the database
    """
    if mix_id is not None:
        for doc in db_docs:
            if doc['OCCI_Description'].has_key('mixins'):
                var = doc['OCCI_Description']['mixins']
                try:
                    var.index(mix_id)
                except ValueError:
                    var.append(mix_id)
                    doc['OCCI_Description']['mixins'] = var
            else:
                doc['OCCI_Description']['mixins'] = [mix_id]
        logger.debug("Associate mixin : Mixin associated with success")
        return db_docs, return_code['OK']
    else:
        logger.debug("Associate mixin : Mixin description problem")
        return list(), return_code['Not Found']


def dissociate_entities_from_a_mixin(mix_id, db_docs):
    """
    Remove a single mixin from entities
    Args:
        @param mix_id: OCCI ID of the mixin
        @param db_docs: documents of the entities already contained in the database
    """
    if mix_id is not None:
        for doc in db_docs:
            if doc['OCCI_Description'].has_key('mixins'):
                var = doc['OCCI_Description']['mixins']
                try:
                    var.remove(mix_id)

                    doc['OCCI_Description']['mixins'] = var
                except ValueError as e:
                    logger.error('Diss a mixin: ' + e.message)

        logger.debug("Dissociate mixin : Mixin dissociated with success")
        return db_docs, return_code['OK']
    else:
        logger.debug("Dissociate mixin : Mixin description problem")
        return list(), return_code['Not Found']