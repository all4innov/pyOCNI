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

import pyocni.pyocni_tools.config as config
import pyocni.pyocni_tools.occi_Joker as joker
from pyocni.registry.categoryManager import KindManager,MixinManager,ActionManager
try:
    import simplejson as json
except ImportError:
    import json
from datetime import datetime
from pyocni.pyocni_tools import uuid_Generator
from couchdbkit import *
from pyocni.pyocni_tools.config import return_code

# getting the Logger
logger = config.logger

class ResourceManager(object):
    """
    Manager of resource and link documents in the couch database.
    """

    def __init__(self):

        self.manager_m = MixinManager()
        self.manager_a = ActionManager()
        self.manager_k = KindManager()


    def register_resources(self,creator,occi_description,occi_kind_location,occi_kind_id):

        """
        Add new resources to the database
        Args:
            @param creator: the user who created these new resources
            @param occi_description: the OCCI description of the new resources
            @param occi_kind_location: the kind location to which belong these new resources
            @param occi_kind_id: the occi kind id of the kind to which belongs these new resources
        """

        database = self.server.get_or_create_db(config.Resource_DB)
        self.add_design_resource_docs_to_db()
        loc_res = list()
        for desc in occi_description:
            #Verify if the kind to which this request is sent is the same as the one in the resource description
            if desc['kind'] == occi_kind_id:
                try:
                    desc.index['actions']
                    existing_actions = self.manager_a.verify_exist_actions(desc['actions'],creator)
                    ok_a = desc['actions'].__len__() is existing_actions.__len__()
                except Exception as e:
                    logger.debug("Register resources : " + e.message)
                    ok_a = True

                if ok_a is False:
                    desc['actions'] = existing_actions
                    logger.debug("Problem in Actions description, check logs for more details")
                try:
                    desc.index['mixins']
                    existing_mixins = self.manager_m.verify_exist_mixins(desc['mixins'],creator)
                    ok_m = desc['mixins'].__len__() is existing_mixins.__len__()
                except Exception as e:
                        logger.debug("Register resources : " + e.message)
                        ok_m = True

                if ok_m is False:
                    desc['mixins'] = existing_mixins
                    logger.debug("Problem in Mixins description, check logs for more details")
                loc = joker.make_resource_location(creator,occi_kind_location,desc['id'])
                try:
                    desc.index['links']
                    created_links = self.register_links_implicit(desc['links'],creator,loc)
                    ok_l = created_links.__len__() is desc['links'].__len__()
                except Exception as e:
                    logger.debug("Register resources : " + e.message)
                    ok_l = True

                if ok_l is False:
                    desc['links'] = created_links
                    logger.debug("Problem in Links description, check logs for more details")


                doc_id = uuid_Generator.get_UUID()
                jData = dict()
                jData['Creator'] = creator
                jData['CreationDate'] = str(datetime.now())
                jData['LastUpdate'] = ""
                jData['OCCI_Location']= loc
                jData['OCCI_Description']= desc
                jData['Type']= "Resource"
                try:
                    database[doc_id] = jData
                    mesg = loc
                    logger.debug("Register resources : " + mesg)

                except Exception as e:
                    mesg = "An error has occurred, please check log for more details"
                    logger.error("Register resources : " + e.message)


            else:
                mesg = "Kind description and kind location don't match, please check logs for more details"
                logger.error("Register resource : " + mesg)
            loc_res.append(mesg)
        return loc_res

    def verify_exist_resource(self,resource_loc):
        """
        Verifies the existence of a resource with such resource location
        Args:
            @param resource_loc: Location of the resource
        """
        self.add_design_resource_docs_to_db()
        database = self.server.get_or_create_db(config.Resource_DB)
        query = database.view('/get_resource/by_occi_location',key = resource_loc)
        if query.count() is 0:
            return False
        else:
            return True



    def associate_resources_to_mixin(self,creator,occi_description,occi_mixin_location,occi_mixin_id):
        """
        Associate resources to mixin
        Args:
            @param creator: Issuer of the association request
            @param occi_description: Resource description
            @param occi_mixin_id: id of the mixin
            @param occi_mixin_location: location of the mixin
        """
    def register_links_implicit(self,creator,occi_descriptions,source):

        """
        Add new links to the database (Called only during the creation of a new resource instance)
        Args:
            @param creator: the user who created this new link
            @param occi_descriptions: the OCCI description of the new link
        """

        database = self.server.get_or_create_db(config.Link_DB)
        self.add_design_link_docs_to_db()
        loc_res=list()
        for desc in occi_descriptions:
            ok_k= self.manager_k.verify_exist_kind(desc['kind'])
            if ok_k is True:
                ok_t = self.verify_exist_resource(desc['target'])
                if ok_t is True:
                    existing_actions = self.manager_a.verify_exist_actions(desc['actions'],creator)
                    ok_a = existing_actions.__len__() is desc['actions'].__len__()
                    if ok_a is False:
                        logger.debug("Problem in Actions description, check logs for more details")
                        desc['actions'] = existing_actions
                    existing_mixins = self.manager_m.verify_exist_mixins(desc['mixins',creator])
                    ok_m = existing_mixins.__len__() is desc['mixins'].__len__()
                    if ok_m is False:
                        logger.debug("Problem in Mixins description, check logs for more details")
                        desc['mixins'] = existing_mixins
                    doc_id = uuid_Generator.get_UUID()
                    kind_loc = desc['kind']
                    loc = joker.make_link_location(creator,kind_loc,desc['id'])
                    jData = dict()
                    desc['source'] = source
                    jData['Creator'] = creator
                    jData['CreationDate'] = str(datetime.now())
                    jData['LastUpdate'] = ""
                    jData['OCCI_Location']= loc
                    jData['OCCI_Description']= desc
                    jData['Type']= "Link"
                    try:
                        database[doc_id] = jData
                        mesg = desc
                    except Exception as e:
                        logger.error("Implicit link : " + e.message)
                        mesg = "An error has occurred, please check logs for more details "
                else:
                    mesg = "Problem in Resources description, check logs for more details"
            else:
                mesg = "Problem in kind description, check logs for more details"

            loc_res.append(mesg)
            logger.debug(mesg)

        return loc_res

