# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

# Copyright (C) 2011 Houssem Medhioub - Institut Telecom
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
@version: 0.2
@license: LGPL - Lesser General Public License
"""

import pyocni.pyocni_tools.config as config
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
        server.flush(config.Kind_DB)
    except Exception:
        logger.debug("No DB named: '" + config.Kind_DB + "' to delete.")
        server.create_db(config.Kind_DB)
    try:
        server.flush(config.Action_DB)
    except Exception:
        logger.debug("No DB named: '" + config.Action_DB + "' to delete")
        server.create_db(config.Action_DB)
    try:
        server.flush(config.Mixin_DB)
    except Exception:
        logger.debug("No DB named: '" + config.Mixin_DB + "' to delete")
        server.create_db(config.Mixin_DB)

class KindManager:
    """

        Kind records management on couch database

    """

    def __init__(self):

        try:
            self.server = Server('http://' + str(DB_server_IP) + ':' + str(DB_server_PORT))
        except Exception:
            logger.error("Database is unreachable")
            raise Exception("Database is unreachable")
        try:
            self.add_design_kind_docs_to_db()
        except Exception as e:
            logger.debug(e.message)


    def add_design_kind_docs_to_db(self):
        """
        Add admin design documents to database.
        """
        design_doc = {
            "_id": "_design/get_kind",
            "language": "javascript",
            "type": "DesignDoc",
            "views": {
                "all": {
                    "map": "(function(doc) { emit(doc._id, doc.Description) });"
                }
            }

        }
        database = self.server.get_or_create_db(config.Kind_DB)
        if database.doc_exist(design_doc['_id']):
            pass
        else:
            database.save_doc(design_doc)


    def get_kind_by_id(self,doc_id=None):
        """
        returns the document matching the id provided in the request
        """
        database = self.server.get_or_create_db(config.Kind_DB)
        #if the doc_id is specified then only one kind will be returned if it exists
        if database.doc_exist(doc_id):
            res =''
            elem = database.get(doc_id)
            res = elem['OCCI_Description']
            logger.debug("Kind found")
            return res,return_code['OK']
        else:
            message = "Kind " + str(doc_id) + " does not exist"
            logger.debug(message)
            return message,return_code['Resource not found']

    def get_all_kinds(self):
        """
        Returns all documents stored in database
        """
        database = self.server.get_or_create_db(config.Kind_DB)
        query = database.view('/get_kind/all')
        var = list()
        #Extract kind descriptions from the dictionary
        try:
            for elem in query:
                var.append(elem['value'])
            logger.debug("Kinds found")
            return var,return_code['OK']
        except Exception as e:
            logger.error(e.message)
            return e.message,return_code['Internal Server Error']

    def register_kind(self,creator,description):

        """
        Add a new kind to the database
        """
        database = self.server.get_or_create_db(config.Kind_DB)
        doc_id = uuid_Generator.get_UUID()
        jData = dict()
        jData['Creator'] = creator
        jData['CreationDate'] = str(datetime.now())
        jData['LastUpdate'] = ""
        jData['Location']= "/-/kind/" + creator + "/" + str(doc_id)
        jData['OCCI_Description']= description
        jData['Type']= "Kind"
        provider = {"local":[],"remote":[]}
        jData['Provider']= provider
        try:
            database[doc_id] = jData
            logger.debug("Document has been successfully added to database : " + jData["Location"])
            return jData["Location"],return_code['OK']
        except Exception as e:
            logger.error(e.message)
            return e.message,return_code['Internal Server Error']

#    def update_part_of_kind(self,doc_id,newData,j_oldData,newData_keys):
#        """
#        update only a part of the kind description (can be called only after a failed try to fully update the kind description)
#        """
#        database = self.server.get_or_create_db(config.Kind_DB)
#        #Try to change parts of the kind description
#        oldData_keys =  j_oldData['kinds'][0].keys()
#        problems = False
#        for key in newData_keys:
#            try:
#                oldData_keys.index(key)
#                j_oldData['kinds'][0][key] = newData[key]
#            except Exception:
#                #Keep the record of the keys(=parts) that couldn't be updated
#                logger.debug(key + 'could not be found')
#                problems = True
#        if problems:
#            message = "Document " + str(doc_id) + " has not been totally updated. Check log for more details"
#        else:
#            message = "Document " + str(doc_id) + " has been updated successfully"
#        return j_oldData,message

    def update_kind(self,doc_id=None,user_id=None,new_Data=None):
        """
        update all of the document description
        """
        #Get the old document data from the database
        database = self.server.get_or_create_db(config.Kind_DB)

        if database.doc_exist(doc_id) is True:
            oldData = database.get(doc_id)
            if oldData['Creator'] == user_id:
                oldData_keys = oldData.keys()
                newData_keys =  new_Data.keys()
                problems = False
                #Try to change the hole kind description
                for key in newData_keys:
                    try:
                        oldData_keys.index(key)
                        oldData[key] = new_Data[key]
                    except Exception:
                        problems = True
                        logger.debug(key + "could not be found")
                    #Keep the record of the keys(=parts) that couldn't be updated
                if problems:
                    message = "Document " + str(doc_id) + " has not been totally updated. Check log for more details"
                else:
                    message = "Document " + str(doc_id) + " has been updated successfully"
                oldData['LastUpdate'] = str(datetime.now())
                #Update the document
                database.save_doc(oldData,force_update = True)
                logger.debug(message)
                return message,return_code['OK']
            else:
                message= "You have no right to update this document"
                logger.debug(message)
                return message,return_code['Unauthorized']

        else:
            message = "Document " + str(doc_id) + "couldn\'t be found"
            logger.debug(message)
            return message,return_code['Resource not found']



    def delete_kind_document(self,doc_id=None,user_id=None):
        """
        Delete the document that is related to the id provided (Can only be done by the creator of the document)
        """
        database = self.server.get_or_create_db(config.Kind_DB)
        #Verify the existence of such document
        if database.doc_exist(doc_id):
        #If so then delete
            try:
                Data = database.get(doc_id)
                if Data['Creator'] == user_id:
                    database.delete_doc(doc_id)
                    message = "Document " + str(doc_id) + " has been successfully deleted "
                    logger.debug(message)
                    return message,return_code['OK']
                else:
                    message = "You have no right to delete this document"
                    logger.debug(message)
                    return message,return_code['Unauthorized']
            except Exception as e:
                logger.debug(e.message)
                return e.message,return_code['Internal Server Error']
        else:
            #else reply with document not found
            message = "Document " + str(doc_id) + " not found"
            logger.debug(message)
            return message,return_code['Resource not found']

