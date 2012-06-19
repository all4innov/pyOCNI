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
try:
    import simplejson as json
except ImportError:
    import json
from datetime import datetime
from pyocni.pyocni_tools import uuid_Generator
from couchdbkit import *
# ======================================================================================
# HTTP Return Codes
# ======================================================================================
return_code = {'OK': 200,
               'Accepted': 202,
               'Bad Request': 400,
               'Unauthorized': 401,
               'Forbidden': 403,
               'Resource not found': 404,
               'Method Not Allowed': 405,
               'Conflict': 409,
               'Gone': 410,
               'Unsupported Media Type': 415,
               'Internal Server Error': 500,
               'Not Implemented': 501,
               'Service Unavailable': 503}
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
            logger.error("Database is unreachable")
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
                    "map": "(function(doc) { emit (doc.OCCI_Location, doc._id) });"
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
                        str_value = json.dumps(elem['value'])
                        var.append(str_value)
                        logger.debug("Kind documents found")
                    else:
                        message = "No kind document matches the requirements"
                        logger.debug(message)
            return var,return_code['OK']
        except Exception as e:
            logger.error(e.message)
            return e.message,return_code['Internal Server Error']

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
                str_value = json.dumps(elem['value'])
                var.append(str_value)
            logger.debug("Kind documents found")
            return var,return_code['OK']
        except Exception as e:
            logger.error(e.message)
            return e.message,return_code['Internal Server Error']

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

        db_data = list()
        loc_res = list()
        query = database.view('/get_kind/all')
        res_code = return_code['OK']
        for q in query:
            db_data.append(q['value'])
        for desc in descriptions:
            ok,occi_id = joker.get_description_id(desc)
            query = database.view('/get_action/by_occi_id',key = occi_id)
            if query.count() is 0:
                ok,occi_loc = joker.make_mixin_location(desc)
                query = database.view('/get_action/by_occi_location',key = occi_loc)
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
                            ok,loc = joker.make_kind_location(desc)
                            jData['Location']= loc
                            jData['OCCI_Description']= desc
                            ok, occi_id =joker.get_description_id(desc)
                            jData['OCCI_ID'] = occi_id
                            jData['Type']= "Kind"
                            jData['Provider']= {"local":[],"remote":[]}
                            try:
                                database[doc_id] = jData
                                message = "Kind document has been successfully added to database : " + loc
                                logger.debug(message)
                                loc_res.append(message)
                            except Exception as e:
                                logger.error(e.message)
                                loc_res.append(e.message)
                                res_code = return_code['Internal Server Error']
                        else:
                            message = "Missing action description, Kind will not be created. Check log for more details"
                            logger.error(message)
                            loc_res.append(message)
                    else:
                        message = "Missing related kind description, Kind will not be created. Check log for more details"
                        logger.error(message)
                        loc_res.append(message)
                else:
                    message = "Location conflict with document " + query.first()['id']+", kind will not be created. "
                    logger.error(message)
                    loc_res.append(message)
            else:
                message = "This kind description already exists in document " +query.first()['id']
                logger.error(message)
                loc_res.append(message)

        return loc_res,res_code

    def update_kind(self,doc_id,user_id,new_description):
        """
        Channel the update request to the right method

        """

        data_keys = new_description.keys()
        try:
            data_keys.index('Provider')
            logger.debug("Provider update request : OK")
            mesg,resp_code = self.update_kind_provider(doc_id,user_id,new_description)
            return mesg,resp_code
        except Exception:
            try:
                data_keys.index('kinds')
                logger.debug("OCCI description update request : OK")
                mesg,resp_code = self.update_OCCI_kind_description(doc_id,user_id,new_description)
                return mesg, resp_code
            except Exception as e:
                mesg = "Unknown data keys " + e.message
                logger.debug(mesg)
                return mesg,return_code['Internal Server Error']

    def update_OCCI_kind_description(self,doc_id,user_id,new_description):
        """
        Updates the OCCI description field of the kind which document id is equal to doc_id (Can only be done by the creator of the kind document)
        Args:
            @param doc_id: ID of the kind document to update
            @param user_id: ID of the creator of the kind document
            @param new_description: The new OCCI kind description
            @return : <string>, return_code
        """
        database = self.server.get_or_create_db(config.Kind_DB)
        if database.doc_exist(doc_id) is True:
            oldData = database.get(doc_id)
            if oldData['Creator'] == user_id:
                old_description = oldData['OCCI_Description']
                new_description = new_description['kinds'][0]
                problems,occi_description= joker.update_occi_description(old_description,new_description)
                ok,occi_id = joker.get_description_id(occi_description)
                if ok is True:
                    query = database.view('/get_kind/by_id',key = occi_id)
                    if query.count() is 0:
                        oldData['OCCI_ID'] = occi_id
                        oldData['OCCI_Description'] = occi_description
                        if problems is True:
                            message = "Kind OCCI description " + str(doc_id) + " has not been totally updated. Check log for more details"
                        else:
                            message = "Kind OCCI description " + str(doc_id) + " has been updated successfully"
                        oldData['LastUpdate'] = str(datetime.now())
                        #Update the kind document
                        database.save_doc(oldData,force_update = True)
                        logger.debug(message)
                        return message,return_code['OK']
                    else:
                        message = "Kind description already exists in document " + query.first()['id']
                        logger.error(message)
                        return message,return_code['Conflict']

            else:
                message= "You have no right to update this kind document"
                logger.debug(message)
                return message,return_code['Unauthorized']

        else:
            message = "Kind document " + str(doc_id) + "couldn\'t be found"
            logger.debug(message)
            return message,return_code['Resource not found']

    def update_kind_provider(self,doc_id=None,user_id=None,new_Data=None):
        """
        Update kind document provider field (can only be done by the creator of the document)
        Args:
            @param doc_id: the id of the kind document to update
            @param user_id: the id of the issuer of the update request
            @param new_Data: the data that will be used to update the kind document
        """
        #Get the old document data from the database
        database = self.server.get_or_create_db(config.Kind_DB)
        if database.doc_exist(doc_id) is True:
            oldData = database.get(doc_id)
            if oldData['Creator'] == user_id:
                oldData_keys = oldData['Provider'].keys()
                newData_keys =  new_Data['Provider'].keys()
                problems = False
                #Try to update kind document provider field
                for key in newData_keys:
                    try:
                        oldData_keys.index(key)
                        oldData['Provider'][key] = new_Data['Provider'][key]
                    except Exception:
                        problems = True
                        logger.debug(key + " could not be found")
                    #Keep the record of the keys(=parts) that couldn't be updated
                if problems is True:
                    message = "Kind document " + str(doc_id) + " has not been totally updated. Check log for more details"
                else:
                    message = "Kind document " + str(doc_id) + " has been updated successfully"
                oldData['LastUpdate'] = str(datetime.now())
                #Update the kind document
                database.save_doc(oldData,force_update = True)
                logger.debug(message)
                return message,return_code['OK']
            else:
                message= "You have no right to update this kind document"
                logger.debug(message)
                return message,return_code['Unauthorized']

        else:
            message = "Kind document " + str(doc_id) + "couldn\'t be found"
            logger.debug(message)
            return message,return_code['Resource not found']



    def delete_kind_documents(self,description=None,user_id=None):
        """
        Delete kind documents that is related to the scheme + term contained in the description provided
        Args:
            @param description: OCCI description of the kind document to delete
            @param user_id: id of the issuer of the delete request
        """
        database = self.server.get_or_create_db(config.Kind_DB)
        message = ""
        #Verify the existence of such kind document
        for desc in description:
            ok, occi_id = joker.get_description_id(desc)
            if ok is True:
                query = database.view('/get_kind/by_occi_id',key = occi_id)
                if query.count() is not 0:
                    if query.first()['value'] == user_id:
                        ok = joker.get_resources_belonging_to_kind(desc)
                        if ok is True:
                            database.delete_doc(query.first()['id'])
                            message += "\nKind document " + occi_id + " has been successfully deleted " + return_code['OK']
                        else:
                            message += "\nUnable to delete because this kind document " + occi_id + " has resources depending on it. " + return_code['Forbidden']
                    else:
                        message += "\nYou have no right to delete this kind document " + occi_id + " " + return_code['Forbidden']

                else:
                    message += "\nKind document " + occi_id + " does not exist " + return_code['Resource not found']
        logger.debug(message)
        return message,return_code['OK']


