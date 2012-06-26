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
Created on May 29, 2012

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
from datetime import datetime
from pyocni.pyocni_tools import uuid_Generator
from couchdbkit import *
from pyocni.pyocni_tools.config import return_code
# getting the Logger
logger = config.logger

class KindManager:
    """

        Manager for Kind documents on couch database

    """

    def get_filtered_kinds(self,jfilters,db_kinds):
        """
        Returns kind documents matching the filter provided
        Args:
            @param jfilters: description of the kind document to retrieve
            @param db_kinds: Kind descriptions that already exist in database
            @return : <list> OCCI kind description contained inside of the kind document
        """
        var = list()
        #Extract kind descriptions from the dictionary
        try:
            for elem in db_kinds:
                for jfilter in jfilters:
                    ok = joker.filter_occi_description(elem,jfilter)
                    if ok is True:
                        var.append(elem)
                        logger.debug("Kind filtered document found")
                    else:
                        message = "No kind document matches the requirements"
                        logger.debug(message)
            return var,return_code['OK']
        except Exception as e:
            logger.error("filtered kinds : " + e.message)
            return "An error has occurred",return_code['Internal Server Error']


    def register_kinds(self,creator,descriptions,db_occi_ids,db_occi_locs):

        """
        Add new kinds to the database
        Args:
            @param creator: the id of the issuer of the creation request
            @param descriptions: OCCI kind descriptions
            @param db_occi_ids: Kind IDs already existing in the database
            @param db_occi_locs: Kind locations already existing in the database
        """
        loc_res = list()
        resp_code = return_code['OK']
        for desc in descriptions:
            occi_id = joker.get_description_id(desc)
            ok_k = joker.verify_occi_uniqueness(occi_id,db_occi_ids)
            if ok_k is True:
                occi_loc = joker.make_category_location(desc)
                ok_loc = joker.verify_occi_uniqueness(occi_loc,db_occi_locs)
                if ok_loc is True:
                    ok_r = joker.verify_exist_relaters(desc,db_occi_ids)
                    if ok_r is True:
                        ok_a = joker.verify_exist_actions(desc,db_occi_ids)
                        if ok_a is True:
                            jData = dict()
                            jData['_id'] = uuid_Generator.get_UUID()
                            jData['Creator'] = creator
                            jData['CreationDate'] = str(datetime.now())
                            jData['LastUpdate'] = ""
                            jData['OCCI_Location']= occi_loc
                            jData['OCCI_Description']= desc
                            jData['OCCI_ID'] = occi_id
                            jData['Type']= "Kind"
                            jData['Provider']= {"local":[],"remote":[]}
                            loc_res.append(jData)
                        else:
                            message = "Missing action description, Kind will not be created."
                            logger.error("Register kind : " + message)
                            resp_code = return_code['Not Found']
                            return list(),resp_code
                    else:
                        message = "Missing related kind description, Kind will not be created."
                        logger.error("Register kind : " + message)
                        resp_code = return_code['Not Found']
                        return list(),resp_code
                else:
                    message = "Location conflict, kind will not be created."
                    logger.error("Register kind : " + message)
                    resp_code = return_code['Conflict']
                    return list(),resp_code
            else:
                message = "This kind description already exists in document "
                logger.error("Register kind : " + message)
                resp_code = return_code['Conflict']
                return list(),resp_code

        return loc_res,resp_code


    def update_OCCI_kind_descriptions(self,user_id,new_data,db_data):
        """
        Updates the OCCI description field of the kind which document OCCI_ID is equal to OCCI_ID contained in data
        (Can only be done by the creator of the kind document)
        Args:
            @param user_id: ID of the creator of the kind document
            @param new_data: Data containing the OCCI ID of the kind and the new OCCI kind description
            @param db_data: Categories already contained in the database

        """
        to_update = list()
        resp_code = return_code['OK']
        for desc in new_data:
            occi_id = joker.get_description_id(desc)
            old_doc = joker.extract_doc(occi_id,db_data)
            if old_doc is not None:
                if user_id == old_doc['Creator']:
                    problems,occi_description= joker.update_occi_description(old_doc['OCCI_Description'],desc)
                    if problems is True:
                        message = "Kind OCCI description " + occi_id + " has not been totally updated."
                        logger.error("Kind OCCI description update " + message)
                        return list(),return_code['Bad Request']
                    else:
                        message = "Kind OCCI description " + occi_id + " has been updated successfully"
                        old_doc['OCCI_Description'] = occi_description
                        old_doc['LastUpdate'] = str(datetime.now())
                        to_update.append(old_doc)
                        logger.debug("Update kind OCCI description : " + message)
                else:
                        message = "You have no right to update this kind document " + occi_id
                        logger.error("Update kind OCCI des : " + message)
                        return list(),return_code['Forbidden']
            else:
                message = "Kind document " + occi_id + " couldn\'t be found "
                logger.error("Update kind OCCI des : " + message)
                return list(),return_code['Not Found']
        return to_update,resp_code

    def update_kind_providers(self,user_id,new_data,db_data):
        """
        Updates the provider field of the kind which document OCCI_ID is equal to OCCI_ID contained in data
        (Can only be done by the creator of the kind document)
        Args:
            @param user_id: ID of the creator of the kind document
            @param new_data: Data containing the OCCI ID of the kind and the new kind provider description
            @param db_data: Categories already contained in the database

        """
        to_update = list()
        resp_code = return_code['OK']
        for desc in new_data:
            occi_id = desc['OCCI_ID']
            old_doc = joker.extract_doc(occi_id,db_data)
            if old_doc is not None:
                if user_id == old_doc['Creator']:
                    provider_description,problems= doc_Joker.update_kind_provider(old_doc['Provider'],desc['Provider'])
                    if problems is True:
                        message = "Kind provider description " + occi_id + " has not been totally updated."
                        logger.error("Kind provider description update " + message)
                        return list(),return_code['Bad Request']
                    else:
                        message = "Kind provider description " + occi_id + " has been updated successfully"
                        old_doc['Provider'] = provider_description
                        old_doc['LastUpdate'] = str(datetime.now())
                        to_update.append(old_doc)
                        logger.debug("Update kind provider description : " + message)
                else:
                    message = "You have no right to update this kind document " + occi_id
                    logger.error("Update kind provider des : " + message)
                    return list(),return_code['Forbidden']
            else:
                message = "Kind document " + occi_id + " couldn\'t be found "
                logger.error("Update kind provider des : " + message)
                return list(),return_code['Not Found']
        return to_update,resp_code


    def delete_kind_documents(self,descriptions,user_id,db_categories,db_entities):
        """
        Delete kind documents that is related to the scheme + term contained in the description provided
        Args:
            @param descriptions: OCCI description of the kind document to delete
            @param user_id: id of the issuer of the delete request
            @param db_categories: Category data already contained in the database
            @param db_entities: Entity data already contained in the database
        """

        message = list()
        res_code = return_code['OK']
        #Verify the existence of such kind document
        for desc in descriptions:
            occi_id = joker.get_description_id(desc)
            kind_id_rev = joker.verify_exist_occi_id_creator(occi_id,user_id,db_categories)
            if kind_id_rev is not None:
                ok = self.get_entities_belonging_to_kind(occi_id,db_entities)
                if ok is True:
                    message.append(kind_id_rev)
                    event = "Kind document " + occi_id + " is sent for delete "
                    logger.debug("Delete kind : " + event)
                else:
                    event = "Unable to delete because this kind document " + occi_id + " has resources depending on it. "
                    logger.error("Delete kind : " + event)
                    return list(), return_code['Bad Request']
            else:
                event = "Could not find this kind document " + occi_id +" or you are not authorized for for delete"
                logger.error("Delete kind : " + event)
                return list(), return_code['Bad Request']
        return message,res_code

    def get_entities_belonging_to_kind(self, occi_id,db_data):
        return True



