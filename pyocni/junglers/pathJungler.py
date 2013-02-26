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
Created on Jun 21, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@license: Apache License, Version 2.0
"""

import pyocni.pyocni_tools.config as config
import pyocni.pyocni_tools.occi_Joker as joker
from pyocni.dataBakers.resource_dataBaker import ResourceDataBaker
from postMan.the_post_man import PostMan

try:
    import simplejson as json
except ImportError:
    import json
from pyocni.pyocni_tools.config import return_code
# getting the Logger
logger = config.logger

class PathManager(object):
    """
    Handles operations concerning Paths
    """

    def __init__(self):

        self.rd_baker = ResourceDataBaker()
        self.PostMan = PostMan()

    def channel_get_on_path(self, req_path, terms):
        """
        Channel get on path request to the manager responsible
        Args:
            @param req_path: Address to which this post request was sent
            @param terms: Data provided for filtering
        """

        locations = list()
        #Step[1]: get the necessary data from DB
        occi_loc = self.rd_baker.bake_to_get_on_path()

        if terms is "":
            #Step[2a]: Get on path without filtering
            if occi_loc is None:
                return "An error has occurred, please check log for more details", return_code['Internal Server Error']

            else:

                for str_loc in occi_loc:

                    if str_loc.find(req_path) is not -1:
                        locations.append(str_loc)

            logger.debug("===== Channel_get_on_Path: Finished with success ===== ")
            return locations, return_code['OK']

        else:
            #Step[2b]: Get on path with filtering
            for str_loc in occi_loc:

                if str_loc.endswith("/") is False and str_loc.find(req_path) is not -1:
                    locations.append(str_loc)

            descriptions = self.rd_baker.bake_to_get_on_path_filtered(locations)

            if descriptions is None:
                return "An error has occurred, please check log for more details", return_code['Internal Server Error']
            else:
                if terms.has_key('resources'):
                    result_res, resp_code_r = get_filtered(terms['resources'], descriptions)
                else:
                    result_res = list()
                    resp_code_r = return_code['OK']

                if terms.has_key('links'):
                    result_link, resp_code_l = get_filtered(terms['links'], descriptions)
                else:
                    result_link = list()
                    resp_code_l = return_code['OK']

                if resp_code_l is not return_code['OK'] or resp_code_r is not return_code['OK']:
                    return "An error has occurred, please check logs for more details", return_code[
                                                                                        'Internal Server Error']

                result = result_res + result_link

                logger.debug("===== Channel_get_on_Path: Finished with success ===== ")
                return result, return_code['OK']


    def channel_delete_on_path(self, req_path):
        """
        Channel the delete resources request to the path manager
        Args:
            @param req_path: Address to which this post request was sent
        """
        occi_loc,doc_loc = self.rd_baker.bake_to_delete_on_path()

        if occi_loc is None or doc_loc is None:
            return "An error has occurred, please check log for more details", return_code['Internal Server Error']
        else:
            to_delete = list()

            for i in range(len(occi_loc)):

                str_loc = str(occi_loc[i])
                if str_loc.find(req_path) is not -1:
                    to_delete.append(doc_loc[i])

            self.PostMan.delete_entities_in_db(to_delete)

            logger.debug("===== Channel Delete on Path: Finished with success =====")
            return "", return_code['OK']


def get_filtered(filters, descriptions_entities):
    """
    Retrieve the resources  that match the filters provided
    Args:
        @param filters: Filters
        @param descriptions_entities: Entity descriptions
    """
    var = list()

    try:
        for desc in descriptions_entities:
            for filter in filters:

                checks = joker.filter_occi_description(desc['OCCI_Description'], filter)

                if checks is True:
                    var.append(desc['OCCI_ID'])
                    logger.debug("Entity filtered : document found")
                    break
        return var, return_code['OK']

    except Exception as e:
        logger.error("filtered entity : " + e.message)
        return list(), return_code['Internal Server Error']