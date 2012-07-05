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
Created on Jun 21, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@version: 0.3
@license: LGPL - Lesser General Public License
"""

import pyocni.pyocni_tools.config as config
import pyocni.pyocni_tools.occi_Joker as joker
import pyocni.pyocni_tools.couchdbdoc_Joker as doc_Joker
try:
    import simplejson as json
except ImportError:
    import json
from pyocni.pyocni_tools.config import return_code
# getting the Logger
logger = config.logger





class PathManager(object):
    """
    CRUD operations on Path
    """

    def channel_get_on_path(self,user_id,req_path,terms):
        """
        Channel the get request to the right method
        Args:
            @param user_id: ID of the issuer of the post request
            @param req_path: Address to which this post request was sent
            @param terms: Data provided for filtering
        """

        database = config.prepare_PyOCNI_db()
        locations = list()

        if terms is "":
            try:
                query = database.view('/db_views/my_occi_locations')
            except Exception as e:
                logger.error("Get on Path: " + e.message)
                return "An error has occurred, please check log for more details",return_code['Internal Server Error']
            for q in query:
                str_loc = str(q['key'])
                if str_loc.endswith("/"):
                    str_loc = joker.format_url_path(str_loc)
                else:
                    if q['value'] != user_id:
                        str_loc = ""
                if str_loc.find(req_path) is not -1:
                    locations.append(str_loc)

            logger.debug("Get on Path:"+ req_path +"done with success")
            return locations,return_code['OK']
        else:
            try:
                query = database.view('/db_views/my_occi_locations')
            except Exception as e:
                logger.error("Get on Path: " + e.message)
                return "An error has occurred, please check log for more details",return_code['Internal Server Error']
            for q in query:
                str_loc = str(q['key'])
                if str_loc.endswith("/") is False and str_loc.find(req_path) is not -1:
                    locations.append(str_loc)
            descriptions = list()
            for loc in locations:
                try:
                    query = database.view('/db_views/my_resources',key=[loc,user_id])
                except Exception as e:
                    logger.error("Get on Path: " + e.message)
                    return "An error has occurred, please check log for more details",return_code['Internal Server Error']
                descriptions.append({'OCCI_Description' : query.first()['value'],'OCCI_ID':loc})

            if terms.has_key('resources'):
                result_res,resp_code_r = get_filtered(terms['resources'],descriptions)
            else:
                result_res = list()
                resp_code_r = return_code['OK']

            if terms.has_key('links'):
                result_link,resp_code_l = get_filtered(terms['links'],descriptions)
            else:
                result_link = list()
                resp_code_l = return_code['OK']

            if resp_code_l is not return_code['OK'] or resp_code_r is not return_code['OK']:
                return "An error has occurred, please check logs for more details",return_code['Internal Server Error']

            result = result_res + result_link
            logger.debug("Get on Path: done with success")
            return result,return_code['OK']


    def channel_delete_on_path(self, req_path, user_id):
        """
        Channel the get request to the right method
        Args:
            @param user_id: ID of the issuer of the post request
            @param req_path: Address to which this post request was sent
        """
        database = config.prepare_PyOCNI_db()
        locations = list()
        try:
            query = database.view('/db_views/for_delete_entities',key = user_id)
        except Exception as e:
            logger.error("Delete on Path: " + e.message)
            return "An error has occurred, please check log for more details",return_code['Internal Server Error']
        for q in query:
            str_loc = str(q['value'][0])
            if str_loc.find(req_path) is not -1:
                locations.append({'_id':q['value'][1],'_rev':q['value'][2]})

        logger.debug("Delete on Path: done with success")
        database.delete_docs(locations)
        return "",return_code['OK']


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
                checks =joker.filter_occi_description(desc['OCCI_Description'],filter)
                if checks is True:
                    var.append(desc['OCCI_ID'])
                    logger.debug("Entity filtered : document found")
                    break
        return var,return_code['OK']
    except Exception as e:
        logger.error("filtered entity : " + e.message)
        return list(),return_code['Internal Server Error']