class MixinManager:
    """

        Manager for Mixin documents on couch database

    """


    def get_filtered_mixins(self,jfilters,db_mixins):
        """
        Returns mixin documents matching the filter provided
        Args:
            @param jfilters: description of the mixin document to retrieve
            @param db_mixins: mixin descriptions that already exist in database
            @return : <list> OCCI mixin description contained inside of the mixin document
        """
        var = list()
        #Extract mixins descriptions from the dictionary
        try:
            for elem in db_mixins:
                for jfilter in jfilters:
                    ok = joker.filter_occi_description(elem,jfilter)
                    if ok is True:
                        var.append(elem)
                        logger.debug("Mixin filtered document found")
                    else:
                        message = "No mixin document matches the requirements"
                        logger.debug(message)
            return var,return_code['OK']
        except Exception as e:
            logger.error("filtered mixins : " + e.message)
            return "An error has occurred",return_code['Internal Server Error']


    def register_mixins(self,creator,descriptions,db_occi_ids,db_occi_locs):

        """
        Add new mixins to the database
        Args:
            @param creator: the id of the issuer of the creation request
            @param descriptions: OCCI mixin descriptions
            @param db_occi_ids: Existing Mixin IDs in database
            @param db_occi_locs: Existing Mixin locations in database
        """
        loc_res = list()
        resp_code = return_code['OK']
        for desc in descriptions:
            occi_id = joker.get_description_id(desc)
            ok_k = joker.verify_occi_uniqueness(occi_id,db_occi_ids)
            if ok_k is True:
                occi_loc = joker.make_category_location(desc)
                ok_loc = joker.verify_occi_uniqueness(occi_loc,db_occi_locs)
                if ok_loc is True:
                    ok_r = joker.verify_exist_relaters(desc,db_occi_ids)
                    if ok_r is True:
                        ok_a = joker.verify_exist_actions(desc,db_occi_ids)
                        if ok_a is True:
                            jData = dict()
                            jData['_id'] = uuid_Generator.get_UUID()
                            jData['Creator'] = creator
                            jData['CreationDate'] = str(datetime.now())
                            jData['LastUpdate'] = ""
                            jData['OCCI_Location']= occi_loc
                            jData['OCCI_Description']= desc
                            jData['OCCI_ID'] = occi_id
                            jData['Type']= "Mixin"
                            loc_res.append(jData)
                        else:
                            message = "Missing action description, Mixin will not be created."
                            logger.error("Register Mixin : " + message)
                            resp_code = return_code['Not Found']
                            return list(),resp_code
                    else:
                        message = "Missing related Mixin description, Mixin will not be created."
                        logger.error("Register Mixin : " + message)
                        resp_code = return_code['Not Found']
                        return list(),resp_code
                else:
                    message = "Location conflict, Mixin will not be created."
                    logger.error("Register Mixin : " + message)
                    resp_code = return_code['Conflict']
                    return list(),resp_code
            else:
                message = "This Mixin description already exists in document."
                logger.error("Register Mixin : " + message)
                resp_code = return_code['Conflict']
                return list(),resp_code

        return loc_res,resp_code

    def update_OCCI_mixin_descriptions(self,user_id,new_data,db_data):
        """
        Updates the OCCI description field of the mixin which document OCCI_ID is equal to OCCI_ID contained in data
        (Can only be done by the creator of the mixin document)
        Args:
            @param user_id: ID of the creator of the mixin document
            @param new_data: Data containing the OCCI ID of the mixin and the new OCCI mixin description
            @param db_data: Data already contained in the database
            @return : <string>, return_code
        """
        to_update = list()
        resp_code = return_code['OK']
        for desc in new_data:
            occi_id = joker.get_description_id(desc)
            old_doc = joker.extract_doc(occi_id,db_data)
            if old_doc is not None:
                if user_id == old_doc['Creator']:
                    problems,occi_description= joker.update_occi_description(old_doc['OCCI_Description'],desc)
                    if problems is True:
                        message = "Mixin OCCI description " + occi_id + " has not been totally updated."
                        logger.error("Mixin OCCI description update " + message)
                        return list(),return_code['Bad Request']
                    else:
                        message = "Mixin OCCI description " + occi_id + " has been updated successfully"
                        old_doc['OCCI_Description'] = occi_description
                        old_doc['LastUpdate'] = str(datetime.now())
                        to_update.append(old_doc)
                        logger.debug("Update Mixin OCCI description : " + message)
                else:
                    message = "You have no right to update this Mixin document " + occi_id
                    logger.error("Update Mixin OCCI des : " + message)
                    return list(),return_code['Forbidden']
            else:
                message = "Mixin document " + occi_id + " couldn\'t be found "
                logger.error("Update Mixin OCCI des : " + message)
                return list(),return_code['Not Found']
        return to_update,resp_code

    def delete_mixin_documents(self,descriptions,user_id,db_categories,db_entities):
        """
        Delete mixin documents that is related to the scheme + term contained in the description provided
        Args:
            @param descriptions: OCCI description of the mixin document to delete
            @param user_id: id of the issuer of the delete request
            @param db_categories: Category data already contained in the database
            @param db_entities: Entity data already contained in the database
        """

        message = list()
        res_code = return_code['OK']
        #Verify the existence of such kind document
        for desc in descriptions:
            occi_id = joker.get_description_id(desc)
            mixin_id_rev = joker.verify_exist_occi_id_creator(occi_id,user_id,db_categories)
            if mixin_id_rev is not None:
                ok = self.dissociate_entities_belonging_to_mixin(occi_id,db_entities)
                if ok is True:
                    message.append(mixin_id_rev)
                    event = "Mixin document " + occi_id + " is sent for delete "
                    logger.debug("Delete mixin : " + event)
                else:
                    event = "Unable to delete because this mixin document " + occi_id + " has resources depending on it. "
                    logger.error("Delete mixin : " + event)
                    return list(), return_code['Bad Request']
            else:
                event = "Could not find this mixin document " + occi_id +" or you are not authorized for for delete"
                logger.error("Delete mixin : " + event)
                return list(), return_code['Bad Request']
        return message,res_code
    def dissociate_entities_belonging_to_mixin(self, occi_id, db_entities):
        return True


