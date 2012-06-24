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


# Get the database server configuration

DB_server_IP = config.DB_IP
DB_server_PORT = config.DB_PORT


def purgeCategoryDBs():

    try:
        server = Server('http://' + str(DB_server_IP) + ':' + str(DB_server_PORT))
    except Exception:
        logger.error("Database is unreachable")

    try:
        server.get_db(config.Kind_DB).flush()
    except Exception:
        logger.debug("No DB named: '" + config.Kind_DB + "' to delete.")
        server.create_db(config.Kind_DB)
    try:
        server.get_db(config.Action_DB).flush()
    except Exception:
        logger.debug("No DB named: '" + config.Action_DB + "' to delete")
        server.create_db(config.Action_DB)
    try:
        server.get_db(config.Mixin_DB).flush()
    except Exception:
        logger.debug("No DB named: '" + config.Mixin_DB + "' to delete")
        server.create_db(config.Mixin_DB)

class KindManager:
    """

        Manager for Kind documents on couch database

    """

    def __init__(self):

        try:
            self.server = Server('http://' + str(DB_server_IP) + ':' + str(DB_server_PORT))
        except Exception:
            logger.error("KindManager : Database is unreachable")
            raise Exception("Database is unreachable")

    def add_design_kind_docs_to_db(self):
        """
        Add kind design documents to database.
        """
        database = self.server.get_or_create_db(config.Kind_DB)
        design_doc = {
            "_id": "_design/get_kind",
            "language": "javascript",
            "type": "DesignDoc",
            "views": {
                "all": {
                    "map": "(function(doc) { emit(doc._id, doc.OCCI_Description) });"
                },
                "by_occi_id": {
                    "map": "(function(doc) { emit (doc.OCCI_ID, doc.Creator) });"
                },
                "by_occi_location": {
                    "map": "(function(doc) { emit (doc.OCCI_Location, doc.OCCI_ID) });"
                }

            }

        }
        if database.doc_exist(design_doc['_id']):
            pass
        else:
            database.save_doc(design_doc)


    def get_filtered_kinds(self,jfilters=None):
        """
        Returns kind documents matching the filter provided
        Args:
            @param jfilters: description of the kind document to retrieve
            @return : <list> OCCI kind description contained inside of the kind document
        """
        database = self.server.get_or_create_db(config.Kind_DB)
        #if the there are many kind filters, any kind matching just one filter will be returned
        self.add_design_kind_docs_to_db()
        query = database.view('/get_kind/all')
        var = list()
        #Extract kind descriptions from the dictionary
        try:
            for elem in query:
                for jfilter in jfilters:
                    ok = joker.filter_occi_description(elem['value'],jfilter)
                    if ok is True:
                        var.append(elem['value'])
                        logger.debug("Kind filtered document found")
                    else:
                        message = "No kind document matches the requirements"
                        logger.debug(message)
            return var,return_code['OK']
        except Exception as e:
            logger.error("filtered kinds : " + e.message)
            return "An error has occurred, please check log for more details",return_code['Internal Server Error']

    def get_all_kinds(self):
        """
        Returns all kind documents stored in database
        Args:
            @return : <list> All OCCI kind descriptions contained inside kind documents stored in the database
        """
        database = self.server.get_or_create_db(config.Kind_DB)
        self.add_design_kind_docs_to_db()
        query = database.view('/get_kind/all')
        var = list()
        #Extract kind descriptions from the dictionary
        try:
            for elem in query:
                var.append(elem['value'])
                logger.debug("Kind document found")
            return var,return_code['OK']
        except Exception as e:
            logger.error("all kind : " + e.message)
            return "An error has occurred, please check log for more details",return_code['Internal Server Error']

    def register_kinds(self,creator,descriptions):

        """
        Add new kinds to the database
        Args:
            @param creator: the id of the issuer of the creation request
            @param descriptions: OCCI kind descriptions
        """

        database = self.server.get_or_create_db(config.Kind_DB)
        self.add_design_kind_docs_to_db()
        manager_a = ActionManager()
        actions_data,ok = manager_a.get_all_actions()
        db_data,ok = self.get_all_kinds()
        loc_res = list()
        for desc in descriptions:
            occi_id = joker.get_description_id(desc)
            query = database.view('/get_kind/by_occi_id',key = occi_id)
            if query.count() is 0:
                occi_loc = joker.make_kind_location(desc)
                query = database.view('/get_kind/by_occi_location',key = occi_loc)
                if query.count() is 0:
                    ok = joker.verify_exist_relaters(desc,db_data)
                    if ok is True:
                        ok = joker.verify_exist_actions(desc,actions_data)
                        if ok is True:
                            doc_id = uuid_Generator.get_UUID()
                            jData = dict()
                            jData['Creator'] = creator
                            jData['CreationDate'] = str(datetime.now())
                            jData['LastUpdate'] = ""
                            jData['OCCI_Location']= occi_loc
                            jData['OCCI_Description']= desc
                            jData['OCCI_ID'] = occi_id
                            jData['Type']= "Kind"
                            jData['Provider']= {"local":[],"remote":[]}
                            try:
                                database[doc_id] = jData
                                message = "Kind document has been successfully added to database : " + occi_loc + ", " +str(return_code['OK'])
                                logger.debug("Register kind : " + message)
                                loc_res.append(occi_loc)
                            except Exception as e:
                                logger.error("Register Kind : " + e.message)
                                loc_res.append("An error has occurred, please check log for more details")
                                res_code = return_code['Internal Server Error']
                        else:
                            message = "Missing action description, Kind will not be created. Check log for more details" + ", " +str(return_code['Not Found'])
                            logger.error("Register kind : " + message)
                            loc_res.append(message)
                            res_code = return_code['OK, but there were some problems']
                    else:
                        message = "Missing related kind description, Kind will not be created. Check log for more details" ", " +str(return_code['Not Found'])
                        logger.error("Register kind : " + message)
                        loc_res.append(message)
                        res_code = return_code['OK, but there were some problems']
                else:
                    message = "Location conflict with document " + query.first()['value']+", kind will not be created. " + ", " +str(return_code['Conflict'])
                    logger.error("Register kind : " + message)
                    loc_res.append(message)
                    res_code = return_code['OK, but there were some problems']
            else:
                message = "This kind description already exists in document " +occi_id + ", " +str(return_code['Conflict'])
                logger.error("Register kind : " + message)
                loc_res.append(message)
                res_code = return_code['OK, but there were some problems']

        return loc_res,res_code


    def update_OCCI_kind_descriptions(self,user_id,data):
        """
        Updates the OCCI description field of the kind which document OCCI_ID is equal to OCCI_ID contained in data
        (Can only be done by the creator of the kind document)
        Args:
            @param user_id: ID of the creator of the kind document
            @param data: Data containing the OCCI ID of the kind and the new OCCI kind description
            @return : <string>, return_code
        """
        database = self.server.get_or_create_db(config.Kind_DB)
        self.add_design_kind_docs_to_db()
        events = list()
        resp_code = return_code['OK']
        for desc in data:
            old_occi_id = desc['OCCI_ID']
            query = database.view('/get_kind/by_occi_id',key = old_occi_id)
            if query.count() is 1:
                if query.first()['value'] == user_id:
                    new_occi_id = joker.get_description_id(desc['kind'])
                    query_n = database.view('/get_kind/by_occi_id',key = new_occi_id)
                    if query_n.count() <=1:
                        oldData = database.get(query.first()['id'])
                        old_description = oldData['OCCI_Description']
                        problems,occi_description= joker.update_occi_description(old_description,desc['kind'])
                        oldData['OCCI_Description'] = occi_description
                        oldData['OCCI_ID'] = new_occi_id
                        oldData['OCCI_Location'] = joker.make_kind_location(desc['kind'])
                        if problems is True:
                            message = "Kind OCCI description " + old_occi_id + " has not been totally updated. Check log for more details"
                            resp_code = return_code['OK, but there were some problems']
                        else:
                            message = "Kind OCCI description " + old_occi_id + " has been updated successfully"
                        oldData['LastUpdate'] = str(datetime.now())
                        #Update the kind document
                        database.save_doc(oldData,force_update = True)
                        events.append(message)
                        logger.debug("Update kind OCCI des : " +message)
                    else:
                        message = "New kind OCCI ID conflict with document " + new_occi_id + " ," +str(return_code['Conflict'])
                        logger.error("Update kind OCCI des : " + message)
                        events.append(message)
                        resp_code = return_code['OK, but there were some problems']

                else:
                    message= "You have no right to update this kind document ," + str(return_code['Forbidden'])
                    logger.error("Update kind OCCI des : " +message)
                    events.append(message)
                    resp_code = return_code['OK, but there were some problems']

            else:
                message = "Kind document " + old_occi_id + " couldn\'t be found ," + str(return_code['Not Found'])
                logger.error(message)
                events.append(message)
                resp_code = return_code['OK, but there were some problems']
        return events,resp_code

    def update_kind_providers(self,user_id=None,new_Data=None):
        """
        Update kind documents provider field (can only be done by the creator of the document)
        Args:
            @param user_id: the id of the issuer of the update request
            @param new_Data: the data that will be used to update the kind document
        """
        #Get the old document data from the database
        database = self.server.get_or_create_db(config.Kind_DB)
        self.add_design_kind_docs_to_db()
        message = list()
        resp_code = return_code['OK']
        for desc in new_Data:
            occi_id = desc['OCCI_ID']
            query = database.view('/get_kind/by_occi_id',key = occi_id)
            if query.count() is not 0:
                if query.first()['value'] == user_id:
                    old_data = database.get(query.first()['id'])
                    old_data['Provider'],problems = doc_Joker.update_kind_provider(old_data['Provider'],desc['Provider'])
                    if problems is True:
                        event = "Kind document " + occi_id + " has not been totally updated. Check log for more details, " + str(return_code['OK'])
                        resp_code = return_code['OK, but there were some problems']
                    else:
                        event = "Kind document " + occi_id + " has been updated successfully, " + str(return_code['OK, but there were some problems'])

                    old_data['LastUpdate'] = str(datetime.now())
                    #Update the kind document
                    database.save_doc(old_data,force_update = True)
                    message.append(event)
                    logger.debug(event)
                else:
                    event = "You have no right to update this kind document, " + str(return_code['Forbidden'])
                    message.append(event)
                    logger.error(event)
                    resp_code = return_code['OK, but there were some problems']


            else:
                event = "Kind document " + occi_id + "couldn\'t be found, " + str(return_code['Not Found'])
                logger.error(event)
                message.append(event)
                resp_code = return_code['OK, but there were some problems']
        return message,resp_code



    def delete_kind_documents(self,description=None,user_id=None):
        """
        Delete kind documents that is related to the scheme + term contained in the description provided
        Args:
            @param description: OCCI description of the kind document to delete
            @param user_id: id of the issuer of the delete request
        """
        database = self.server.get_or_create_db(config.Kind_DB)
        self.add_design_kind_docs_to_db()
        message = list()
        res_code = return_code['OK']
        #Verify the existence of such kind document
        for desc in description:
            occi_id = joker.get_description_id(desc)
            query = database.view('/get_kind/by_occi_id',key = occi_id)
            if query.count() is not 0:
                if query.first()['value'] == user_id:
                    ok = joker.get_resources_belonging_to_kind(desc)
                    if ok is True:
                        database.delete_doc(query.first()['id'])
                        event = "Kind document " + occi_id + " has been successfully deleted " + ", " +str(return_code['OK'])
                        logger.debug("Delete kind : " + event)
                        message.append(event)
                    else:
                        event = "Unable to delete because this kind document " + occi_id + " has resources depending on it. " + ", " +str(return_code['Unauthorized'])
                        logger.error("Delete kind : " + event)
                        message.append(event)
                        res_code = return_code['OK, but there were some problems']
                else:
                    event = "You have no right to delete this kind document " + occi_id + ", " + str(return_code['Unauthorized'])
                    logger.error("Delete kind : " + event)
                    message.append(event)
                    res_code = return_code['OK, but there were some problems']

            else:
                event = "Kind document " + occi_id + " does not exist " + ", " +str(return_code['Not Found'])
                logger.error("Delete kind : " + event)
                message.append(event)
                res_code = return_code['OK, but there were some problems']


        return message,res_code

    def verify_kind_location(self,location):
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

    def verify_exist_kind(self,kind_occi_id):
        """
        Verify the existence of a kind with such an OCCI ID
        Args:
            @param kind_occi_id: Kind OCCI ID to be checked
        """
        self.add_design_kind_docs_to_db()
        database = self.server.get_or_create_db(config.Kind_DB)
        query = database.view('/get_kind/by_occi_id',key = kind_occi_id)
        if query.count() is 0:
            logger.debug("Kind with kind OCCI ID = " + kind_occi_id + " not found")
            return False
        else:
            return True