class MixinManager:
    """

    Mixin records management on couch database

    """

    def __init__(self):

        try:
            self.server = Server('http://' + str(DB_server_IP) + ':' + str(DB_server_PORT))
        except Exception:
            logger.error("Database is unreachable")
            raise Exception("Database is unreachable")
        try:
            self.add_design_mixin_docs_to_db()
        except Exception as e:
            logger.debug(e.message)


    def add_design_mixin_docs_to_db(self):
        """
        Add admin design documents to database.
        """
        design_doc = {
            "_id": "_design/get_mixin",
            "language": "javascript",
            "type": "DesignDoc",
            "views": {
                "all": {
                    "map": "(function(doc) { emit(doc._id, doc.Description) });"
                }
            }

        }
        database = self.server.get_or_create_db(config.Mixin_DB)
        if database.doc_exist(design_doc['_id']):
            pass
        else:
            database.save_doc(design_doc)


    def get_mixin_by_id(self,doc_id=None):
        """
        returns the mixin matching the id provided in the request
        """
        database = self.server.get_or_create_db(config.Mixin_DB)
        #if the doc_id is specified then only one mixin will be returned if it exists
        if database.doc_exist(doc_id):
            elem = database.get(doc_id)
            res = elem['OCCI_Description']
            logger.debug("Mixin found")
            return res,return_code['OK']
        else:
            message = "Mixin " + str(doc_id) + " does not exist"
            logger.debug(message)
            return message,return_code['Resource not found']

    def get_all_mixins(self):
        """
        Returns all mixins stored in database
        """
        database = self.server.get_or_create_db(config.Mixin_DB)
        query = database.view('/get_mixin/all')
        var = list()
        #Extract mixin descriptions from the dictionary
        try:
            for elem in query:
                var.append(elem['value'])
            logger.debug("Mixins found")
            return var,return_code['OK']
        except Exception as e:
            logger.error(e.message)
            return e.message,return_code['Internal Server Error']

    def register_mixin(self,creator,description):

        """
        Add a new mixin to the database
        """
        database = self.server.get_or_create_db(config.Mixin_DB)
        doc_id = uuid_Generator.get_UUID()
        jData = dict()
        jData['Creator'] = creator
        jData['CreationDate'] = str(datetime.now())
        jData['LastUpdate'] = ""
        jData['Location']= "/-/mixin/" + creator + "/" + str(doc_id)
        jData['OCCI_Description']= description
        jData['Type']= "Mixin"
        provider = {"local":[],"remote":[]}
        jData['Provider']= provider
        try:
            database[doc_id] = jData
            logger.debug("Document has been successfully added to database : " + jData["Location"])
            return jData["Location"],return_code['OK']
        except Exception as e:
            logger.error(e.message)
            return e.message,return_code['Internal Server Error']

    def update_mixin(self,doc_id=None,user_id=None,new_Data=None):
        """
        update all fields of the document (Can only be done by the creator of the document)
        """
        #Get the old document data from the database
        database = self.server.get_or_create_db(config.Mixin_DB)

        if database.doc_exist(doc_id) is True:
            oldData = database.get(doc_id)
            if oldData['Creator'] == user_id:
                oldData_keys = oldData.keys()
                newData_keys =  new_Data.keys()
                problems = False
                #Update only the fields that exist in the new data
                for key in newData_keys:
                    try:
                        oldData_keys.index(key)
                        oldData[key] = new_Data[key]
                    except Exception:
                        problems = True
                        logger.debug(key + "could not be found")
                        #Keep the record of the keys(=parts) that couldn't be updated
                if problems:
                    message = "Document " + str(doc_id) + " has not been totally updated. Check log for more details"
                else:
                    message = "Document " + str(doc_id) + " has been updated successfully"
                oldData['LastUpdate'] = str(datetime.now())
                #Update the document
                database.save_doc(oldData,force_update = True)
                logger.debug(message)
                return message,return_code['OK']
            else:
                message= "You have no right to update this document"
                logger.debug(message)
                return message,return_code['Unauthorized']

        else:
            message = "Document " + str(doc_id) + "couldn\'t be found"
            logger.debug(message)
            return message,return_code['Resource not found']



    def delete_mixin_document(self,doc_id=None,user_id=None):
        """
        Delete the document that is related to the id provided (Can only be done by the creator of the document)
        """
        database = self.server.get_or_create_db(config.Mixin_DB)
        #Verify the existence of such document
        if database.doc_exist(doc_id) is True:
        #If so then delete
            try:
                Data = database.get(doc_id)
                if Data['Creator'] == user_id:
                    database.delete_doc(doc_id)
                    message = "Document " + str(doc_id) + " has been successfully deleted "
                    logger.debug(message)
                    return message,return_code['OK']
                else:
                    message = "You have no right to delete this document"
                    logger.debug(message)
                    return message,return_code['Unauthorized']
            except Exception as e:
                logger.debug(e.message)
                return e.message,return_code['Internal Server Error']

        else:
            #else reply with document not found
            message = "Document " + str(doc_id) + " not found"
            logger.debug(message)
            return message,return_code['Resource not found']


