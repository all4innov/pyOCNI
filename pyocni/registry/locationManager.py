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
Created on Jun 12, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@version: 0.2
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

def purgeLocationDBs():
    """
    Delete resource and link databases
    """
    try:
        server = Server('http://' + str(DB_server_IP) + ':' + str(DB_server_PORT))
    except Exception:
        logger.error("Database is unreachable")
    try:
        server.flush(config.Resource_DB)

    except Exception:
        logger.debug("No DB named: '" + config.Resource_DB + "' to delete")
        server.create_db(config.Resource_DB)
    try:
        server.flush(config.Link_DB)
    except Exception:
        logger.debug("No DB named: '" + config.Link_DB + "' to delete")
        server.create_db(config.Link_DB)



class ResourceManager(object):
    """
    Manager of resource documents in the couch database.
    """

    def __init__(self):

        try:
            self.server = Server('http://' + str(DB_server_IP) + ':' + str(DB_server_PORT))
        except Exception:
            logger.error("Database is unreachable")
            raise Exception("Database is unreachable")
        try:
            self.add_design_resource_docs_to_db()
        except Exception as e:
            logger.debug(e.message)

    def add_design_resource_docs_to_db(self):
        """
        Add resource design documents to database.
        """
        design_doc = {
            "_id": "_design/get_resource",
            "language": "javascript",
            "type": "DesignDoc",
            "views": {
                "all": {
                    "map": "(function(doc) { emit(doc._id, doc.OCCI_Description) });"
                }
            }

        }
        database = self.server.get_or_create_db(config.Resource_DB)
        if database.doc_exist(design_doc['_id']):
            pass
        else:
            database.save_doc(design_doc)

    def get_resource_by_id(self,doc_id=None):

        """
        Returns the OCCI resource description contained inside the resource document matching the doc_id provided
        Args:
            @param doc_id: id of the resource document to be retrieved
            @return : <dict> OCCI description of the resource

        """
        database = self.server.get_or_create_db(config.Resource_DB)
        #if the doc_id exists then the resource description will be returned
        if database.doc_exist(doc_id):
            elem = database.get(doc_id)
            res = elem['OCCI_Description']
            logger.debug("Resource document " + str(doc_id) + " is found")
            return res,return_code['OK']
        else:
            message = "Resource document " + str(doc_id) + " does not exist"
            logger.debug(message)
            return message,return_code['Resource not found']

    def get_all_resources(self):
        """
        Returns all OCCI descriptions of the resources contained inside resource documents stored in the database
        Args:
            @return : <dict> All OCCI resource descriptions

        """
        database = self.server.get_or_create_db(config.Resource_DB)
        query = database.view('/get_resource/all')
        var = list()
        #Extract resource descriptions from the dictionary
        try:
            for elem in query:
                var.append(elem['value'])
            logger.debug("Resources found")
            return var,return_code['OK']
        except Exception as e:
            logger.error(e.message)
            return e.message,return_code['Internal Server Error']

    def register_resource(self,creator,description):

        """
        Add a new resource to the database
        Args:
            @param creator: the user who created this new resource
            @param description: the OCCI description of the new resource
        """

        database = self.server.get_or_create_db(config.Resource_DB)
        doc_id = uuid_Generator.get_UUID()
        ok, loc = joker.make_resource_location(description,doc_id,creator)
        if ok is True:
            jData = dict()
            jData['Creator'] = creator
            jData['CreationDate'] = str(datetime.now())
            jData['LastUpdate'] = ""
            jData['Location']= loc
            jData['OCCI_Description']= description
            jData['Type']= "Resource"
            provider = {"local":[],"remote":[]}
            jData['Provider']= provider
            try:
                database[doc_id] = jData
                logger.debug("Resource document has been successfully added to database : " + loc)
                return loc,return_code['OK']
            except Exception as e:
                logger.error(e.message)
                return e.message,return_code['Internal Server Error']
        else:
            logger.error(loc)
            return loc,return_code['Internal Server Error']

    def update_resource(self,doc_id=None,user_id=None,new_Data=None):
        """
        Update all fields of the resource document (Can only be done by the creator of the document)
        Args:
            @param doc_id: id of the resource document
            @param user_id: id of the issuer of update request
            @param new_Data: the new data that will be used to update the old data
        """
        #Get the old document data from the database
        database = self.server.get_or_create_db(config.Resource_DB)

        if database.doc_exist(doc_id) is True:
            oldData = database.get(doc_id)
            if oldData['Creator'] == user_id:
                oldData_keys = oldData.keys()
                newData_keys =  new_Data.keys()
                problems = False
                for key in newData_keys:
                    try:
                        #OCCI_Description field will be treated separately
                        if key == "OCCI_Description":
                            old_descrip = oldData[key]['resources'][0]
                            new_descrip = new_Data[key]['resources'][0]
                            problems,oldData[key]['resources'][0] = joker.update_occi_description(old_descrip,new_descrip)
                        else:
                            oldData_keys.index(key)
                            oldData[key] = new_Data[key]
                    except Exception:
                        problems = True
                        logger.debug(key + "could not be found")
                        #Keep the record of the keys(=parts) that couldn't be update
                if problems is True:
                    message = "Resource document " + str(doc_id) + " has not been totally updated. Check log for more details"
                else:
                    message = "Resource document " + str(doc_id) + " has been updated successfully"
                oldData['LastUpdate'] = str(datetime.now())
                #Update the resource document
                database.save_doc(oldData,force_update = True)
                logger.debug(message)
                return message,return_code['OK']
            else:
                message= "You have no right to update this resource document"
                logger.debug(message)
                return message,return_code['Unauthorized']

        else:
            message = "Resource document " + str(doc_id) + " couldn\'t be found"
            logger.debug(message)
            return message,return_code['Resource not found']

    def delete_resource_document(self,doc_id=None,user_id=None):
        """
        Delete the resource document that is related to the id provided (Can only be done by the creator of the document)
        Args:
            @param doc_id: id of the resource document
            @param user_id: id of the issuer of the delete request
        """
        database = self.server.get_or_create_db(config.Resource_DB)
        #Verify the existence of such resource document
        if database.doc_exist(doc_id):
        #If so then delete
            try:
                Data = database.get(doc_id)
                if Data['Creator'] == user_id:
                    database.delete_doc(doc_id)
                    message = "Resource document " + str(doc_id) + " has been successfully deleted "
                    logger.debug(message)
                    return message,return_code['OK']
                else:
                    message = "You have no right to delete this resource document"
                    logger.debug(message)
                    return message,return_code['Unauthorized']
            except Exception as e:
                logger.error(e.message)
                return e.message,return_code['Internal Server Error']
        else:
            #else reply with resource document not found
            message = "Resource document " + str(doc_id) + " not found"
            logger.debug(message)
            return message,return_code['Resource not found']