class MixinManager:
    """

        Manager for Mixin documents on couch database

    """

    def __init__(self):

        try:
            self.server = Server('http://' + str(DB_server_IP) + ':' + str(DB_server_PORT))
        except Exception:
            logger.error("Mixin : Database is unreachable")
            raise Exception("Database is unreachable")

    def add_design_mixin_docs_to_db(self):
        """
        Add mixin design documents to database.
        """
        database = self.server.get_or_create_db(config.Mixin_DB)
        design_doc = {
            "_id": "_design/get_mixin",
            "language": "javascript",
            "type": "DesignDoc",
            "views": {
                "all": {
                    "map": "(function(doc) { emit(doc._id, doc.OCCI_Description) });"
                },
                "by_occi_id": {
                    "map": "(function(doc) { emit (doc.OCCI_ID, doc.Creator) });"
                },
                "by_occi_location": {
                    "map": "(function(doc) { emit (doc.OCCI_Location, doc.OCCI_ID) });"
                }
            }

        }
        if database.doc_exist(design_doc['_id']):
            pass
        else:
            database.save_doc(design_doc)


    def get_filtered_mixins(self,jfilters=None):
        """
        Returns mixin documents matching the filter provided
        Args:
            @param jfilters: description of the mixin document to retrieve
            @return : <list> OCCI mixin description contained inside of the mixin document
        """
        database = self.server.get_or_create_db(config.Mixin_DB)
        #if the there are many mixin filters, any mixin matching just one filter will be returned
        self.add_design_mixin_docs_to_db()
        query = database.view('/get_mixin/all')
        var = list()
        #Extract mixin descriptions from the dictionary
        try:
            for elem in query:
                for jfilter in jfilters:
                    ok = joker.filter_occi_description(elem['value'],jfilter)
                    if ok is True:
                        var.append(elem['value'])
                        logger.debug("Filter mixin : Mixin document found")
                    else:
                        message = "Filter mixin : No mixin document matches the requirements"
                        logger.debug(message)
            return var,return_code['OK']
        except Exception as e:
            logger.error("Filter mixin : " + e.message)
            return "An error has occurred, please check log for more details",return_code['Internal Server Error']

    def get_all_mixins(self):
        """
        Returns all mixin documents stored in database
        Args:
            @return : <list> All OCCI mixin descriptions contained inside mixin documents stored in the database
        """
        database = self.server.get_or_create_db(config.Mixin_DB)
        self.add_design_mixin_docs_to_db()
        query = database.view('/get_mixin/all')
        var = list()
        #Extract mixin descriptions from the dictionary
        try:
            for elem in query:
                var.append(elem['value'])
                logger.debug("Mixin document found")
            return var,return_code['OK']
        except Exception as e:
            logger.error("All mixin : " + e.message)
            return "An error has occurred, please check log for more details",return_code['Internal Server Error']

    def register_mixins(self,creator,descriptions):

        """
        Add new mixins to the database
        Args:
            @param creator: the id of the issuer of the creation request
            @param descriptions: OCCI mixin descriptions
        """
        database = self.server.get_or_create_db(config.Mixin_DB)
        self.add_design_mixin_docs_to_db()
        manager_a = ActionManager()
        actions_data,ok = manager_a.get_all_actions()
        db_data = list()
        loc_res = list()
        res_code = return_code['OK']
        query = database.view('/get_mixin/all')
        for q in query:
            db_data.append(q['value'])
        for desc in descriptions:
            occi_id = joker.get_description_id(desc)
            query = database.view('/get_mixin/by_occi_id',key = occi_id)
            if query.count() is 0:
                occi_loc = joker.make_mixin_location(desc)
                query = database.view('/get_mixin/by_occi_location',key = occi_loc)
                if query.count() is 0:
                    ok = joker.verify_exist_relaters(desc,db_data)
                    if ok is True:
                        ok = joker.verify_exist_actions(desc,actions_data)
                        if ok is True:
                            doc_id = uuid_Generator.get_UUID()
                            jData = dict()
                            jData['Creator'] = creator
                            jData['CreationDate'] = str(datetime.now())
                            jData['LastUpdate'] = ""
                            jData['OCCI_Location']= occi_loc
                            jData['OCCI_Description']= desc
                            jData['OCCI_ID'] = occi_id
                            jData['Type']= "Mixin"
                            try:
                                database[doc_id] = jData
                                message = "Mixin document has been successfully added to database : " + occi_loc + ", " +str(return_code['OK'])
                                logger.debug("Register mixin : " + message)
                                loc_res.append(occi_loc)
                            except Exception as e:
                                logger.error("Register mixin : " + e.message)
                                loc_res.append("An error has occured, please check log for more details")
                                res_code = return_code['Internal Server Error']
                        else:
                            message = "Missing action description, mixin will not be created. Check log for more details" + ", " +str(return_code['Not Found'])
                            logger.error("Register mixin : " + message)
                            loc_res.append(message)
                            res_code = return_code['OK, but there were some problems']
                    else:
                        message = "Missing related mixin description, mixin will not be created. Check log for more details" + ", " +str(return_code['Not Found'])
                        logger.error("Register mixin : " + message)
                        loc_res.append(message)
                        res_code = return_code['OK, but there were some problems']
                else:
                    message = "Location conflict with document " + query.first()['value']+", mixin will not be created" + ", " +str(return_code['Conflict'])
                    logger.error("Register mixin : " + message)
                    loc_res.append(message)
                    res_code = return_code['OK, but there were some problems']
            else:
                message = "This mixin description already exists in document " +occi_id + ", " +str(return_code['Conflict'])
                logger.error("Register mixin : " + message)
                loc_res.append(message)
                res_code = return_code['OK, but there were some problems']

        return loc_res,res_code



    def update_OCCI_mixin_descriptions(self,user_id,data):
        """
        Updates the OCCI description field of the mixin which document OCCI_ID is equal to OCCI_ID contained in data
        (Can only be done by the creator of the mixin document)
        Args:
            @param user_id: ID of the creator of the mixin document
            @param data: Data containing the OCCI ID of the mixin and the new OCCI mixin description
            @return : <string>, return_code
        """
        database = self.server.get_or_create_db(config.Mixin_DB)
        self.add_design_mixin_docs_to_db()
        events = list()
        resp_code = return_code['OK']
        for desc in data:
            old_occi_id = desc['OCCI_ID']
            query = database.view('/get_mixin/by_occi_id',key = old_occi_id)
            if query.count() is 1:
                if query.first()['value'] == user_id:
                    new_occi_id = joker.get_description_id(desc['mixin'])
                    query_n = database.view('/get_mixin/by_occi_id',key = new_occi_id)
                    if query_n.count() <=1:
                        oldData = database.get(query.first()['id'])
                        old_description = oldData['OCCI_Description']
                        problems,occi_description= joker.update_occi_description(old_description,desc['mixin'])
                        oldData['OCCI_Description'] = occi_description
                        oldData['OCCI_ID'] = new_occi_id
                        oldData['OCCI_Location'] = joker.make_kind_location(desc['kind'])
                        if problems is True:
                            message = "Mixin OCCI description " + old_occi_id + " has not been totally updated. Check log for more details"
                            resp_code = return_code['OK, but there were some problems']
                        else:
                            message = "Mixin OCCI description " + old_occi_id + " has been updated successfully"
                        oldData['LastUpdate'] = str(datetime.now())
                        #Update the mixin document
                        database.save_doc(oldData,force_update = True)
                        events.append(message)
                        logger.debug("Update mixin OCCI des : " +message)
                    else:
                        message = "New mixin OCCI ID conflict with document " + new_occi_id + " ," +str(return_code['Conflict'])
                        logger.error("Update mixin OCCI des : " + message)
                        events.append(message)
                        resp_code = return_code['OK, but there were some problems']

                else:
                    message= "You have no right to update this mixin document ," + str(return_code['Forbidden'])
                    logger.error("Update mixin OCCI des : " +message)
                    events.append(message)
                    resp_code = return_code['OK, but there were some problems']

            else:
                message = "Mixin document " + old_occi_id + " couldn\'t be found ," + str(return_code['Not Found'])
                logger.error(message)
                events.append(message)
                resp_code = return_code['OK, but there were some problems']
        return events,resp_code






    def delete_mixin_documents(self,description=None,user_id=None):
        """
        Delete mixin documents that is related to the scheme + term contained in the description provided
        Args:
            @param description: OCCI description of the mixin document to delete
            @param user_id: id of the issuer of the delete request
        """
        database = self.server.get_or_create_db(config.Mixin_DB)
        self.add_design_mixin_docs_to_db()
        message = list()
        resp_code = return_code['OK']
        #Verify the existence of such mixin document
        for desc in description:
            occi_id = joker.get_description_id(desc)
            query = database.view('/get_mixin/by_occi_id',key = occi_id)
            if query.count() is not 0:
                if query.first()['value'] == user_id:
                    database.delete_doc(query.first()['id'])
                    joker.dissociate_resource_from_mixin(occi_id)
                    event = "Mixin document " + occi_id + " has been successfully deleted " + str(return_code['OK'])
                    logger.debug("Delete mixin : "+ event)
                    message.append(event)
                else:
                    event = "You have no right to delete this mixin document " + occi_id + " " + str(return_code['Forbidden'])
                    logger.error("Delete mixin : "+ event)
                    message.append(event)
                    resp_code = return_code['OK, but there were some problems']
            else:
                event = "Mixin document " + occi_id + " does not exist " + str(return_code['Not Found'])
                logger.error("Delete mixin : "+ event)
                message.append(event)
                resp_code = return_code['OK, but there were some problems']
        return message,resp_code

    def verify_mixin_location(self,location):
        """
        Verify the existence of a mixin with such location
        Args:
            @param location: location of mixin
        """
        mixin_location = "http://" + config.OCNI_IP + ":" + config.OCNI_PORT + "/-" + location
        self.add_design_mixin_docs_to_db()
        database = self.server.get_or_create_db(config.Mixin_DB)
        query = database.view('/get_mixin/by_occi_location',key = mixin_location)
        if query.count() is 0:
            logger.debug("Mixin with mixin location = " + mixin_location + " not found")
            return False,None
        else:
            return True,query.first()['value']

    def verify_exist_mixins(self,mixins_id_list,creator):
        """
        Verfiy the existence of mixins using the mixins OCCI ID provided and returns only the existing ones
        Args:
            @param mixins_id_list: List containing the ids of mixins that need to verify its existence
            @param creator: Issuer of the verify of existence of mixins
        """
        self.add_design_mixin_docs_to_db()
        database = self.server.get_or_create_db(config.Mixin_DB)
        exists = list()
        for mixin_id in mixins_id_list:
            query = database.view('/get_mixin/by_occi_id',key = mixin_id )
            if query.count() is 0:
                logger.error("Exist mixins : No match to mixin " + mixin_id)
            else:
                exists.append(mixin_id)
                logger.error("Exist mixins : Mixin " + mixin_id + " verified ")

        return exists

