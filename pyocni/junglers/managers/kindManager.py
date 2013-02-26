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
import pyocni.pyocni_tools.occi_Joker as joker
import pyocni.pyocni_tools.couchdbdoc_Joker as doc_Joker

import pyocni.pyocni_tools.uuid_Generator as uuid_Generator

try:
    import simplejson as json
except ImportError:
    import json

from pyocni.pyocni_tools.config import return_code

# getting the Logger
logger = config.logger

class KindManager:
    """

        Manager for Kind documents

    """

    def get_filtered_kinds(self, jfilters, db_kinds):
        """
        Returns kind documents matching the filter provided
        Args:
            @param jfilters: description of the kind filter document
            @param db_kinds: Kind descriptions that already exist in database
        """
        var = list()

        try:
            for elem in db_kinds:
                for jfilter in jfilters:
                    #Step[1]: compare kinds to the filter
                    ok = joker.filter_occi_description(elem, jfilter)
                    if ok is True:
                        #Step[2]: Store the filter matching documents
                        var.append(elem)
                        logger.debug("===== Get_filtered_Kinds: A kind was found =====")
                        break
            return var, return_code['OK']

        except Exception as e:

            logger.error("===== Get_filtered_Kinds: " + e.message + "=====")
            return "An error has occurred", return_code['Internal Server Error']


    def register_kinds(self, descriptions, db_occi_ids, db_occi_locs):
        """
        Create new kinds
        Args:
            @param descriptions: OCCI kind descriptions
            @param db_occi_ids: Kind IDs already existing in the database
            @param db_occi_locs: Kind locations already existing in the database
        """
        loc_res = list()

        resp_code = return_code['OK']

        for desc in descriptions:

            occi_id = joker.get_description_id(desc)
            #Step[1]: verify uniqueness of the new kind
            ok_k = joker.verify_occi_uniqueness(occi_id, db_occi_ids)

            if ok_k is True:
                occi_loc = joker.make_category_location(desc)
                ok_loc = joker.verify_occi_uniqueness(occi_loc, db_occi_locs)

                if ok_loc is True:
                    jData = dict()
                    jData['_id'] = uuid_Generator.get_UUID()
                    jData['OCCI_Location'] = occi_loc
                    jData['OCCI_Description'] = desc
                    jData['OCCI_ID'] = occi_id
                    jData['Type'] = "Kind"
                    #Default backend is dummy
                    jData['Provider'] = {"local": [config.DEFAULT_BACKEND], "remote": []}
                    loc_res.append(jData)

                else:
                    message = "Location conflict, kind will not be created."
                    logger.error("===== Register kind : " + message + " =====")
                    resp_code = return_code['Conflict']
                    return list(), resp_code
            else:
                message = "This kind description already exists in document "
                logger.error("===== Register kind : " + message + " =====")
                resp_code = return_code['Conflict']
                return list(), resp_code

        return loc_res, resp_code


    def update_OCCI_kind_descriptions(self, new_data, db_data):
        """
        Updates the OCCI kind description which OCCI_ID is equal to OCCI_ID contained in new_data
        Args:

            @param new_data: Data containing the OCCI ID of the kind and the new OCCI kind description
            @param db_data: Categories already contained in the database

        """
        to_update = list()

        resp_code = return_code['OK']

        for desc in new_data:

            occi_id = joker.get_description_id(desc)
            #Step[1]: Extract the old document
            old_doc = joker.extract_doc(occi_id, db_data)

            if old_doc is not None:
                #Step[2]: Update kind OCCI description
                problems, occi_description = joker.update_occi_category_description(old_doc['OCCI_Description'], desc)

                #Step[3]: Detect if there is problems
                if problems is True:

                    message = "Kind OCCI description " + occi_id + " has not been totally updated."
                    logger.error("===== Kind OCCI description update:" + message + " =====")
                    return list(), return_code['Bad Request']
                else:
                    message = "Kind OCCI description " + occi_id + " has been updated successfully"
                    old_doc['OCCI_Description'] = occi_description

                    #Step[4]: If no problem, just append the doc to the to_update list
                    to_update.append(old_doc)

                    logger.debug("===== Update kind OCCI description : " + message + " =====")

            else:
                message = "Kind document " + occi_id + " couldn\'t be found "
                logger.error("===== Update kind OCCI description : " + message + " =====")
                return list(), return_code['Not Found']

        return to_update, resp_code

    def update_kind_providers(self, new_data, db_data):
        """
        Updates the kind provider field which document OCCI_ID is equal to OCCI_ID contained in data

        Args:

            @param new_data: Data containing the OCCI ID of the kind and the new kind provider description
            @param db_data: Categories already contained in the database

        """
        to_update = list()
        resp_code = return_code['OK']

        for desc in new_data:

            #Step[1]: Extract the old document
            occi_id = desc['OCCI_ID']
            old_doc = joker.extract_doc(occi_id, db_data)

            if old_doc is not None:
                #Step[2]: Update the kind provider
                provider_description, problems = doc_Joker.update_kind_provider(old_doc['Provider'], desc['Provider'])

                if problems is True:
                    message = "Kind provider description " + occi_id + " has not been totally updated."
                    logger.error("===== Kind provider description update " + message + " =====")
                    return list(), return_code['Bad Request']
                else:
                    message = "Kind provider description " + occi_id + " has been updated successfully"
                    old_doc['Provider'] = provider_description
                    #Step[3]: if OK, append the kind doc to the to_update list
                    to_update.append(old_doc)
                    logger.debug("===== Update kind provider description : " + message + " =====")

            else:
                message = "Kind document " + occi_id + " couldn\'t be found "
                logger.error("===== Update kind provider des : " + message + " =====")
                return list(), return_code['Not Found']
        return to_update, resp_code


    def delete_kind_documents(self, descriptions, db_categories):
        """
        Delete kind documents that is related to the scheme + term contained in the description provided
        Args:
            @param descriptions: OCCI description of the kind document to delete
            @param db_categories: Category data already contained in the database

        """

        kind_ref = list()
        res_code = return_code['OK']

        #Step[1]: Verify the existence of such kind document

        for desc in descriptions:

            occi_id = joker.get_description_id(desc)

            kind_id_rev = joker.verify_exist_occi_id(occi_id, db_categories)

            if kind_id_rev is not None:
                #Step[2]: if Yes, return kind doc ref for delete
                kind_ref.append(kind_id_rev)
                event = "Kind document " + occi_id + " is sent for delete "
                logger.debug("===== Delete_kind_documents : " + event + " =====")

            else:
                event = "Could not find this kind document " + occi_id
                logger.error("===== Delete kind : " + event + " ===== ")
                return list(), return_code['Bad Request']

        return kind_ref, res_code