class MixinManager:
    """

        Manager for Mixin documents on couch database

    """

    def __init__(self):

        try:
            self.server = Server('http://' + str(DB_server_IP) + ':' + str(DB_server_PORT))
        except Exception:
            logger.error("Database is unreachable")
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
                    "map": "(function(doc) { emit (doc.OCCI_Location, doc._id) });"
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
                        str_value = json.dumps(elem['value'])
                        var.append(str_value)
                        logger.debug("Mixin documents found")
                    else:
                        message = "No mixin document matches the requirements"
                        logger.debug(message)
            return var,return_code['OK']
        except Exception as e:
            logger.error(e.message)
            return e.message,return_code['Internal Server Error']

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
                str_value = json.dumps(elem['value'])
                var.append(str_value)
            logger.debug("Mixin documents found")
            return var,return_code['OK']
        except Exception as e:
            logger.error(e.message)
            return e.message,return_code['Internal Server Error']

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
            ok,occi_id = joker.get_description_id(desc)
            query = database.view('/get_action/by_occi_id',key = occi_id)
            if query.count() is 0:
                ok,occi_loc = joker.make_mixin_location(desc)
                query = database.view('/get_action/by_occi_location',key = occi_loc)
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
                            ok,loc = joker.make_mixin_location(desc)
                            jData['OCCI_Location']= loc
                            jData['OCCI_Description']= desc
                            ok, occi_id =joker.get_description_id(desc)
                            jData['OCCI_ID'] = occi_id
                            jData['Type']= "Mixin"
                            try:
                                database[doc_id] = jData
                                message = "Mixin document has been successfully added to database : " + loc
                                logger.debug(message)
                                loc_res.append(message)
                            except Exception as e:
                                logger.error(e.message)
                                loc_res.append(e.message)
                                res_code = return_code['Internal Server Error']
                        else:
                            message = "Missing action description, mixin will not be created. Check log for more details"
                            logger.error(message)
                            loc_res.append(message)
                    else:
                        message = "Missing related mixin description, mixin will not be created. Check log for more details"
                        logger.error(message)
                        loc_res.append(message)
                else:
                    message = "Location conflict with document " + query.first()['id']+", mixin will not be created."
                    logger.error(message)
                    loc_res.append(message)
            else:
                message = "This mixin description already exists in document " +query.first()['id']
                logger.error(message)
                loc_res.append(message)

        return loc_res,res_code



    def update_OCCI_mixin_description(self,doc_id,user_id,new_description):
        """
        Updates the OCCI description field of the mixin which document id is equal to doc_id (Can only be done by the creator of the mixin document)
        Args:
            @param doc_id: ID of the mixin document to update
            @param user_id: ID of the creator of the mixin document
            @param new_description: The new OCCI mixin description
            @return : <string>, return_code
        """
        database = self.server.get_or_create_db(config.Mixin_DB)
        if database.doc_exist(doc_id) is True:
            oldData = database.get(doc_id)
            if oldData['Creator'] == user_id:
                old_description = oldData['OCCI_Description']
                new_description = new_description['mixins'][0]
                problems,occi_description= joker.update_occi_description(old_description,new_description)
                ok,occi_id = joker.get_description_id(occi_description)
                if ok is True:
                    query = database.view('/get_mixin/by_id',key = occi_id)
                    if query.count() is 0:
                        oldData['OCCI_ID'] = occi_id
                        oldData['OCCI_Description'] = occi_description
                        if problems is True:
                            message = "Mixin OCCI description " + str(doc_id) + " has not been totally updated. Check log for more details"
                        else:
                            message = "Mixin OCCI description " + str(doc_id) + " has been updated successfully"
                        oldData['LastUpdate'] = str(datetime.now())
                        #Update the mixin document
                        database.save_doc(oldData,force_update = True)
                        logger.debug(message)
                        return message,return_code['OK']
                    else:
                        message = "Mixin description already exists in document " + query.first()['id']
                        logger.error(message)
                        return message,return_code['Conflict']

            else:
                message= "You have no right to update this mixin document"
                logger.debug(message)
                return message,return_code['Unauthorized']

        else:
            message = "Mixin document " + str(doc_id) + "couldn\'t be found"
            logger.debug(message)
            return message,return_code['Resource not found']





    def delete_mixin_documents(self,description=None,user_id=None):
        """
        Delete mixin documents that is related to the scheme + term contained in the description provided
        Args:
            @param description: OCCI description of the mixin document to delete
            @param user_id: id of the issuer of the delete request
        """
        database = self.server.get_or_create_db(config.Mixin_DB)
        message = ""
        #Verify the existence of such mixin document
        for desc in description:
            ok, occi_id = joker.get_description_id(desc)
            if ok is True:
                query = database.view('/get_kind/by_occi_id',key = occi_id)
                if query.count() is not 0:
                    if query.first()['value'] == user_id:
                        database.delete_doc(query.first()['id'])
                        joker.dissociate_resource_from_mixin()
                        message += "\nMixin document " + occi_id + " has been successfully deleted " + return_code['OK']
                    else:
                        message += "\nYou have no right to delete this mixin document " + occi_id + " " + return_code['Forbidden']

                else:
                    message += "\nMixin document " + occi_id + " does not exist " + return_code['Resource not found']
        logger.debug(message)
        return message,return_code['OK']

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
                "by_id": {
                    "map": "(function(doc) { emit (doc.OCCI_ID, doc._id) });"
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
                        str_value = json.dumps(elem['value'])
                        var.append(str_value)
                        logger.debug("Action documents found")
                    else:
                        message = "No action document matches the requirements"
                        logger.debug(message)
            return var,return_code['OK']
        except Exception as e:
            logger.error(e.message)
            return e.message,return_code['Internal Server Error']

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
                str_value = json.dumps(elem['value'])
                var.append(str_value)
            logger.debug("Action documents found")
            return var,return_code['OK']
        except Exception as e:
            logger.error(e.message)
            return e.message,return_code['Internal Server Error']

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
            ok,occi_id = joker.get_description_id(desc)
            query = database.view('/get_action/by_occi_id',key = occi_id)
            if query.count() is 0:
                doc_id = uuid_Generator.get_UUID()
                jData = dict()
                jData['Creator'] = creator
                jData['CreationDate'] = str(datetime.now())
                jData['LastUpdate'] = ""
                ok,loc = joker.make_action_location(desc)
                jData['OCCI_Location']= loc
                jData['OCCI_Description']= desc
                jData['OCCI_ID'] = occi_id
                jData['Type']= "Action"
                try:
                    database[doc_id] = jData
                    message = "Action document has been successfully added to database : " + loc
                    logger.debug(message)
                    loc_res.append(message)
                except Exception as e:
                    logger.error(e.message)
                    loc_res.append(e.message)
                    res_code = return_code['Internal Server Error']

            else:
                message = "This action description is not unique. Check log for more details"
                logger.error(message)
                loc_res.append(message)

        return loc_res,res_code



    def update_OCCI_action_description(self,doc_id,user_id,new_description):
        """
        Updates the OCCI description field of the action which document id is equal to doc_id (Can only be done by the creator of the action document)
        Args:
            @param doc_id: ID of the action document to update
            @param user_id: ID of the creator of the action document
            @param new_description: The new OCCI action description
            @return : <string>, return_code
        """
        database = self.server.get_or_create_db(config.Action_DB)
        if database.doc_exist(doc_id) is True:
            oldData = database.get(doc_id)
            if oldData['Creator'] == user_id:
                old_description = oldData['OCCI_Description']
                new_description = new_description['actions'][0]
                problems,occi_description= joker.update_occi_description(old_description,new_description)
                ok,occi_id = joker.get_description_id(occi_description)
                if ok is True:
                    query = database.view('/get_action/by_id',key = occi_id)
                    if query.count() is 0:
                        oldData['OCCI_ID'] = occi_id
                        oldData['OCCI_Description'] = occi_description
                        if problems is True:
                            message = "Action OCCI description " + str(doc_id) + " has not been totally updated. Check log for more details"
                        else:
                            message = "Action OCCI description " + str(doc_id) + " has been updated successfully"
                        oldData['LastUpdate'] = str(datetime.now())
                        #Update the action document
                        database.save_doc(oldData,force_update = True)
                        logger.debug(message)
                        return message,return_code['OK']
                    else:
                        message = "Action description already exists in document " + query.first()['id']
                        logger.error(message)
                        return message,return_code['Conflict']

            else:
                message= "You have no right to update this action document"
                logger.debug(message)
                return message,return_code['Unauthorized']

        else:
            message = "Action document " + str(doc_id) + "couldn\'t be found"
            logger.debug(message)
            return message,return_code['Resource not found']

    def delete_action_document(self,doc_id=None,user_id=None):
        """
        Delete the action document that is related to the id provided (Can only be done by the creator of the document)
        Args:
            @param doc_id: id of the action document to delete
            @param user_id: id of the issuer of the delete request
        """
        database = self.server.get_or_create_db(config.Action_DB)
        #Verify the existence of such action document
        if database.doc_exist(doc_id):
        #If so then delete
            try:
                Data = database.get(doc_id)
                if Data['Creator'] == user_id:
                    database.delete_doc(doc_id)
                    message = "Action document " + str(doc_id) + " has been successfully deleted "
                    logger.debug(message)
                    return message,return_code['OK']
                else:
                    message = "You have no right to delete this action document"
                    logger.debug(message)
                    return message,return_code['Unauthorized']
            except Exception as e:
                logger.debug(e.message)
                return e.message,return_code['Internal Server Error']
        else:
            #else reply with action document not found
            message = "Action document " + str(doc_id) + " not found"
            logger.debug(message)
            return message,return_code['Resource not found']

class CategoryManager:
    """

        Channel requests to their appropriate target : Kinds, Mixins and Actions

    """

    def __init__(self):

        self.manager_k = KindManager()
        self.manager_m = MixinManager()
        self.manager_a = ActionManager()

    def channel_register_categories(self,user_id,jreq):
        """
        Channel the post request to the right method

        """
        mesg_1 = ""
        mesg_2 = ""
        mesg_3 = ""
        data_keys = jreq.keys()
        try:
            data_keys.index('kinds')
            logger.debug("Kinds post request : channeled")
            mesg_1,resp_code = self.manager_k.register_kinds(user_id,jreq['kinds'])
        except Exception as e:
            logger.debug(e.message)

        try:
            data_keys.index('mixins')
            logger.debug("Mixins post request : channeled")
            mesg_2,resp_code = self.manager_m.register_mixins(user_id,jreq['mixins'])
        except Exception as e:
            logger.debug(e.message)

        try:
            data_keys.index('actions')
            logger.debug("Actions post request : channeled")
            mesg_3,resp_code = self.manager_a.register_actions(user_id,jreq['actions'])
        except Exception as e:
            logger.debug(e.message)

        result_1 = '\n========= Kinds : ===========\n'
        result_1 += '\n========= Kind : ===========\n'.join(mesg_1)
        result_2 = '\n========= Mixins : ===========\n'
        result_2 += '\n========= Mixin : ===========\n'.join(mesg_2)
        result_3 = '\n========= Actions : ===========\n'
        result_3 += '\n========= Action : ===========\n'.join(mesg_3)
        register = result_1 + "\n\n" + result_2 + "\n\n" + result_3 + "\n\n"
        return result_1

    def channel_get_all_categories(self):
        """
        Retrieve all categories to show the server's capacity

        """
        #get all kinds
        result_1 = '\n========= Kind : ===========\n'
        var,status_code_1 = self.manager_k.get_all_kinds()
        result_1 += '\n========= Kind : ===========\n'.join(var)

        #get all mixins
        result_2 = '\n========== Mixin : ==========\n'
        var,status_code_2 = self.manager_m.get_all_mixins()
        result_2 += '\n========== Mixin : ==========\n'.join(var)

        #get all actions
        result_3 = '\n========== Action : ==========\n'
        var,status_code_3 = self.manager_a.get_all_actions()
        result_3 += '\n========== Action : ==========\n'.join(var)

        capacities = result_1 + "\n\n" + result_2 + "\n\n" + result_3 + "\n\n"

        return capacities

    def channel_get_filtered_categories(self,jreq):
        """
        Channel the post request to the right method

        """
        mesg_1 = ""
        mesg_2 = ""
        mesg_3 = ""
        data_keys = jreq.keys()
        try:
            data_keys.index('kinds')
            logger.debug("Kinds filter get request : channeled")
            mesg_1,resp_code = self.manager_k.get_filtered_kinds(jreq['kinds'])
        except Exception as e:
            logger.debug(e.message)

        try:
            data_keys.index('mixins')
            logger.debug("Mixins filter get request : channeled")
            mesg_2,resp_code = self.manager_m.get_filtered_mixins(jreq['mixins'])
        except Exception as e:
            logger.debug(e.message)

        try:
            data_keys.index('actions')
            logger.debug("Actions filter get : channeled")
            mesg_3,resp_code = self.manager_a.get_filtered_actions(jreq['actions'])
        except Exception as e:
            logger.debug(e.message)

        result_1 = '\n========= Kinds : ===========\n'
        result_1 += '\n========= Kind : ===========\n'.join(mesg_1)
        result_2 = '\n========= Mixins : ===========\n'
        result_2 += '\n========= Mixin : ===========\n'.join(mesg_2)
        result_3 = '\n========= Actions : ===========\n'
        result_3 += '\n========= Action : ===========\n'.join(mesg_3)
        capacities = result_1 + "\n\n" + result_2 + "\n\n" + result_3 + "\n\n"

        return capacities

    def channel_delete_categories(self,jreq,user_id):
        """
        Channel the delete request to the right method

        """
        data_keys = jreq.keys()
        mesg_1 = ""
        mesg_2 = ""
        mesg_3 = ""
        try:
            data_keys.index('kinds')
            logger.debug("Kinds delete request : channeled")
            mesg_1,resp_code = self.manager_k.delete_kind_documents(user_id,jreq['kinds'])
        except Exception as e:
            logger.debug(e.message)

        try:
            data_keys.index('mixins')
            logger.debug("Mixins delete request : channeled")
            mesg_2,resp_code = self.manager_m.delete_mixin_documents(user_id,jreq['mixins'])
        except Exception as e:
            logger.debug(e.message)

        try:
            data_keys.index('actions')
            logger.debug("Actions delete request : channeled")
            mesg_3,resp_code = self.manager_a.delete_action_documents(user_id,jreq['actions'])
        except Exception as e:
            logger.debug(e.message)

        result_1 = '\n========= Kinds : ===========\n'
        result_1 += '\n========= Kind : ===========\n'.join(mesg_1)
        result_2 = '\n========= Mixins : ===========\n'
        result_2 += '\n========= Mixin : ===========\n'.join(mesg_2)
        result_3 = '\n========= Actions : ===========\n'
        result_3 += '\n========= Action : ===========\n'.join(mesg_3)
        register = result_1 + "\n\n" + result_2 + "\n\n" + result_3 + "\n\n"
        return register