class ActionManager:
    """

        Manager for Action documents on couch database

    """

    def __init__(self):

        try:
            self.server = Server('http://' + str(DB_server_IP) + ':' + str(DB_server_PORT))
        except Exception:
            logger.error("Database is unreachable")
            raise Exception("Database is unreachable")

    def add_design_action_docs_to_db(self):
        """
        Add action design documents to database.
        """
        database = self.server.get_or_create_db(config.Action_DB)
        design_doc = {
            "_id": "_design/get_action",
            "language": "javascript",
            "type": "DesignDoc",
            "views": {
                "all": {
                    "map": "(function(doc) { emit(doc._id, doc.OCCI_Description) });"
                },
                "by_occi_id": {
                    "map": "(function(doc) { emit (doc.OCCI_ID, doc.Creator) });"
                }
            }

        }
        if database.doc_exist(design_doc['_id']):
            pass
        else:
            database.save_doc(design_doc)


    def get_filtered_actions(self,jfilters=None):
        """
        Returns action documents matching the filter provided
        Args:
            @param jfilters: description of the action document to retrieve
            @return : <list> OCCI action description contained inside of the action document
        """
        database = self.server.get_or_create_db(config.Action_DB)
        #if the there are many action filters, any action matching just one filter will be returned
        self.add_design_action_docs_to_db()
        query = database.view('/get_action/all')
        var = list()
        #Extract action descriptions from the dictionary
        try:
            for elem in query:
                for jfilter in jfilters:
                    ok = joker.filter_occi_description(elem['value'],jfilter)
                    if ok is True:
                        var.append(elem['value'])
                        logger.debug("Filter actions : Action documents found")
                    else:
                        message = "Filter actions : No action document matches the requirements"
                        logger.debug(message)
            return var,return_code['OK']
        except Exception as e:
            logger.error(" Filter actions : " + e.message)
            return "A problem has occurred, please check log for more details",return_code['Internal Server Error']

    def get_all_actions(self):
        """
        Returns all action documents stored in database
        Args:
            @return : <list> All OCCI action descriptions contained inside action documents stored in the database
        """
        database = self.server.get_or_create_db(config.Action_DB)
        self.add_design_action_docs_to_db()
        query = database.view('/get_action/all')
        var = list()
        #Extract action descriptions from the dictionary
        try:
            for elem in query:
                var.append(elem['value'])
                logger.debug("Filter all : Action document found")
            return var,return_code['OK']
        except Exception as e:
            logger.error(" Filter all actions : " +e.message)
            return "An error has occurred, please check log for more details",return_code['Internal Server Error']

    def register_actions(self,creator,descriptions):

        """
        Add new actions to the database
        Args:
            @param creator: the id of the issuer of the creation request
            @param descriptions: OCCI action descriptions
        """
        database = self.server.get_or_create_db(config.Action_DB)
        self.add_design_action_docs_to_db()
        loc_res = list()

        res_code = return_code['OK']
        for desc in descriptions:
            occi_id = joker.get_description_id(desc)
            query = database.view('/get_action/by_occi_id',key = occi_id)
            if query.count() is 0:
                doc_id = uuid_Generator.get_UUID()
                jData = dict()
                jData['Creator'] = creator
                jData['CreationDate'] = str(datetime.now())
                jData['LastUpdate'] = ""
                jData['OCCI_Description']= desc
                jData['OCCI_ID'] = occi_id
                jData['Type']= "Action"
                try:
                    database[doc_id] = jData
                    message = "Action document has been successfully added to database " + str(return_code['OK'])
                    logger.debug("Register actions : " + message)
                    loc_res.append(occi_id)
                except Exception as e:
                    logger.error("Register actions : " + e.message)
                    loc_res.append("An error has occurred, please check log for more details.")
                    res_code = return_code['Internal Server Error']
            else:
                message = "This action description is not unique. Check log for more details " + str(return_code['Conflict'])
                logger.error("Register actions : " + message)
                loc_res.append(message)
                res_code = return_code['OK, but there were some problems']

        return loc_res,res_code



    def update_OCCI_action_descriptions(self,user_id,data):
        """
        Updates the OCCI description field of the action which document OCCI_ID is equal to OCCI_ID contained in data
        (Can only be done by the creator of the action document)
        Args:
            @param user_id: ID of the creator of the action document
            @param data: Data containing the OCCI ID of the action and the new OCCI action description
            @return : <string>, return_code
        """
        database = self.server.get_or_create_db(config.Action_DB)
        self.add_design_action_docs_to_db()
        events = list()
        resp_code = return_code['OK']
        for desc in data:
            old_occi_id = desc['OCCI_ID']
            query = database.view('/get_action/by_occi_id',key = old_occi_id)
            if query.count() is 1:
                if query.first()['value'] == user_id:
                    new_occi_id = joker.get_description_id(desc['action'])
                    query_n = database.view('/get_action/by_occi_id',key = new_occi_id)
                    if query_n.count() <=1:
                        oldData = database.get(query.first()['id'])
                        old_description = oldData['OCCI_Description']
                        problems,occi_description= joker.update_occi_description(old_description,desc['action'])
                        oldData['OCCI_Description'] = occi_description
                        oldData['OCCI_ID'] = new_occi_id
                        if problems is True:
                            message = "Action OCCI description " + old_occi_id + " has not been totally updated. Check log for more details"
                            resp_code = return_code['OK, but there were some problems']
                        else:
                            message = "Action OCCI description " + old_occi_id + " has been updated successfully"
                        oldData['LastUpdate'] = str(datetime.now())
                        #Update the mixin document
                        database.save_doc(oldData,force_update = True)
                        events.append(message)
                        logger.debug("Update action OCCI des : " +message)
                    else:
                        message = "New action OCCI ID conflict with document " + new_occi_id + " ," +str(return_code['Conflict'])
                        logger.error("Update action OCCI des : " + message)
                        events.append(message)
                        resp_code = return_code['OK, but there were some problems']

                else:
                    message= "You have no right to update this action document ," + str(return_code['Forbidden'])
                    logger.error("Update action OCCI des : " +message)
                    events.append(message)
                    resp_code = return_code['OK, but there were some problems']

            else:
                message = "Action document " + old_occi_id + " couldn\'t be found ," + str(return_code['Not Found'])
                logger.error(message)
                events.append(message)
                resp_code = return_code['OK, but there were some problems']
        return events,resp_code

    def delete_action_documents(self,description=None,user_id=None):
        """
        Delete action documents that are related to the scheme + term contained in the description provided
        Args:
            @param description: OCCI description of the action document to delete
            @param user_id: id of the issuer of the delete request
        """
        database = self.server.get_or_create_db(config.Action_DB)
        self.add_design_action_docs_to_db()
        message = list()
        resp_code = return_code['OK']
        #Verify the existence of such action document
        for desc in description:
            occi_id = joker.get_description_id(desc)
            query = database.view('/get_action/by_occi_id',key = occi_id)
            if query.count() is not 0:
                if query.first()['value'] == user_id:
                    database.delete_doc(query.first()['id'])
                    event = "Action document " + occi_id + " has been successfully deleted " + str(return_code['OK'])
                    logger.debug("Delete actions : "+ event)
                    message.append(event)
                else:
                    event = "You have no right to delete this action document " + occi_id + " " + str(return_code['Forbidden'])
                    logger.error("Delete action : "+ event)
                    message.append(event)
                    resp_code = return_code['OK, but there were some problems']
            else:
                event = "Action document " + occi_id + " does not exist " + str(return_code['Not Found'])
                logger.error("Delete action : "+ event)
                message.append(event)
                resp_code = return_code['OK, but there were some problems']
        return message,resp_code

    def verify_exist_actions(self,actions_id_list,creator):
        """
        Verfiy the existence of actions using the actions OCCI ID provided and returns only the existing ones
        Args:
            @param actions_id_list: List containing the ids of actions that need to verify its existence
            @param creator: Issuer of the verify of existence of actions
        """
        self.add_design_action_docs_to_db()
        database = self.server.get_or_create_db(config.Action_DB)
        exists = list()
        for action_id in actions_id_list:
            try:
                action_id.index('category')
                query = database.view('/get_action/by_occi_id',key = action_id['category'])
                if query.count() is 0:
                    logger.error("Exist actions : action " + action_id['category'] + " does not exist")
                else:
                    logger.debug("Exist actions : action " + action_id['category'] + "existence verified ")
                    exists.append(action_id)
            except Exception as e:
                logger.error("Exist actions : " +e.message)

        return exists


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
        data_keys = jreq.keys()
        try:
            data_keys.index('actions')
            logger.debug("Actions post request : channeled")
            mesg_3,resp_code = self.manager_a.register_actions(user_id,jreq['actions'])
        except Exception as e:
            logger.error("ch register categories : " + e.message)
            mesg_3 = ""

        try:
            data_keys.index('kinds')
            logger.debug("Kinds post request : channeled")
            mesg_1,resp_code = self.manager_k.register_kinds(user_id,jreq['kinds'])
        except Exception as e:
            logger.error("ch register categories : " + e.message)
            mesg_1 = ""
        try:
            data_keys.index('mixins')
            logger.debug("Mixins post request : channeled")
            mesg_2,resp_code = self.manager_m.register_mixins(user_id,jreq['mixins'])
        except Exception as e:
            logger.error("ch register categories : " + e.message)
            mesg_2 = ""

        result = {'kinds': mesg_1, 'mixins': mesg_2, 'actions': mesg_3}
        return result

    def channel_get_all_categories(self):
        """
        Retrieve all categories to show the server's capacity

        """
        #get all kinds
        mesg_1,status_code_1 = self.manager_k.get_all_kinds()

        #get all mixins
        mesg_2,status_code_2 = self.manager_m.get_all_mixins()

        #get all actions
        mesg_3,status_code_3 = self.manager_a.get_all_actions()

        result = {'kinds': mesg_1, 'mixins': mesg_2, 'actions': mesg_3}

        return result

    def channel_get_filtered_categories(self,jreq):
        """
        Channel the post request to the right methods
        Args:
            @param jreq: Body content of the post request

        """

        data_keys = jreq.keys()
        try:
            data_keys.index('kinds')
            logger.debug("Kinds filter get request : channeled")
            mesg_1,resp_code = self.manager_k.get_filtered_kinds(jreq['kinds'])
        except Exception as e:
            logger.debug("ch get filter : " + e.message)
            mesg_1 = ""

        try:
            data_keys.index('mixins')
            logger.debug("Mixins filter get request : channeled")
            mesg_2,resp_code = self.manager_m.get_filtered_mixins(jreq['mixins'])
        except Exception as e:
            logger.debug("ch get filter : " + e.message)
            mesg_2 = ""

        try:
            data_keys.index('actions')
            logger.debug("Actions filter get : channeled")
            mesg_3,resp_code = self.manager_a.get_filtered_actions(jreq['actions'])
        except Exception as e:
            logger.debug("ch get filter : " + e.message)
            mesg_3 = ""

        result = {'kinds': mesg_1, 'mixins': mesg_2, 'actions': mesg_3}

        return result

    def channel_delete_categories(self,jreq,user_id):
        """
        Channel the delete request to the right methods
        Args:
            @param user_id: ID of the issuer of the post request
            @param jreq: Body content of the post request

        """
        data_keys = jreq.keys()
        try:
            data_keys.index('kinds')
            logger.debug("Kinds delete request : channeled")
            mesg_1,resp_code = self.manager_k.delete_kind_documents(jreq['kinds'],user_id)
        except Exception as e:
            logger.error("ch delete filter : " +e.message)
            mesg_1=""

        try:
            data_keys.index('mixins')
            logger.debug("Mixins delete request : channeled")
            mesg_2,resp_code = self.manager_m.delete_mixin_documents(jreq['mixins'],user_id)
        except Exception as e:
            logger.error("ch delete filter : " +e.message)
            mesg_2=""

        try:
            data_keys.index('actions')
            logger.debug("Actions delete request : channeled")
            mesg_3,resp_code = self.manager_a.delete_action_documents(jreq['actions'],user_id)
        except Exception as e:
            logger.error("ch delete filter : " +e.message)
            mesg_3 = ""

        result = {'kinds': mesg_1, 'mixins': mesg_2, 'actions': mesg_3}
        return result


    def channel_update_categories(self,user_id,j_newData):
        """
        Channel the PUT requests to their right methods
        Args:
            @param user_id: ID of the issuer of the post request
            @param j_newData: Body content of the post request
        """

        data_keys = j_newData.keys()
        try:
            data_keys.index('actions')
            logger.debug("Actions put request : channeled")
            mesg_3,resp_code = self.manager_a.update_OCCI_action_descriptions(user_id,j_newData['actions'])
        except Exception as e:
            logger.error("ch update categories : " + e.message)
            mesg_3=""

        try:
            data_keys.index('kinds')
            logger.debug("Kinds put request : channeled")
            mesg_1,resp_code = self.manager_k.update_OCCI_kind_descriptions(user_id,j_newData['kinds'])
        except Exception as e:
            logger.error("ch update categories : " + e.message)
            mesg_1=""
        try:
            data_keys.index('providers')
            logger.debug("Providers put request : channeled")
            mesg_4,resp_code = self.manager_k.update_kind_providers(user_id,j_newData['providers'])
        except Exception as e:
            logger.error("ch update categories : " + e.message)
            mesg_4=""

        try:
            data_keys.index('mixins')
            logger.debug("Mixins put request : channeled")
            mesg_2,resp_code = self.manager_m.update_OCCI_mixin_descriptions(user_id,j_newData['mixins'])
        except Exception as e:
            logger.error("ch update categories : " + e.message)
            mesg_2=""



        result = {'kinds': mesg_1, 'provider':mesg_4, 'mixins': mesg_2, 'actions': mesg_3}

        return result
