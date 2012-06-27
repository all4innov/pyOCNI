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

    def register_resources(self,creator,occi_descriptions,occi_kind_location,db_occi_ids_locs):

        """
        Add new resources to the database
        Args:
            @param creator: the user who created these new resources
            @param occi_descriptions: the OCCI description of the new resources
            @param occi_kind_location: the kind location to which belong these new resources
            @param db_occi_ids_locs: OCCI IDs and OCCI Location extracted from the database
        """
        loc_res = list()
        loc = joker.make_category_location({'location':"/"+occi_kind_location+"/"})
        kind_occi_id = None
        for elem in db_occi_ids_locs:
            if elem['OCCI_Location'] == loc:
                kind_occi_id = elem['OCCI_ID']
                break
        if kind_occi_id is not None:
            for desc in occi_descriptions:

                #Verify if the kind to which this request is sent is the same as the one in the link description
                if desc['kind'] == kind_occi_id:
                    if desc.has_key('actions'):
                        ok_a = joker.verify_existences_delta(desc['actions'],db_occi_ids_locs)
                    else:
                        ok_a = True
                    if ok_a is True:
                        if desc.has_key('mixins'):
                            ok_m = joker.verify_existences_beta(desc['mixins'],db_occi_ids_locs)
                        else:
                            ok_m = True
                        if ok_m is True:
                            if desc.has_key('links'):
                                ok_l,exist_links = self.verify_links_implicit(desc['links'],creator,db_occi_ids_locs)
                            else:
                                ok_l = True
                                exist_links = False
                            if ok_l is True:
                                loc = joker.make_entity_location(creator,occi_kind_location,desc['id'])
                                exist_same = joker.verify_existences_teta([loc],db_occi_ids_locs)
                                if exist_same is False:
                                    jData = dict()
                                    jData['_id'] = uuid_Generator.get_UUID()
                                    jData['Creator'] = creator
                                    jData['CreationDate'] = str(datetime.now())
                                    jData['LastUpdate'] = ""
                                    jData['OCCI_Location']= loc
                                    jData['OCCI_Description']= desc
                                    jData['Type']= "Resource"
                                    jData['Internal_Links'] = exist_links
                                    loc_res.append(jData)
                                else:
                                    logger.error("Reg resource exp : Bad Resource id ")
                                    return list(),return_code['Conflict']
                            else:
                                logger.error("Reg resources exp : Bad links description ")
                                return list(),exist_links
                        else:
                            logger.error("Reg resources exp : Bad Mixins description ")
                            return list(),return_code['Not Found']
                    else:
                        logger.error("Reg resources exp : Bad Actions description ")
                        return list(),return_code['Not Found']
                else:
                    mesg = "Kind description and kind location don't match"
                    logger.error("Reg resources exp: " + mesg)
                    return list(),return_code['Conflict']
            logger.debug("Reg resouces exp: Resources sent for creation")
            return loc_res,return_code['OK']
        else:
            mesg = "No kind corresponding to this location was found"
            logger.error("Reg resources exp: " + mesg)
            return list(),return_code['Not Found']

    def associate_resources_to_mixin(self,creator,occi_description,occi_mixin_location,occi_mixin_id):
        """
        Associate resources to mixin
        Args:
            @param creator: Issuer of the association request
            @param occi_description: Resource description
            @param occi_mixin_id: id of the mixin
            @param occi_mixin_location: location of the mixin
        """
    def verify_links_implicit(self,occi_descriptions,creator,db_occi_ids_locs):
        """
        Checks the integrity of internal resource links (Called only during the creation of a new resource instance)
        Args:

            @param occi_descriptions: the OCCI descriptions of new links
            @param creator: Issuer of the request
            @param db_occi_ids_locs: OCCI IDs and locations contained in the database
        """

        for desc in occi_descriptions:
            ok_k = joker.verify_existences_beta([desc['kind']],db_occi_ids_locs)
            #Verify if the kind to which this request is sent is the same as the one in the link description
            if ok_k is True:
                ok_target = joker.verify_existences_teta([desc['target']],db_occi_ids_locs)
                if ok_target is True:
                    if desc.has_key('actions'):
                        ok_a = joker.verify_existences_delta(desc['actions'],db_occi_ids_locs)
                    else:
                        ok_a = True
                    if ok_a is True:
                        if desc.has_key('mixins'):
                            ok_m = joker.verify_existences_beta(desc['mixins'],db_occi_ids_locs)
                        else:
                            ok_m = True
                        if ok_m is True:
                            exist_same = joker.verify_existences_kappa(desc['id'],desc['kind'],creator,db_occi_ids_locs)
                            if exist_same is True:
                                logger.error("Reg links impl : Bad link id ")
                                return False,return_code['Conflict']
                        else:
                            logger.error("Reg links impl : Bad Mixins description ")
                            return False,return_code['Not Found']
                    else:
                        logger.error("Reg links impl : Bad Actions description ")
                        return False,return_code['Not Found']
                else:
                    logger.error("Reg links impl : Bad target description ")
                    return False,return_code['Not Found']
            else:
                mesg = "Kind description does not exist"
                logger.error("Reg links impl: " + mesg)
                return False,return_code['Not Found']
        logger.debug("Internal links validated with success")
        return True,True

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
        loc = joker.make_category_location({'location':"/" + kind_occi_location + "/"})
        kind_occi_id = None
        for elem in db_occi_ids_locs:
            if elem['OCCI_Location'] == loc:
                kind_occi_id = elem['OCCI_ID']
                break
        if kind_occi_id is not None:
            for desc in occi_descriptions:

                #Verify if the kind to which this request is sent is the same as the one in the link description
                if desc['kind'] == kind_occi_id:
                    ok_target = joker.verify_existences_teta([desc['target']],db_occi_ids_locs)
                    if ok_target is True:
                        ok_source = joker.verify_existences_teta([desc['source']],db_occi_ids_locs)
                        if ok_source is True:
                            if desc.has_key('actions'):
                                ok_a = joker.verify_existences_delta(desc['actions'],db_occi_ids_locs)
                            else:
                                ok_a = True
                            if ok_a is True:
                                if desc.has_key('mixins'):
                                    ok_m = joker.verify_existences_beta(desc['mixins'],db_occi_ids_locs)
                                else:
                                    ok_m = True
                                if ok_m is True:
                                    loc = joker.make_entity_location(creator,kind_occi_location,desc['id'])
                                    exist_same = joker.verify_existences_teta([loc],db_occi_ids_locs)
                                    if exist_same is False:
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
                                        logger.error("Reg links exp : Bad Link id ")
                                        return list(),return_code['Conflict']
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
                    mesg = "Kind description and kind location don't match"
                    logger.error("Reg links exp: " + mesg)
                    return list(),return_code['Conflict']
            logger.debug("Reg links exp: links sent for creation")
            return loc_res,return_code['OK']
        else:
            mesg = "No kind corresponding to this location was found"
            logger.error("Reg links exp: " + mesg)
            return list(),return_code['Not Found']


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



