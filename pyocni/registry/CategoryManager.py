# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

# Copyright (C) 2012 Bilel Msekni - Institut Mines-Telecom
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

from webob import Request, Response
from pyocni.pyocni_tools.Enum import Enum

import pyocni.pyocni_tools.config as config
try:
    import simplejson as json
except ImportError:
    import json
from datetime import datetime
from pyocni.pyocni_tools import UUID_Generator
from couchdbkit import *
from pprint import *
import base64

# getting the Logger
logger = config.logger


# Get the database server configuration

DB_server_IP = config.DB_IP
DB_server_PORT = config.DB_PORT

entity_children = Enum("resources","links")

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

        CRUD operation on kind

    """


    def __init__(self,req, doc_id=None,user_id=None):

        self.req = req
        self.doc_id=doc_id
        self.user_id=user_id
        self.res = Response()
        self.res.content_type = req.accept
        self.res.server = 'ocni-server/1.1 (linux) OCNI/1.1'
        try:
            self.server = Server('http://' + str(DB_server_IP) + ':' + str(DB_server_PORT))
        except Exception:
            logger.error("Database is unreachable")
            self.res.body = "Nothing has been added to the database, please check log for more details"
            self.res.status_code = return_code["Internal Server Error"]
        try:
            self.database = self.server.get_or_create_db(config.Kind_DB)
            self.add_design_doc_to_db()
        except Exception as e:
            logger.debug(e.message)


    def add_design_doc_to_db(self):

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
        if self.database.doc_exist(design_doc['_id']):
            pass
        else:
            self.database.save_doc(design_doc)


    def get(self):

        """
        Retrieval of all registered Kinds or just one kind
        """
        #if the doc_id is specified then only one kind will be returned if it exists
        if self.doc_id is not None:
            if self.database.doc_exist(self.doc_id):
                elem = self.database.get(self.doc_id)
                self.res.body = json.dumps(elem['Description'])
                self.res.status = return_code['OK']
                return self.res
            else:
                self.res.body = self.doc_id + 'have no match'
                self.res.body = return_code['Resource not found']
                return self.res
        #No doc_id specified, all kinds will be returned
        else:
            query = self.database.view('/get_kind/all')
            var = list()
            #Extract kind description from the dictionary
            for elem in query:
                var.append(elem['value'])
            #Convert the list into JSON
            self.res.body = json.dumps(var)
            self.res.status_code = return_code['OK']
            return self.res

    def post(self):
        """
        Create a new kind

        """
        #Detect the body type (HTTP or JSON)
        if self.req.content_type == "text/occi" or self.req.content_type == "text/plain" or self.req.content_type == "text/uri-list":
            # Solution 1 : convert to Json then validate
            # Solution 2  (To adopt) : Validate HTTP then convert to JSON
            pass
        elif self.req.content_type =="application/occi+json":
            #Validate the JSON message
            pass
        else:
            logger.error(self.req.content_type + " is an unknown request content type")
            self.res.status_code = return_code["Unsupported Media Type"]
            self.res.body = self.req.content_type + " is an unknown request content type"
            return self.res

        #Decode authorization header to get the user_id
        var,user_id = self.req.authorization
        user_id = base64.decodestring(user_id)
        user_id = user_id.split(':')[0]
        jBody = json.loads(self.req.body)
        #add the JSON to database along with other attributes
        doc_id = UUID_Generator.get_UUID()
        jData = dict()
        jData["Creator"]= user_id
        jData["CreationDate"]= str(datetime.now())
        jData["Location"]= "/-/kind/" + user_id + "/" + str(doc_id)
        jData["Description"]= jBody
        jData["Type"]= "Kind"
        try:
            self.database[doc_id] = jData
        except Exception:
            self.database = self.server.get_or_create_db(config.Kind_DB)
            self.database[doc_id] = jData
        kind_location = jData["Location"]
        self.res.body = "A new kind has been successfully added to database : " + kind_location
        self.res.status_code = return_code["OK"]
        return self.res

    def put(self):
        """
        Update a kind using the id and user_id attributes

        """
        #Detect the body type (HTTP or JSON)
        if self.req.content_type == "text/occi" or self.req.content_type == "text/plain" or self.req.content_type == "text/uri-list":
            # Solution 1 : convert to Json then validate
            # Solution 2  (To adopt) : Validate HTTP then convert to JSON
            pass
        elif self.req.content_type =="application/occi+json":
            #Validate the JSON message
            pass
        else:
            logger.error(self.req.content_type + " is an unknown request content type")
            self.res.status_code = return_code["Unsupported Media Type"]
            self.res.body = self.req.content_type + " is an unknown request content type"
            return self.res
        #Get the new data from the request
        j_newData = json.loads(self.req.body)
        #Get the old kind data from the database

        oldData = self.database.get(self.doc_id)
        if oldData is not None:
            j_oldData = oldData['Description']
            newData_keys =  j_newData.keys()
            #Try to change the hole kind description
            try:
                val = newData_keys.index('kinds')
                j_oldData['kinds'] = j_newData['kinds']
            except Exception:
                #Try to change parts of the kind description
                oldData_keys =  j_oldData['kinds'][0].keys()
                problems = False
                for key in newData_keys:
                    try:
                        val = oldData_keys.index(key)
                        j_oldData['kinds'][0][key] = j_newData[key]
                    except Exception:
                        logger.debug(key + 'could not be found')
                        problems = True
            oldData['Description'] = j_oldData
            #Update the document
            self.database.save_doc(oldData,force_update = True)
            if problems:
                self.res.status_code = return_code['Bad Request']
                self.res.body = 'Document ' + str(self.doc_id) + 'has not been totally updated. Check log for more details'
            else:
                self.res.status_code = return_code['OK']
                self.res.body = 'Document ' + str(self.doc_id) + 'has been updated successfully'
        else:
            self.res.body = 'Document ' + str(self.doc_id) + 'couldn\'t be updated'
            self.res.status_code = return_code['Resource not found']
        return self.res


    def delete(self):
        """

        Delete a kind using the doc_id

        """
        #Verify the existence of such kind
        if self.database.doc_exist(self.doc_id):
            #If so then delete
            try:
                self.database.delete_doc(self.doc_id)
                self.res.body = "Kind has been successfully deleted "
                self.res.status_code = return_code['OK']
            except Exception as e:
                return e.message
        else:
            #else reply with kind not found
            self.res.body = "Kind not found"
            self.res.status_code = return_code["Resource not found"]

        return self.res
