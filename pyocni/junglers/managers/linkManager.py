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

#
##=======================================================================================================================
##                                           LinkManager
##=======================================================================================================================

import pyocni.pyocni_tools.config as config
import pyocni.pyocni_tools.occi_Joker as joker

import pyocni.pyocni_tools.uuid_Generator as uuid_Generator

try:
    import simplejson as json
except ImportError:
    import json

from pyocni.pyocni_tools.config import return_code

# getting the Logger
logger = config.logger

class LinkManager(object):
    """
    Manager of link documents.
    """
    def register_links_explicit(self,occi_descriptions,url_path,db_occi_ids_locs, default_attributes):
        """
        Add new links to database
        Args:
            @param occi_descriptions: The new Link OCCI descriptions
            @param db_occi_ids_locs: OCCI ID and locations extracted from the database
            @param url_path: URL path of the request
            @param default_attributes: The default attributes extracted from the kind
        """

        loc_res = list()
        kind_occi_id = None

        #Step[1] Extract the kind of the sent request

        for elem in db_occi_ids_locs:
            if elem['OCCI_Location'] == url_path:
                kind_occi_id = elem['OCCI_ID']
                break

        if kind_occi_id is not None:

            for desc in occi_descriptions:

                #Note: Verify if the kind to which this request is sent is the same as the one in the link description
                if desc['kind'] == kind_occi_id:
                     #Note: Create the URL of the Link using the id provided in the OCCI description.

                    loc = joker.make_entity_location_from_url(url_path,desc['id'])
                    #Note: Verify the uniqueness of the Address.
                    exist_same = joker.verify_existences_teta([loc],db_occi_ids_locs)

                    if exist_same is False:
                        jData = dict()
                        jData['_id'] = uuid_Generator.get_UUID()
                        jData['OCCI_Location']= loc
                        full_att = joker.complete_occi_description_with_default_attributes(desc['attributes'],
                                                                                           default_attributes)
                        desc['attributes'] = full_att
                        jData['OCCI_Description']= desc
                        jData['Type']= "Link"
                        loc_res.append(jData)
                    else:
                        logger.error(" ===== Register links explicit : Bad Link id ===== ")
                        return list(),return_code['Conflict']
                else:
                    mesg = "Kind description and kind location don't match"
                    logger.error(" =====  Register links explicit: " + mesg + " ===== ")
                    return list(),return_code['Conflict']

             #Step[3]: return the list of resources

            logger.debug(" ===== Register links explicit : links sent for creation ===== ")
            return loc_res,return_code['OK, and location returned']
        else:
            mesg = "No kind corresponding to this location was found"
            logger.error(" ===== Register links explicit: " + mesg + " =====")
            return list(),return_code['Not Found']

    def get_filtered_links(self, filters, descriptions_link):
        """
        Retrieve the resources that match the filters provided
        Args:
            @param filters: Filters
            @param descriptions_link: Link descriptions
        """
        var = list()
        try:
            for desc in descriptions_link:
                #Step[1]: Check if the descriptions match the filters
                for filter in filters:
                    checks =joker.filter_occi_description(desc['OCCI_Description'],filter)
                    if checks is True:
                        #Step[2]: Keep the record of those descriptions matching the filter
                        var.append(desc['OCCI_ID'])
                        logger.debug(" ===== Get_filtered_links : A link document was found =====")
                        break
            return var,return_code['OK']

        except Exception as e:
            logger.error(" ===== Get_filtered_links : " + e.message + " ===== ")
            return list(),return_code['Internal Server Error']

    def register_custom_link(self, occi_description, path_url, db_occi_ids_locs):
        """
        Add a new link with a custom URL to the database
        Args:
            @param occi_description: link description
            @param path_url: Custom URL of the link
            @param db_occi_ids_locs: Ids and locations from the database
        """
        #Step[1]: Verify if the kind of the new link exists
        ok_k = joker.verify_existences_beta([occi_description['kind']],db_occi_ids_locs)
        #Step[2]: Create the link
        if ok_k is True:

            jData = dict()
            jData['_id'] = uuid_Generator.get_UUID()
            jData['OCCI_Location']= path_url
            jData['OCCI_Description']= occi_description
            jData['Type']= "Link"

        else:
            mesg = "Kind description does not exist"
            logger.error(" ===== Register custom link : " + mesg + " ===== ")
            return list(),return_code['Not Found']

        logger.debug(" ===== Register Custom link: Link sent for creation ===== ")
        return jData,return_code['OK, and location returned']

    def update_link(self, old_doc, occi_new_description):
        """
        Fully Update the link description attached to the custom URL
        Args:
            @param old_doc: old link document
            @param occi_new_description: new link description
        """
        try:

            logger.debug("===== Update_link: Link sent for update =====")
            #Step[1]: Replace the old occi description with the new occi description
            old_doc['OCCI_Description'] = occi_new_description
            #Step[2]: Return the hole document for update
            return old_doc, return_code['OK, and location returned']

        except Exception as e:

            logger.error("===== Update_link: Resource couldn't be updated =====")
            return {}, return_code['Internal Server Error']


    def partial_link_update(self, old_data, occi_description):
        """
        Partially update the link's old occi description
        Args:

            @param occi_description: link description
            @param old_data: Old link description
        """

        #Step[1]: try a partial link update
        problems, updated_data = joker.update_occi_entity_description(old_data, occi_description)

        #Step[2]: if no problem then return the new data for update else return the old data with conflict status code
        if problems is False:
            logger.debug("===== Update_partial_resource: Resource sent for update =====")
            return updated_data, return_code['OK, and location returned']
        else:
            logger.error("===== Update_partial_resource: Resource couldn't have been fully updated =====")
            return old_data, return_code['Conflict']