class ActionManager:
    """

        Manager for Action documents on couch database

    """

    def get_filtered_actions(self,jfilters,db_actions):
        """
        Returns action documents matching the filter provided
        Args:
            @param jfilters: description of the action document to retrieve
            @param db_actions: action descriptions that already exist in database
            @return : <list> OCCI action description contained inside of the action document
        """
        var = list()
        #Extract action descriptions from the dictionary
        try:
            for elem in db_actions:
                for jfilter in jfilters:
                    ok = joker.filter_occi_description(elem,jfilter)
                    if ok is True:
                        var.append(elem)
                        logger.debug("action filtered document found")
                    else:
                        message = "No action document matches the requirements"
                        logger.debug(message)
            return var,return_code['OK']
        except Exception as e:
            logger.error("filtered actions : " + e.message)
            return "An error has occurred",return_code['Internal Server Error']

    def register_actions(self,creator,descriptions,db_actions):

        """
        Add new actions to the database
        Args:
            @param creator: the id of the issuer of the creation request
            @param descriptions: OCCI action descriptions
            @param db_actions: Existing actions in database
        """
        loc_res = list()
        resp_code = return_code['OK']
        for desc in descriptions:
            occi_id = joker.get_description_id(desc)
            ok_k = joker.verify_occi_uniqueness(occi_id,db_actions)
            if ok_k is True:
                jData = dict()
                jData['_id'] = uuid_Generator.get_UUID()
                jData['Creator'] = creator
                jData['CreationDate'] = str(datetime.now())
                jData['LastUpdate'] = ""
                jData['OCCI_Description']= desc
                jData['OCCI_ID'] = occi_id
                jData['Type']= "Action"
                loc_res.append(jData)
            else:
                message = "This Action description already exists in document. "
                logger.error("Register Action : " + message)
                resp_code = return_code['Conflict']
                return list(),resp_code
        return loc_res,resp_code



    def update_OCCI_action_descriptions(self,user_id,new_data,db_data):
        """
        Updates the OCCI description field of the action which document OCCI_ID is equal to OCCI_ID contained in data
        (Can only be done by the creator of the action document)
        Args:
            @param user_id: ID of the creator of the action document
            @param new_data: Data containing the OCCI ID of the action and the new OCCI action description
            @param db_data: Data already contained in the database
            @return : <string>, return_code
        """
        to_update = list()
        resp_code = return_code['OK']
        for desc in new_data:
            occi_id = joker.get_description_id(desc)
            old_doc = joker.extract_doc(occi_id,db_data)
            if old_doc is not None:
                if user_id == old_doc['Creator']:
                    problems,occi_description= joker.update_occi_description(old_doc['OCCI_Description'],desc)
                    if problems is True:
                        message = "Action OCCI description " + occi_id + " has not been totally updated."
                        logger.error("Action OCCI description update " + message)
                        return list(),return_code['Bad Request']
                    else:
                        message = "Action OCCI description " + occi_id + " has been updated successfully"
                        old_doc['OCCI_Description'] = occi_description
                        old_doc['LastUpdate'] = str(datetime.now())
                        to_update.append(old_doc)
                        logger.debug("Update Action OCCI description : " + message)
                else:
                    message = "You have no right to update this Action document " + occi_id
                    logger.error("Update Action OCCI des : " + message)
                    return list(),return_code['Forbidden']
            else:
                message = "Action document " + occi_id + " couldn\'t be found "
                logger.error("Update Action OCCI des : " + message)
                return list(),return_code['Not Found']
        return to_update,resp_code

    def delete_action_documents(self,descriptions,user_id,db_categories):
        """
        Delete action documents that is related to the scheme + term contained in the description provided
        Args:
            @param descriptions: OCCI description of the action document to delete
            @param user_id: id of the issuer of the delete request
            @param db_categories: Category data already contained in the database
        """

        message = list()
        res_code = return_code['OK']
        #Verify the existence of such action document
        for desc in descriptions:
            occi_id = joker.get_description_id(desc)
            action_id_rev = joker.verify_exist_occi_id_creator(occi_id,user_id,db_categories)
            if action_id_rev is not None:
                message.append(action_id_rev)
                event = "Action document " + occi_id + " is sent for delete "
                logger.debug("Delete action : " + event)
            else:
                event = "Could not find this action document " + occi_id +" or you are not authorized for for delete"
                logger.error("Delete action : " + event)
                return list(), return_code['Bad Request']
        return message,res_code


