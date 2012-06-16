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
                "by_id": {
                    "map": "(function(doc) { emit (doc.OCCI_ID, doc._id) });"
                }
            }

        }
        if database.doc_exist(design_doc['_id']):
            pass
        else:
            database.save_doc(design_doc)


    def get_kind_by_id(self,doc_id=None):
        """
        Returns the kind document matching the id provided
        Args:
            @param doc_id: id of the kind document to retrieve
            @return : <dic> OCCI kind description contained inside of the kind document
        """
        database = self.server.get_or_create_db(config.Kind_DB)
        #if the doc_id is specified then only one kind document will be returned if it exists
        if database.doc_exist(doc_id):
            elem = database.get(doc_id)
            res = json.dumps(elem['OCCI_Description'])
            logger.debug("Kind document found")
            return res,return_code['OK']
        else:
            message = "Kind document " + str(doc_id) + " does not exist"
            logger.debug(message)
            return message,return_code['Resource not found']

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
        loc_res = list()
        for desc in descriptions['kinds']:
            res_code = return_code['OK']
            ok, occi_id = joker.get_description_id(desc)
            if ok is True:
                query = database.view('/get_kind/by_id',key = occi_id)
                if query.count() is 0:

                    doc_id = uuid_Generator.get_UUID()
                    ok, loc = joker.make_kind_location(desc,doc_id,creator)
                    if ok is True:
                        jData = dict()
                        jData['Creator'] = creator
                        jData['CreationDate'] = str(datetime.now())
                        jData['LastUpdate'] = ""
                        jData['Location']= loc
                        jData['OCCI_Description']= desc
                        jData['OCCI_ID'] = occi_id
                        jData['Type']= "Kind"
                        provider = {"local":[],"remote":[]}
                        jData['Provider']= provider
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
                        logger.error(loc)
                        loc_res.append(loc)
                        res_code = return_code['Bad Request']
                else:
                    message = "Kind description already exists in document " + query.first()['id']
                    logger.error(message)
                    loc_res.append(message)
                    res_code = return_code['Conflict']
            else:
                logger.error(occi_id)
                loc_res.append(occi_id)
                res_code = return_code['Bad Request']
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
                        ok, oldData['Location'] = joker.make_kind_location(occi_description,doc_id,user_id)
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



    def delete_kind_document(self,doc_id=None,user_id=None):
        """
        Delete the kind document that is related to the id provided (Can only be done by the creator of the document)
        Args:
            @param doc_id: id of the kind document to delete
            @param user_id: id of the issuer of the delete request
        """
        database = self.server.get_or_create_db(config.Kind_DB)
        #Verify the existence of such kind document
        if database.doc_exist(doc_id):
        #If so then delete
            try:
                Data = database.get(doc_id)
                if Data['Creator'] == user_id:
                    database.delete_doc(doc_id)
                    message = "Kind document " + str(doc_id) + " has been successfully deleted "
                    logger.debug(message)
                    return message,return_code['OK']
                else:
                    message = "You have no right to delete this kind document"
                    logger.debug(message)
                    return message,return_code['Unauthorized']
            except Exception as e:
                logger.debug(e.message)
                return e.message,return_code['Internal Server Error']
        else:
            #else reply with kind document not found
            message = "Kind document " + str(doc_id) + " not found"
            logger.debug(message)
            return message,return_code['Resource not found']

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
                "by_id": {
                    "map": "(function(doc) { emit (doc.OCCI_ID, doc._id) });"
                }
            }

        }
        if database.doc_exist(design_doc['_id']):
            pass
        else:
            database.save_doc(design_doc)


    def get_mixin_by_id(self,doc_id=None):
        """
        Returns the mixin document matching the id provided
        Args:
            @param doc_id: id of the mixin document to retrieve
            @return : <dic> OCCI mixin description contained inside of the mixin document
        """
        database = self.server.get_or_create_db(config.Mixin_DB)
        #if the doc_id is specified then only one mixin document will be returned if it exists
        if database.doc_exist(doc_id):
            elem = database.get(doc_id)
            res = json.dumps(elem['OCCI_Description'])
            logger.debug("Mixin document found")
            return res,return_code['OK']
        else:
            message = "Mixin document " + str(doc_id) + " does not exist"
            logger.debug(message)
            return message,return_code['Resource not found']

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
        loc_res = list()
        for desc in descriptions['mixins']:
            res_code = return_code['OK']
            ok, occi_id = joker.get_description_id(desc)
            if ok is True:
                query = database.view('/get_mixin/by_id',key = occi_id)
                if query.count() is 0:

                    doc_id = uuid_Generator.get_UUID()
                    ok, loc = joker.make_mixin_location(desc,doc_id,creator)
                    if ok is True:
                        jData = dict()
                        jData['Creator'] = creator
                        jData['CreationDate'] = str(datetime.now())
                        jData['LastUpdate'] = ""
                        jData['Location']= loc
                        jData['OCCI_Description']= desc
                        jData['OCCI_ID'] = occi_id
                        jData['Type']= "Mixin"
                        provider = {"local":[],"remote":[]}
                        jData['Provider']= provider
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
                        logger.error(loc)
                        loc_res.append(loc)
                        res_code = return_code['Bad Request']
                else:
                    message = "Mixin description already exists in document " + query.first()['id']
                    logger.error(message)
                    loc_res.append(message)
                    res_code = return_code['Conflict']
            else:
                logger.error(occi_id)
                loc_res.append(occi_id)
                res_code = return_code['Bad Request']
        return loc_res,res_code

    def update_mixin(self,doc_id,user_id,new_description):
        """
        Channel the update request to the right method

        """

        data_keys = new_description.keys()
        try:
            data_keys.index('Provider')
            logger.debug("Provider update request : OK")
            mesg,resp_code = self.update_mixin_provider(doc_id,user_id,new_description)
            return mesg,resp_code
        except Exception:
            try:
                data_keys.index('mixins')
                logger.debug("OCCI description update request : OK")
                mesg,resp_code = self.update_OCCI_mixin_description(doc_id,user_id,new_description)
                return mesg, resp_code
            except Exception as e:
                mesg = "Unknown data keys " + e.message
                logger.debug(mesg)
                return mesg,return_code['Internal Server Error']

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
                        ok, oldData['Location'] = joker.make_mixin_location(occi_description,doc_id,user_id)
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

    def update_mixin_provider(self,doc_id=None,user_id=None,new_Data=None):
        """
        Update mixin document provider field (can only be done by the creator of the document)
        Args:
            @param doc_id: the id of the mixin document to update
            @param user_id: the id of the issuer of the update request
            @param new_Data: the data that will be used to update the mixin document
        """
        #Get the old document data from the database
        database = self.server.get_or_create_db(config.Mixin_DB)
        if database.doc_exist(doc_id) is True:
            oldData = database.get(doc_id)
            if oldData['Creator'] == user_id:
                oldData_keys = oldData['Provider'].keys()
                newData_keys =  new_Data['Provider'].keys()
                problems = False
                #Try to update mixin document provider field
                for key in newData_keys:
                    try:
                        oldData_keys.index(key)
                        oldData['Provider'][key] = new_Data['Provider'][key]
                    except Exception:
                        problems = True
                        logger.debug(key + " could not be found")
                        #Keep the record of the keys(=parts) that couldn't be updated
                if problems is True:
                    message = "Mixin document " + str(doc_id) + " has not been totally updated. Check log for more details"
                else:
                    message = "Mixin document " + str(doc_id) + " has been updated successfully"
                oldData['LastUpdate'] = str(datetime.now())
                #Update the mixin document
                database.save_doc(oldData,force_update = True)
                logger.debug(message)
                return message,return_code['OK']
            else:
                message= "You have no right to update this mixin document"
                logger.debug(message)
                return message,return_code['Unauthorized']

        else:
            message = "Mixin document " + str(doc_id) + "couldn\'t be found"
            logger.debug(message)
            return message,return_code['Resource not found']



    def delete_mixin_document(self,doc_id=None,user_id=None):
        """
        Delete the mixin document that is related to the id provided (Can only be done by the creator of the document)
        Args:
            @param doc_id: id of the mixin document to delete
            @param user_id: id of the issuer of the delete request
        """
        database = self.server.get_or_create_db(config.Mixin_DB)
        #Verify the existence of such mixin document
        if database.doc_exist(doc_id):
        #If so then delete
            try:
                Data = database.get(doc_id)
                if Data['Creator'] == user_id:
                    database.delete_doc(doc_id)
                    message = "Mixin document " + str(doc_id) + " has been successfully deleted "
                    logger.debug(message)
                    return message,return_code['OK']
                else:
                    message = "You have no right to delete this mixin document"
                    logger.debug(message)
                    return message,return_code['Unauthorized']
            except Exception as e:
                logger.debug(e.message)
                return e.message,return_code['Internal Server Error']
        else:
            #else reply with mixin document not found
            message = "Mixin document " + str(doc_id) + " not found"
            logger.debug(message)
            return message,return_code['Resource not found']
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


    def get_action_by_id(self,doc_id=None):
        """
        Returns the action document matching the id provided
        Args:
            @param doc_id: id of the action document to retrieve
            @return : <dic> OCCI action description contained inside of the action document
        """
        database = self.server.get_or_create_db(config.Action_DB)
        #if the doc_id is specified then only one action document will be returned if it exists
        if database.doc_exist(doc_id):
            elem = database.get(doc_id)
            res = json.dumps(elem['OCCI_Description'])
            logger.debug("Action document found")
            return res,return_code['OK']
        else:
            message = "Action document " + str(doc_id) + " does not exist"
            logger.debug(message)
            return message,return_code['Resource not found']

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
        for desc in descriptions['actions']:
            res_code = return_code['OK']
            ok, occi_id = joker.get_description_id(desc)
            if ok is True:
                query = database.view('/get_action/by_id',key = occi_id)
                if query.count() is 0:

                    doc_id = uuid_Generator.get_UUID()
                    ok, loc = joker.make_action_location(desc,doc_id,creator)
                    if ok is True:
                        jData = dict()
                        jData['Creator'] = creator
                        jData['CreationDate'] = str(datetime.now())
                        jData['LastUpdate'] = ""
                        jData['Location']= loc
                        jData['OCCI_Description']= desc
                        jData['OCCI_ID'] = occi_id
                        jData['Type']= "Action"
                        provider = {"local":[],"remote":[]}
                        jData['Provider']= provider
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
                        logger.error(loc)
                        loc_res.append(loc)
                        res_code = return_code['Bad Request']
                else:
                    message = "Action description already exists in document " + query.first()['id']
                    logger.error(message)
                    loc_res.append(message)
                    res_code = return_code['Conflict']
            else:
                logger.error(occi_id)
                loc_res.append(occi_id)
                res_code = return_code['Bad Request']
        return loc_res,res_code

    def update_action(self,doc_id,user_id,new_description):
        """
        Channel the update request to the right method

        """

        data_keys = new_description.keys()
        try:
            data_keys.index('Provider')
            logger.debug("Provider update request : OK")
            mesg,resp_code = self.update_action_provider(doc_id,user_id,new_description)
            return mesg,resp_code
        except Exception:
            try:
                data_keys.index('actions')
                logger.debug("OCCI description update request : OK")
                mesg,resp_code = self.update_OCCI_action_description(doc_id,user_id,new_description)
                return mesg, resp_code
            except Exception as e:
                mesg = "Unknown data keys " + e.message
                logger.debug(mesg)
                return mesg,return_code['Internal Server Error']

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
                        ok, oldData['Location'] = joker.make_action_location(occi_description,doc_id,user_id)
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

    def update_action_provider(self,doc_id=None,user_id=None,new_Data=None):
        """
        Update action document provider field (can only be done by the creator of the document)
        Args:
            @param doc_id: the id of the action document to update
            @param user_id: the id of the issuer of the update request
            @param new_Data: the data that will be used to update the action document
        """
        #Get the old document data from the database
        database = self.server.get_or_create_db(config.Action_DB)
        if database.doc_exist(doc_id) is True:
            oldData = database.get(doc_id)
            if oldData['Creator'] == user_id:
                oldData_keys = oldData['Provider'].keys()
                newData_keys =  new_Data['Provider'].keys()
                problems = False
                #Try to update action document provider field
                for key in newData_keys:
                    try:
                        oldData_keys.index(key)
                        oldData['Provider'][key] = new_Data['Provider'][key]
                    except Exception:
                        problems = True
                        logger.debug(key + " could not be found")
                        #Keep the record of the keys(=parts) that couldn't be updated
                if problems is True:
                    message = "Action document " + str(doc_id) + " has not been totally updated. Check log for more details"
                else:
                    message = "Action document " + str(doc_id) + " has been updated successfully"
                oldData['LastUpdate'] = str(datetime.now())
                #Update the action document
                database.save_doc(oldData,force_update = True)
                logger.debug(message)
                return message,return_code['OK']
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
#class ActionManager:
#    """
#
#    Manager for the Action documents on couch database
#
#    """
#
#    def __init__(self):
#
#        try:
#            self.server = Server('http://' + str(DB_server_IP) + ':' + str(DB_server_PORT))
#        except Exception:
#            logger.error("Database is unreachable")
#            raise Exception("Database is unreachable")
#        try:
#            self.add_design_action_docs_to_db()
#        except Exception as e:
#            logger.debug(e.message)
#
#
#    def add_design_action_docs_to_db(self):
#        """
#        Add action design documents to database.
#        """
#        design_doc = {
#            "_id": "_design/get_action",
#            "language": "javascript",
#            "type": "DesignDoc",
#            "views": {
#                "all": {
#                    "map": "(function(doc) { emit(doc._id, doc.OCCI_Description) });"
#                }
#            }
#
#        }
#        database = self.server.get_or_create_db(config.Action_DB)
#        if database.doc_exist(design_doc['_id']):
#            pass
#        else:
#            database.save_doc(design_doc)
#
#
#    def get_action_by_id(self,doc_id=None):
#        """
#        Returns the action document matching the id provided
#        Args:
#            @param doc_id: id of the action document to retrieve
#            @return : <dic> OCCI action description contained inside of the action document
#        """
#        database = self.server.get_or_create_db(config.Action_DB)
#        #if the doc_id is specified then only one action will be returned if it exists
#        if database.doc_exist(doc_id):
#            res =""
#            elem = database.get(doc_id)
#            res = elem['OCCI_Description']
#            logger.debug("Action document found")
#            return res,return_code['OK']
#        else:
#            message = "Action document " + str(doc_id) + " does not exist"
#            logger.debug(message)
#            return message,return_code['Resource not found']
#
#    def get_all_actions(self):
#        """
#        Returns all action documents stored in database
#        Args:
#            @return : <dict> All OCCI action descriptions contained inside action documents stored in the database
#        """
#        database = self.server.get_or_create_db(config.Action_DB)
#        query = database.view('/get_action/all')
#        var = list()
#        #Extract action descriptions from the dictionary
#        try:
#            for elem in query:
#                var.append(elem['value'])
#            logger.debug("Action documents found")
#            return var,return_code['OK']
#        except Exception as e:
#            logger.error(e.message)
#            return e.message, return_code['Internal Server Error']
#
#
#    def register_action(self,creator,description):
#
#        """
#        Add a new action to the database
#        Args:
#            @param creator: the id of the issuer of the creation request
#            @param description: OCCI action description
#        """
#        database = self.server.get_or_create_db(config.Action_DB)
#        doc_id = uuid_Generator.get_UUID()
#        ok,loc = joker.make_action_location(description,doc_id,creator)
#        if ok is True:
#            jData = dict()
#            jData['Creator'] = creator
#            jData['CreationDate'] = str(datetime.now())
#            jData['LastUpdate'] = ""
#            jData['Location']= loc
#            jData['OCCI_Description']= description
#            jData['Type']= "Action"
#            provider = {"local":[],"remote":[]}
#            jData['Provider']= provider
#            try:
#                database[doc_id] = jData
#                logger.debug("Action document has been successfully added to database : " + loc)
#                return loc,return_code['OK']
#            except Exception as e:
#                logger.error(e.message)
#                return e.message,return_code['Internal Server Error']
#        else:
#            logger.error(loc)
#            return loc,return_code['Internal Server Error']
#
#    def update_action(self,doc_id=None,user_id=None,new_Data=None):
#        """
#        Update action document fields (can only be done by the creator of the document)
#        Args:
#            @param doc_id: the id of the action document to update
#            @param user_id: the id of the issuer of the update request
#            @param new_Data: the data that will be used to update the action document
#        """
#        #Get the old document data from the database
#        database = self.server.get_or_create_db(config.Action_DB)
#
#        if database.doc_exist(doc_id) is True:
#            oldData = database.get(doc_id)
#            if oldData['Creator'] == user_id:
#                oldData_keys = oldData.keys()
#                newData_keys =  new_Data.keys()
#                problems = False
#                #Update only the fields that exist in the new data
#                for key in newData_keys:
#                    try:
#                        #OCCI_Description field will be treated separately
#                        if key == "OCCI_Description":
#                            old_descrip = oldData[key]['actions'][0]
#                            new_descrip = new_Data[key]['actions'][0]
#                            problems,oldData[key]['actions'][0] = joker.update_occi_description(old_descrip,new_descrip)
#                        else:
#                            oldData_keys.index(key)
#                            oldData[key] = new_Data[key]
#                    except Exception:
#                        problems = True
#                        logger.debug(key + "could not be found")
#                        #Keep the record of the keys(=parts) that couldn't be update
#                if problems is True:
#                    message = "Action document " + str(doc_id) + " has not been totally updated. Check log for more details"
#                else:
#                    message = "Action document " + str(doc_id) + " has been updated successfully"
#                oldData['LastUpdate'] = str(datetime.now())
#                #Update the document
#                database.save_doc(oldData,force_update = True)
#                logger.debug(message)
#                return message,return_code['OK']
#            else:
#                message= "You have no right to update this action document"
#                logger.debug(message)
#                return message,return_code['Unauthorized']
#
#        else:
#            message = "Action document " + str(doc_id) + "couldn\'t be found"
#            logger.debug(message)
#            return message,return_code['Resource not found']
#
#
#
#    def delete_action_document(self,doc_id=None,user_id=None):
#        """
#        Delete the action document that is related to the id provided (Can only be done by the creator of the document)
#        Args:
#            @param doc_id: id of the action document to delete
#            @param user_id: id of the issuer of the delete request
#        """
#        database = self.server.get_or_create_db(config.Action_DB)
#        #Verify the existence of such action document
#        if database.doc_exist(doc_id):
#        #If so then delete
#            try:
#                Data = database.get(doc_id)
#                if Data['Creator'] == user_id:
#                    database.delete_doc(doc_id)
#                    message = "Action document " + str(doc_id) + " has been successfully deleted "
#                    logger.debug(message)
#                    return message,return_code['OK']
#                else:
#                    message = "You have no right to delete this action document"
#                    logger.debug(message)
#                    return message,return_code['Unauthorized']
#            except Exception as e:
#                logger.error(e.message)
#                return e.message,return_code['Internal Server Error']
#        else:
#            #else reply with action document not found
#            message = "Action document " + str(doc_id) + " not found"
#            logger.debug(message)
#            return message,return_code['Resource not found']