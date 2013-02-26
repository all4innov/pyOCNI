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
Created on Jun 01, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@license: Apache License, Version 2.0
"""

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

class ResourceManager(object):
    """
    Manager of resource documents
    """

    def register_resources(self, occi_descriptions, url_path, db_occi_ids_locs, default_attributes):
        """
        Add new resources to the database
        Args:

            @param occi_descriptions: the OCCI description of the new resources
            @param db_occi_ids_locs: OCCI IDs and OCCI Location extracted from the database
            @param url_path: URL path of the request
            @param default_attributes: the default attributes extracted from kind
        """
        loc_res = list()
        kind_occi_id = None

        #Step[1]: Get the kind on which the request was sent

        for elem in db_occi_ids_locs:
            if elem['OCCI_Location'] == url_path:
                kind_occi_id = elem['OCCI_ID']
                break

        if kind_occi_id is not None:
            for desc in occi_descriptions:
                #Note: Verify if the kind to which this request is sent is the same as the one in the link description
                if desc['kind'] == kind_occi_id:
                    #Note: create the url of the id based on the id provided in the request
                    loc = joker.make_entity_location_from_url(url_path, desc['id'])
                    exist_same = joker.verify_existences_teta([loc], db_occi_ids_locs)

                    #Step[2]: Create the new resource
                    if exist_same is False:
                        jData = dict()
                        jData['_id'] = uuid_Generator.get_UUID()
                        jData['OCCI_Location'] = loc
                        full_att = joker.complete_occi_description_with_default_attributes(desc['attributes'],
                            default_attributes)
                        desc['attributes'] = full_att
                        jData['OCCI_Description'] = desc
                        jData['Type'] = "Resource"
                        loc_res.append(jData)
                    else:
                        logger.error(" ===== Register_resources : Bad Resource id ===== ")
                        return list(), return_code['Conflict']

                else:
                    mesg = "Kind description and kind location don't match"
                    logger.error("===== Register_resources: " + mesg + " ===== ")
                    return list(), return_code['Conflict']
            #Step[3]: return the list of resources for creation
            logger.debug("===== Register_resources: Resources sent for creation =====")
            return loc_res, return_code['OK, and location returned']
        else:
            mesg = "No kind corresponding to this location was found"
            logger.error("===== Register_resources: " + mesg + " =====")
            return list(), return_code['Not Found']




    def get_filtered_resources(self, filters, descriptions_res):
        """
        Retrieve the resources that match the filters provided
        Args:
            @param filters: Filters
            @param descriptions_res: Resource descriptions
        """
        var = list()
        try:
            for desc in descriptions_res:
                for filter in filters:
                    #Step[1]: Check if descriptions match the filters
                    checks = joker.filter_occi_description(desc['OCCI_Description'], filter)

                    if checks is True:
                        #Step[2]: Keep record of those description matching the filter
                        var.append(desc['OCCI_ID'])
                        logger.debug("===== Get_filtered_resources: A resource document is found =====")

            return var, return_code['OK']

        except Exception as e:
            logger.error("===== Get_filtered_resources : " + e.message + " =====")
            return list(), return_code['Internal Server Error']

    def register_custom_resource(self, occi_description, path_url, db_occi_ids_locs):
        """
        Add a new resource with a custom URL to the database
        Args:

            @param occi_description: Resource description
            @param path_url: Custom URL of the resource
            @param db_occi_ids_locs: Ids and locations from the database
        """

        #Step[1]: Verify if the kind of the new resource exists
        ok_k = joker.verify_existences_beta([occi_description['kind']], db_occi_ids_locs)

        #Step[2]: create the resource
        if ok_k is True:
            jData = dict()
            jData['_id'] = uuid_Generator.get_UUID()
            jData['OCCI_Location'] = path_url
            jData['OCCI_Description'] = occi_description
            jData['Type'] = "Resource"

        else:
            mesg = "This kind does not exist"
            logger.error(" ===== Register_custom_resource : " + mesg + " =====")
            return list(), return_code['Not Found']

        #Step[3]: send resource for creation
        logger.debug("===== Register_custom_resource :  Resources sent for creation")
        return jData, return_code['OK, and location returned']

    def update_resource(self, old_doc, occi_new_description):
        """
        Fully update the resource's old description
        Args:
            @param old_doc: Old resource document
            @param occi_new_description: New resource description
        """
        try:

            logger.debug("===== Update_resource: Resource sent for update =====")
            #Step[1]: Replace the old occi description with the new occi description
            old_doc['OCCI_Description'] = occi_new_description
            #Step[2]: Return the hole document for update
            return old_doc, return_code['OK, and location returned']

        except Exception as e:

            logger.error("===== Update_resource: Resource couldn't be updated =====")
            return {}, return_code['Internal Server Error']

    def partial_resource_update(self, old_data, occi_description):
        """
        Partially update the resource's old occi description
        Args:

            @param occi_description: Resource description
            @param old_data: Old resource description
        """

        #Step[1]: try a partial resource update
        problems, updated_data = joker.update_occi_entity_description(old_data, occi_description)

        #Step[2]: if no problem then return the new data for update else return the old data with conflict status code
        if problems is False:
            logger.debug("===== Update_partial_resource: Resource sent for update =====")
            return updated_data, return_code['OK, and location returned']
        else:
            logger.error("===== Update_partial_resource: Resource couldn't have been fully updated =====")
            return old_data, return_code['Conflict']