class CategoryManager:
    """

        Channel requests to their appropriate targets : Kinds, Mixins and Actions

    """

    def __init__(self):

        self.manager_k = KindManager()
        self.manager_m = MixinManager()
        self.manager_a = ActionManager()


    def channel_register_categories(self,user_id,jreq):
        """
        Channel the post request to the right methods
        Args:
            @param user_id: ID of the issuer of the post request
            @param jreq: Body content of the post request

        """
        database = config.prepare_PyOCNI_db()
        query = database.view('/get_views/occi_id_occi_location')
        db_occi_ids = list()
        db_occi_locs = list()
        for q in query:
            db_occi_ids.append( q['key'])
            db_occi_locs.append(q['value'])
        data_keys = jreq.keys()
        try:
            data_keys.index('actions')
            logger.debug("Actions post request : channeled")
            new_actions,resp_code_a = self.manager_a.register_actions(user_id,jreq['actions'],db_occi_ids)
        except Exception as e:
            logger.error("ch register categories : " + e.message)
            new_actions = list()
            resp_code_a = return_code['OK']

        try:
            data_keys.index('kinds')
            logger.debug("Kinds post request : channeled")
            new_kinds,resp_code_k = self.manager_k.register_kinds(user_id,jreq['kinds'],db_occi_ids,db_occi_locs)
        except Exception as e:
            logger.error("ch register categories : " + e.message)
            new_kinds = list()
            resp_code_k = return_code['OK']

        try:
            data_keys.index('mixins')
            logger.debug("Mixins post request : channeled")
            new_mixins,resp_code_m = self.manager_m.register_mixins(user_id,jreq['mixins'],db_occi_ids,db_occi_locs)
        except Exception as e:
            logger.error("ch register categories : " + e.message)
            new_mixins= list()
            resp_code_m = return_code['OK']

        if resp_code_a is not 200 or resp_code_k is not 200 or resp_code_m is not 200:
            return "An error has occurred, please check log for more details",return_code['Bad Request']

        categories = new_kinds + new_mixins + new_actions
        database.save_docs(categories,use_uuids=True, all_or_nothing=True)
        return "",return_code['OK']

    def channel_get_all_categories(self):
        """
        Retrieve all categories to show the server's capacity

        """
        database = config.prepare_PyOCNI_db()
        db_kinds = list()
        db_mixins = list()
        db_actions = list()
        try:
            query = database.view('/get_views/type_occi_desc')
        except Exception as e:
            logger.error("Category get all : " + e.message)
            return ["An error has occurred, please check log for more details"],return_code['Internal Server Error']

        for q in query:
            if q['key'] == "Kind":
                db_kinds.append(q['value'])
            elif q['key'] == "Mixin":
                db_mixins.append(q['value'])
            elif q['key'] == "Action":
                db_actions.append(q['value'])

        result = {'kinds': db_kinds, 'mixins': db_mixins, 'actions': db_actions}

        return result,return_code['OK']

    def channel_get_filtered_categories(self,jreq):
        """
        Channel the post request to the right methods
        Args:
            @param jreq: Body content of the post request

        """
        database = config.prepare_PyOCNI_db()
        db_kinds = list()
        db_mixins = list()
        db_actions = list()
        try:
            query = database.view('/get_views/type_occi_desc')
        except Exception as e:
            logger.error("Category get all : " + e.message)
            return ["An error has occurred, please check log for more details"],return_code['Internal Server Error']

        for q in query:
            if q['key'] == "Kind":
                db_kinds.append(q['value'])
            elif q['key'] == "Mixin":
                db_mixins.append(q['value'])
            elif q['key'] == "Action":
                db_actions.append(q['value'])

        data_keys = jreq.keys()
        try:
            data_keys.index('kinds')
            logger.debug("Kinds filter get request : channeled")
            filtred_kinds,resp_code_k = self.manager_k.get_filtered_kinds(jreq['kinds'],db_kinds)
        except Exception as e:
            logger.debug("ch get filter : " + e.message)
            filtred_kinds = ""
            resp_code_k = return_code['OK']

        try:
            data_keys.index('mixins')
            logger.debug("Mixins filter get request : channeled")
            filtred_mixins,resp_code_m = self.manager_m.get_filtered_mixins(jreq['mixins'],db_mixins)
        except Exception as e:
            logger.debug("ch get filter : " + e.message)
            filtred_mixins = ""
            resp_code_m = return_code['OK']

        try:
            data_keys.index('actions')
            logger.debug("Actions filter get : channeled")
            filtred_actions,resp_code_a = self.manager_a.get_filtered_actions(jreq['actions'],db_actions)
        except Exception as e:
            logger.debug("ch get filter : " + e.message)
            filtred_actions = ""
            resp_code_a = return_code['OK']

        if resp_code_a is not 200 or resp_code_k is not 200 or resp_code_m is not 200:
            return "An error has occurred, please check log for more details",return_code['Bad Request']
        result = {'kinds': filtred_kinds, 'mixins': filtred_mixins, 'actions': filtred_actions}
        return result,return_code['OK']

    def channel_delete_categories(self,jreq,user_id):
        """
        Channel the delete request to the right methods
        Args:
            @param user_id: ID of the issuer of the post request
            @param jreq: Body content of the post request

        """
        database = config.prepare_PyOCNI_db()
        try:
            query = database.view('/get_views/_id_rev_occi_id_creator')
        except Exception as e:
            logger.error("Category delete : " + e.message)
            return ["An error has occurred, please check log for more details"],return_code['Internal Server Error']
        db_occi_id_creator = list()
        for q in query:
            db_occi_id_creator.append( { "_id" : q['key'],"_rev" : q['value'][0], "OCCI_ID" : q['value'][1],"Creator" : q['value'][2]})

        try:
            query = database.view('/get_views/type_occi_desc')
        except Exception as e:
            logger.error("Category delete : " + e.message)
            return "An error has occurred, please check log for more details",return_code['Internal Server Error']

        db_entities = list()
        for q in query:
            if q['key'] == "Link" or q['key'] == "Resource":
                db_entities.append(q['value'])

        data_keys = jreq.keys()
        try:
            data_keys.index('kinds')
            logger.debug("Kinds delete request : channeled")
            delete_kinds,resp_code_k = self.manager_k.delete_kind_documents(jreq['kinds'],user_id,db_occi_id_creator,db_entities)
        except Exception as e:
            logger.error("ch delete filter : " +e.message)
            delete_kinds=list()
            resp_code_k = return_code['OK']

        try:
            data_keys.index('mixins')
            logger.debug("Mixins delete request : channeled")
            delete_mixins,resp_code_m = self.manager_m.delete_mixin_documents(jreq['mixins'],user_id,db_occi_id_creator,db_entities)
        except Exception as e:
            logger.error("ch delete filter : " +e.message)
            delete_mixins=list()
            resp_code_m = return_code['OK']

        try:
            data_keys.index('actions')
            logger.debug("Actions delete request : channeled")
            delete_actions,resp_code_a = self.manager_a.delete_action_documents(jreq['actions'],user_id,db_occi_id_creator)
        except Exception as e:
            logger.error("ch delete filter : " +e.message)
            delete_actions = list()
            resp_code_a = return_code['OK']

        if resp_code_a is not 200 or resp_code_k is not 200 or resp_code_m is not 200:
            return "An error has occurred, please check log for more details",return_code['Bad Request']

        categories = delete_kinds + delete_mixins + delete_actions

        database.delete_docs(categories)
        return "",return_code['OK']


    def channel_update_categories(self,user_id,j_newData):
        """
        Channel the PUT requests to their right methods
        Args:
            @param user_id: ID of the issuer of the post request
            @param j_newData: Body content of the post request
        """
        database = config.prepare_PyOCNI_db()
        try:
            query = database.view('/get_views/occi_id_doc')
        except Exception as e:
            logger.error("Category delete : " + e.message)
            return "An error has occurred, please check log for more details",return_code['Internal Server Error']
        db_occi_id_doc = list()
        for q in query:
            db_occi_id_doc.append( { "OCCI_ID" : q['key'],"Doc" : q['value']})

        data_keys = j_newData.keys()
        try:
            data_keys.index('actions')
            logger.debug("Actions put request : channeled")
            updated_actions,resp_code_a = self.manager_a.update_OCCI_action_descriptions(user_id,j_newData['actions'],db_occi_id_doc)
        except Exception as e:
            logger.error("ch update categories : " + e.message)
            updated_actions=list()
            resp_code_a = return_code['OK']

        try:
            data_keys.index('kinds')
            logger.debug("Kinds put request : channeled")
            updated_kinds,resp_code_k = self.manager_k.update_OCCI_kind_descriptions(user_id,j_newData['kinds'],db_occi_id_doc)
        except Exception as e:
            logger.error("ch update categories : " + e.message)
            updated_kinds = list()
            resp_code_k = return_code['OK']
        try:
            data_keys.index('providers')
            logger.debug("Providers put request : channeled")
            updated_providers,resp_code_p = self.manager_k.update_kind_providers(user_id,j_newData['providers'],db_occi_id_doc)
        except Exception as e:
            logger.error("ch update categories : " + e.message)
            updated_providers=list()
            resp_code_p = return_code['OK']

        try:
            data_keys.index('mixins')
            logger.debug("Mixins put request : channeled")
            updated_mixins,resp_code_m = self.manager_m.update_OCCI_mixin_descriptions(user_id,j_newData['mixins'],db_occi_id_doc)
        except Exception as e:
            logger.error("ch update categories : " + e.message)
            updated_mixins = list()
            resp_code_m = return_code['OK']


        if resp_code_a is not 200 or resp_code_k is not 200 or resp_code_m is not 200 or resp_code_p is not 200:
            return "An error has occurred, please check log for more details",return_code['Bad Request']

        categories = updated_kinds + updated_providers + updated_mixins + updated_actions
        database.save_docs(categories,force_update=True, all_or_nothing=True)
        return "",return_code['OK']