class LinkManager(object):
    """
    Manager of link documents in the couch database.
    """

    def __init__(self):

        try:
            self.server = Server('http://' + str(DB_server_IP) + ':' + str(DB_server_PORT))
        except Exception:
            logger.error("Database is unreachable")
            raise Exception("Database is unreachable")
        try:
            self.add_design_link_docs_to_db()
        except Exception as e:
            logger.debug(e.message)

    def add_design_link_docs_to_db(self):
        """
        Add link design documents to database.
        """
        design_doc = {
            "_id": "_design/get_link",
            "language": "javascript",
            "type": "DesignDoc",
            "views": {
                "all": {
                    "map": "(function(doc) { emit(doc._id, doc.OCCI_Description) });"
                }
            }

        }
        database = self.server.get_or_create_db(config.Link_DB)
        if database.doc_exist(design_doc['_id']):
            pass
        else:
            database.save_doc(design_doc)

    def get_link_by_id(self,doc_id=None):

        """
        Returns the OCCI link description contained inside the document matching the doc_id provided
        Args:
            @param doc_id: id of the link document to be retrieved
            @return : <dict> OCCI description of the link

        """
        database = self.server.get_or_create_db(config.Link_DB)
        #if the doc_id exists then the link description will be returned
        if database.doc_exist(doc_id):
            elem = database.get(doc_id)
            res = elem['OCCI_Description']
            logger.debug("Link document" + str(doc_id) + " is found")
            return res,return_code['OK']
        else:
            message = "Link document" + str(doc_id) + " does not exist"
            logger.debug(message)
            return message,return_code['Resource not found']

    def get_all_links(self):
        """
        Returns all OCCI descriptions of the links contained inside documents stored in the database
        Args:
            @return : <dict> All OCCI link descriptions

        """
        database = self.server.get_or_create_db(config.Link_DB)
        query = database.view('/get_link/all')
        var = list()
        #Extract link descriptions from the dictionary
        try:
            for elem in query:
                var.append(elem['value'])
            logger.debug("Link documents found")
            return var,return_code['OK']
        except Exception as e:
            logger.error(e.message)
            return e.message,return_code['Internal Server Error']

    def register_link(self,creator,description):

        """
        Add a new link to the database
        Args:
            @param creator: the user who created this new link
            @param description: the OCCI description of the new link
        """

        database = self.server.get_or_create_db(config.Link_DB)
        doc_id = uuid_Generator.get_UUID()
        ok, loc = joker.make_link_location(description,doc_id,creator)
        if ok is True:
            jData = dict()
            jData['Creator'] = creator
            jData['CreationDate'] = str(datetime.now())
            jData['LastUpdate'] = ""
            jData['Location']= loc
            jData['OCCI_Description']= description
            jData['Type']= "Link"
            provider = {"local":[],"remote":[]}
            jData['Provider']= provider
            try:
                database[doc_id] = jData
                logger.debug("Link document has been successfully added to database : " + loc)
                return loc,return_code['OK']
            except Exception as e:
                logger.error(e.message)
                return e.message,return_code['Internal Server Error']
        else:
            logger.error(loc)
            return loc,return_code['Internal Server Error']

    def update_link(self,doc_id=None,user_id=None,new_Data=None):
        """
        Update all fields of the link document (Can only be done by the creator of the document)
        Args:
            @param doc_id: id of the link document
            @param user_id: id of the issuer of update request
            @param new_Data: the new data that will be used to update the old data
        """
        #Get the old document data from the database
        database = self.server.get_or_create_db(config.Link_DB)

        if database.doc_exist(doc_id) is True:
            oldData = database.get(doc_id)
            if oldData['Creator'] == user_id:
                oldData_keys = oldData.keys()
                newData_keys =  new_Data.keys()
                problems = False
                for key in newData_keys:
                    try:
                        #OCCI_Description field will be treated separately
                        if key == "OCCI_Description":
                            old_descrip = oldData[key]['links'][0]
                            new_descrip = new_Data[key]['links'][0]
                            problems,oldData[key]['links'][0] = joker.update_occi_description(old_descrip,new_descrip)
                        else:
                            oldData_keys.index(key)
                            oldData[key] = new_Data[key]
                    except Exception:
                        problems = True
                        logger.debug(key + "could not be found")
                        #Keep the record of the keys(=parts) that couldn't be update
                if problems:
                    message = "Link document " + str(doc_id) + " has not been totally updated. Check log for more details"
                else:
                    message = "Link Document " + str(doc_id) + " has been updated successfully"
                oldData['LastUpdate'] = str(datetime.now())
                #Update the document
                database.save_doc(oldData,force_update = True)
                logger.debug(message)
                return message,return_code['OK']
            else:
                message= "You have no right to update this link document"
                logger.debug(message)
                return message,return_code['Unauthorized']

        else:
            message = "Link document " + str(doc_id) + " couldn\'t be found"
            logger.debug(message)
            return message,return_code['Resource not found']

    def delete_link_document(self,doc_id=None,user_id=None):
        """
        Delete the link document that is related to the id provided (Can only be done by the creator of the document)
        Args:
            @param doc_id: id of the link document
            @param user_id: id of the issuer of the delete request
        """
        database = self.server.get_or_create_db(config.Link_DB)
        #Verify the existence of such link document
        if database.doc_exist(doc_id):
        #If so then delete
            try:
                Data = database.get(doc_id)
                if Data['Creator'] == user_id:
                    database.delete_doc(doc_id)
                    message = "Link document " + str(doc_id) + " has been successfully deleted "
                    logger.debug(message)
                    return message,return_code['OK']
                else:
                    message = "You have no right to delete this link document"
                    logger.debug(message)
                    return message,return_code['Unauthorized']
            except Exception as e:
                logger.error(e.message)
                return e.message,return_code['Internal Server Error']
        else:
            #else reply with link document not found
            message = "Link document " + str(doc_id) + " not found"
            logger.debug(message)
            return message,return_code['Resource not found']







