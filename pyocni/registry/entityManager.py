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
try:
    import simplejson as json
except ImportError:
    import json
from datetime import datetime
from pyocni.pyocni_tools import uuid_Generator
from pyocni.pyocni_tools.config import return_code

# getting the Logger
logger = config.logger

#=======================================================================================================================
#                                           ResourceManager
#=======================================================================================================================

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

#=======================================================================================================================
#                                           LinkManager
#=======================================================================================================================

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

#=======================================================================================================================
#                                           MultiEntityManager
#=======================================================================================================================

class MultiEntityManager(object):
    """

    """

    def __init__(self):

        self.manager_r = ResourceManager()
        self.manager_l = LinkManager()

    def channel_post_multi(self,user_id,jreq,location):
        """
        Identifies the post path's goal : create a resource instance or update a mixin
        Args:
            @param user_id: ID of the issuer of the post request
            @param jreq: Body content of the post request
            @param location: Address to which this post request was sent
        """
        database = config.prepare_PyOCNI_db()

        if jreq.has_key('resources') or jreq.has_key('links'):
            is_kind_loc = True
        else:
            is_kind_loc = False

        if is_kind_loc is True:
            try:
                query = database.view('/get_views/occi_id_occi_location')
            except Exception as e:
                logger.error("Category delete : " + e.message)
                return "An error has occurred, please check log for more details",return_code['Internal Server Error']
            db_occi_ids_locs = list()
            for q in query:
                db_occi_ids_locs.append({"OCCI_ID" : q['key'],"OCCI_Location":q['value']})

            if jreq.has_key('resources'):
                logger.debug("Post path : Post on kind path to create a new resource channeled")
                new_resources, resp_code_r = self.manager_r.register_resources(user_id,jreq['resources'],location,db_occi_ids_locs)
            else:
                new_resources = list()
                resp_code_r = return_code['OK']

            if jreq.has_key('links'):
                logger.debug("Post path : Post on kind path to create a new link channeled")
                new_links, resp_code_l = self.manager_l.register_links_explicit(user_id,jreq['links'],location,db_occi_ids_locs)
            else:
                new_links = list()
                resp_code_l = return_code['OK']

            if resp_code_r is not return_code['OK'] or resp_code_l is not return_code['OK']:
                return "An error has occurred, please check log for more details",return_code['Bad Request']

            entities = new_resources + new_links
            database.save_docs(entities,use_uuids=True, all_or_nothing=True)
            #return the locations of the resources
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

            if jreq.has_key('OCCI_Locations'):
                logger.debug("Post path : Post on kind path to associate a mixin channeled")
                updated_entities,resp_code_e = associate_entities_to_a_mixin(jreq['OCCI_Locations'],location,db_occi_locs_docs)
            else:
                updated_entities = list()
                resp_code_e = return_code['OK']

            if resp_code_e is not return_code['OK']:
                return "An error has occurred, please check log for more details",return_code['Bad Request']

            database.save_docs(updated_entities,force_update=True,all_or_nothing=True)
            return "",return_code['OK']

#=======================================================================================================================
#                                           SingleEntityManager
#=======================================================================================================================

class SingleEntityManager(object):
    """

    """

    def __init__(self):

        self.manager_r = ResourceManager()
        self.manager_l = LinkManager()

#=======================================================================================================================
#                                           Independant Functions
#=======================================================================================================================

def associate_entities_to_a_mixin(entities_locations, location, db_occi_ids_docs):
    """
    Add a single mixin to entities
    Args:
        @param entities_locations: OCCI Location of the entities
        @param location: location of the mixin
        @param db_occi_ids_docs: OCCI IDs and documents of the entities already contained in the database
    """
    #Get the Mixin's OCCI_ID
    mix_loc = joker.make_category_location({"location":"/"+location+"/"})
    mix_id = None
    to_update = list()
    for item in db_occi_ids_docs:
        if item['OCCI_Location'] == mix_loc and item['Doc']['Type'] == "Mixin":
            mix_id = item['Doc']['OCCI_ID']
        else:
            try:
                entities_locations.index(item['OCCI_Location'])
                if item['Doc']['Type'] == 'Resource' or item['Doc']['Type'] == 'Link':
                    to_update.append(item['Doc'])
            except ValueError:
                pass
    if mix_id is not None:
        for doc in to_update:
            if doc['OCCI_Description'].has_key('mixins'):
                try:
                    var = doc['OCCI_Description']['mixins']
                    var.index(mix_id)
                except ValueError:
                    var.append(mix_id)
                    doc['OCCI_Description']['mixins'] = var
            else:
                doc['OCCI_Description']['mixins'] = [mix_id]
        return to_update,return_code['OK']
    else:
        return list(),return_code['Not Found']



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