class ActionManager:
    """

    Action records management on couch database

    """

    def __init__(self):

        try:
            self.server = Server('http://' + str(DB_server_IP) + ':' + str(DB_server_PORT))
        except Exception:
            logger.error("Database is unreachable")
            raise Exception("Database is unreachable")
        try:
            self.add_design_action_docs_to_db()
        except Exception as e:
            logger.debug(e.message)


    def add_design_action_docs_to_db(self):
        """
        Add admin design documents to database.
        """
        design_doc = {
            "_id": "_design/get_action",
            "language": "javascript",
            "type": "DesignDoc",
            "views": {
                "all": {
                    "map": "(function(doc) { emit(doc._id, doc.Description) });"
                }
            }

        }
        database = self.server.get_or_create_db(config.Action_DB)
        if database.doc_exist(design_doc['_id']):
            pass
        else:
            database.save_doc(design_doc)


    def get_action_by_id(self,doc_id=None):
        """
        returns the action matching the id provided in the request
        """
        database = self.server.get_or_create_db(config.Action_DB)
        #if the doc_id is specified then only one action will be returned if it exists
        if database.doc_exist(doc_id):
            res =""
            elem = database.get(doc_id)
            res = elem['OCCI_Description']
            logger.debug("Action found")
            return res,return_code['OK']
        else:
            message = "Action " + str(doc_id) + " does not exist"
            logger.debug(message)
            return message,return_code['Resource not found']

    def get_all_actions(self):
        """
        Returns all actions stored in database
        """
        database = self.server.get_or_create_db(config.Action_DB)
        query = database.view('/get_action/all')
        var = list()
        #Extract action descriptions from the dictionary
        try:
            for elem in query:
                var.append(elem['value'])
            logger.debug("Actions found")
            return var,return_code['OK']
        except Exception as e:
            logger.error(e.message)
            return e.message, return_code['Internal Server Error']


    def register_action(self,creator,description):

        """
        Add a new action to the database
        """
        database = self.server.get_or_create_db(config.Action_DB)
        doc_id = uuid_Generator.get_UUID()
        jData = dict()
        jData['Creator'] = creator
        jData['CreationDate'] = str(datetime.now())
        jData['LastUpdate'] = ""
        jData['Location']= "/-/action/" + creator + "/" + str(doc_id)
        jData['OCCI_Description']= description
        jData['Type']= "Action"
        provider = {"local":[],"remote":[]}
        jData['Provider']= provider
        try:
            database[doc_id] = jData
            logger.debug("Document has been successfully added to database : " + jData["Location"])
            return jData["Location"],return_code['OK']
        except Exception as e:
            logger.error(e.message)
            return e.message,return_code['Internal Server Error']

    def update_action(self,doc_id=None,user_id=None,new_Data=None):
        """
        update all fields of the document (Can only be done by the creator of the document)
        """
        #Get the old document data from the database
        database = self.server.get_or_create_db(config.Action_DB)

        if database.doc_exist(doc_id) is True:
            oldData = database.get(doc_id)
            if oldData['Creator'] == user_id:
                oldData_keys = oldData.keys()
                newData_keys =  new_Data.keys()
                problems = False
                #Update only the fields that exist in the new data
                for key in newData_keys:
                    try:
                        oldData_keys.index(key)
                        oldData[key] = new_Data[key]
                    except Exception:
                        problems = True
                        logger.debug(key + "could not be found")
                        #Keep the record of the keys(=parts) that couldn't be updated
                if problems:
                    message = "Document " + str(doc_id) + " has not been totally updated. Check log for more details"
                else:
                    message = "Document " + str(doc_id) + " has been updated successfully"
                oldData['LastUpdate'] = str(datetime.now())
                #Update the document
                database.save_doc(oldData,force_update = True)
                logger.debug(message)
                return message,return_code['OK']
            else:
                message= "You have no right to update this document"
                logger.debug(message)
                return message,return_code['Unauthorized']

        else:
            message = "Document " + str(doc_id) + "couldn\'t be found"
            logger.debug(message)
            return message,return_code['Resource not found']



    def delete_action_document(self,doc_id=None,user_id=None):
        """
        Delete the document that is related to the id provided (Can only be done by the creator of the document)
        """
        database = self.server.get_or_create_db(config.Action_DB)
        #Verify the existence of such document
        if database.doc_exist(doc_id):
        #If so then delete
            try:
                Data = database.get(doc_id)
                if Data['Creator'] == user_id:
                    database.delete_doc(doc_id)
                    message = "Document " + str(doc_id) + " has been successfully deleted "
                    logger.debug(message)
                    return message,return_code['OK']
                else:
                    message = "You have no right to delete this document"
                    logger.debug(message)
                    return message,return_code['Unauthorized']
            except Exception as e:
                logger.error(e.message)
                return e.message,return_code['Internal Server Error']
        else:
            #else reply with document not found
            message = "Document " + str(doc_id) + " not found"
            logger.debug(message)
            return message,return_code['Resource not found']