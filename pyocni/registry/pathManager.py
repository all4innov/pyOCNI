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
from pyocni.registry.entityManager import ResourceManager,LinkManager
from pyocni.registry.categoryManager import KindManager,MixinManager
from datetime import datetime
from pyocni.pyocni_tools import uuid_Generator
from couchdbkit import *
from pyocni.pyocni_tools.config import return_code
# getting the Logger
logger = config.logger


# Get the database server configuration

DB_server_IP = config.DB_IP
DB_server_PORT = config.DB_PORT

def verify_location_type(location):
    """
    Verify the existence of a kind with such location
    Args:
        @param location: location of kind
    """
    kind_location = "http://" + config.OCNI_IP + ":" + config.OCNI_PORT + "/-" + location
    self.add_design_kind_docs_to_db()
    database = self.server.get_or_create_db(config.Kind_DB)
    query = database.view('/get_kind/by_occi_location',key = kind_location)
    if query.count() is 0:
        logger.debug("Kind with kind location = " + kind_location + " not found")
        return False,None
    else:
        return True,query.first()['value']

def associate_entities_to_mixin(user_id, param, location, db_occi_ids_locs):
    pass


class PathManager(object):
    """

    """

    def __init__(self):

        self.manager_r = ResourceManager()
        self.manager_l = LinkManager()

    def channel_post_path(self,user_id,jreq,location):
        """
        Identifies the post path's goal : create a resource instance or update a mixin
        Args:
            @param user_id: ID of the issuer of the post request
            @param jreq: Body content of the post request
            @param location: Address to which this post request was sent
        """
        database = config.prepare_PyOCNI_db()
        try:
            jreq.index('resources')
            is_kind_loc = True
        except KeyError:
            try:
                jreq.index('links')
                is_kind_loc = True
            except KeyError:
                jreq.index('OCCI_Location')
                is_kind_loc = False
        except Exception:
            return "An error has occurred, please check log for more details",return_code['Internal Server Error']

        if is_kind_loc is True:
            try:
                query = database.view('/get_views/occi_id_occi_location')
            except Exception as e:
                logger.error("Category delete : " + e.message)
                return "An error has occurred, please check log for more details",return_code['Internal Server Error']
            db_occi_ids_locs = list()
            for q in query:
                db_occi_ids_locs.append({"OCCI_ID" : q['key'],"OCCI_Location":q['value']})
            try:
                jreq.index('resources')
                logger.debug("Post path : Post on kind path to create a new resource channeled")
                new_resources, resp_code_r = self.manager_r.register_resources(user_id,jreq['resources'],location,db_occi_ids_locs)
            except Exception as e:
                logger.error("Post path : " +e.message)
                new_resources = list()
                resp_code_r = return_code['OK']
            try:
                jreq.index('links')
                logger.debug("Post path : Post on kind path to create a new link channeled")
                new_links, resp_code_l = self.manager_l.register_links_explicit(user_id,jreq['links'],location,db_occi_ids_locs)
            except Exception as e:
                logger.error("Post path : " +e.message)
                new_links = list()
                resp_code_l = return_code['OK']
            if resp_code_r is not return_code['OK'] or resp_code_l is not return_code['OK']:
                return "An error has occurred, please check log for more details",return_code['Bad Request']

            categories = new_resources + new_links
            database.save_docs(categories,use_uuids=True, all_or_nothing=True)
            return "",return_code['OK']

        else:

            try:
                query = database.view('/get_views/occi_location_doc')
            except Exception as e:
                logger.error("Category delete : " + e.message)
                return "An error has occurred, please check log for more details",return_code['Internal Server Error']
            db_occi_locs_docs = list()
            for q in query:
                db_occi_locs_docs.append({"OCCI_Location" : q['key'],"Doc":q['value']})

            try:
                jreq.index('OCCI_Location')
                logger.debug("Post path : Post on kind path to create a new resource channeled")
                updated_entities,resp_code_e = associate_entities_to_mixin(user_id,jreq['OCCI_Location'],location,db_occi_locs_docs)
            except Exception as e:
                logger.error("Post path : " +e.message)
                updated_entities = list()
                resp_code_e = return_code['OK']

            if resp_code_e is not return_code['OK']:
                return "An error has occurred, please check log for more details",return_code['Bad Request']

            database.save_docs(updated_entities,force_update=True, all_or_nothing=True)
            return "",return_code['OK']

    def channel_get_path(self,user_id,jreq,location):
        """
        Channel the get request to the right method
        Args:
            @param user_id: ID of the issuer of the post request
            @param jreq: Body content of the post request
            @param location: Address to which this post request was sent
        """
        #Verify if this is a kind location
        ok_k = self.manager_k.verify_kind_location(location)
        #if yes : call the ResourceManager to retrieve resource instances belonging to this kind
        if ok_k is True:
            logger.debug("Get path : Get on kind path channeled")
        else:
        #if no : verify if this is a mixin location
            ok_m = self.manager_m.verify_mixin_location(location)
            if ok_m is True:
                #if yes: call the ResourceManager to retrieve all resource instances belonging to this mixin
                logger.debug("Get path : Get on mixin path channeled")
            else:
                #Get all locations and state hierarchy below this path
                logger.debug("Get path : Get on path channeled")