def verify_existences(occi_ids, db_occi_ids_locs):
    """
    Verifies the existence of occi_ids in db_occi_ids_locs
    """
    var_ids = list()
    for occi_ids_locs in db_occi_ids_locs:
        var_ids.append(occi_ids_locs['OCCI_ID'])
    try:
        for occi_id in occi_ids:
            var_ids.index(occi_id)
    except KeyError:
        return False

    return True

class LinkManager(object):
    """
    Manager of link documents in the couch database.
    """

    def register_links_explicit(self,creator,occi_descriptions,kind_occi_location,db_occi_ids_locs):
        """
        Add new links to database
        Args:
            @param creator: Issuer of the register request
            @param occi_descriptions: Link OCCI descriptions
            @param kind_occi_location: Location of the kind to which belong these links
            @param db_occi_ids_locs: OCCI ID and locations extracted from the database
        """

        loc_res = list()
        loc = joker.make_category_location({'location':kind_occi_location})
        kind_occi_id = None
        for elem in db_occi_ids_locs:
            if elem['OCCI_Location'] == loc:
                kind_occi_id = elem['OCCI_ID']
                break
        if kind_occi_id is not None:
            for desc in occi_descriptions:

                #Verify if the kind to which this request is sent is the same as the one in the link description
                if desc['kind'] == kind_occi_id:
                    ok_target = verify_existences([desc['target']],db_occi_ids_locs)
                    if ok_target is True:
                        ok_source = verify_existences([desc['source']],db_occi_ids_locs)
                        if ok_source is True:
                            try:
                                ok_a = verify_existences(desc['actions'],db_occi_ids_locs)
                            except KeyError as e:
                                logger.debug("Register resources : " + e.message)
                                ok_a = True
                            if ok_a is True:
                                try:
                                    ok_m = verify_existences(desc['mixins'],creator)
                                except KeyError as e:
                                    logger.debug("Register resources : " + e.message)
                                    ok_m = True

                                if ok_m is True:
                                    loc = joker.make_link_location(creator,kind_occi_location,desc['id'])
                                    jData = dict()
                                    jData['_id'] = uuid_Generator.get_UUID()
                                    jData['Creator'] = creator
                                    jData['CreationDate'] = str(datetime.now())
                                    jData['LastUpdate'] = ""
                                    jData['OCCI_Location']= loc
                                    jData['OCCI_Description']= desc
                                    jData['Type']= "Link"
                                    loc_res.append(jData)
                                else:
                                    logger.error("Reg links exp : Bad Mixins description ")
                                    return list(),return_code['Not Found']
                            else:
                                logger.error("Reg links exp : Bad Actions description ")
                                return list(),return_code['Not Found']
                        else:
                            logger.error("Reg links exp : Bad source description ")
                            return list(),return_code['Not Found']
                    else:
                        logger.error("Reg links exp : Bad target description ")
                        return list(),return_code['Not Found']
                else:
                    mesg = "Kind description and kind location don't match, please check logs for more details"
                    logger.error("Reg links exp: " + mesg)
                    return list(),return_code['Conflict']

            return loc_res,return_code['OK']

    def associate_links_to_mixin(self,creator,occi_description,occi_mixin_location,occi_mixin_id):
        """
        Associate resources to mixin
        Args:
            @param creator: Issuer of the association request
            @param occi_description: link description
            @param occi_mixin_id: id of the mixin
            @param occi_mixin_location: location of the mixin
        """


def dissociate_resource_from_mixin(occi_id):
    """
    Dissociates a resource from a mixin upon the deletion of a mixin
    Args:
        @param mix_desc: OCCI description of the mixin
    """
    return True
def get_resources_belonging_to_kind(kind_desc):
    """
    Verifies if there are resources of this kind description
    Args:
        @param kind_desc: OCCI kind description of the kind

    """
    return True



