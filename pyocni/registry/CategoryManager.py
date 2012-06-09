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
from pyocni.pyocni_tools import UUID_Generator
from couchdbkit import *

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

        CRUD operation on kind

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
            res = elem['Description']
            logger.debug("Kind found")
            return res
        else:
            message = "Document " + str(doc_id) + " have no match"
            logger.debug(message)
            return message

    def get_all_kinds(self):
        """
        Returns all documents stored in database
        """
        database = self.server.get_or_create_db(config.Kind_DB)
        query = database.view('/get_kind/all')
        var = list()
        #Extract kind descriptions from the dictionary
        for elem in query:
            var.append(elem['value'])
        logger.debug("Kinds found")
        return var
    def register_kind(self,creator,description):

        """
        Add a new kind to the database
        """
        database = self.server.get_or_create_db(config.Kind_DB)
        doc_id = UUID_Generator.get_UUID()
        jData = dict()
        jData["Creator"]= creator
        jData["CreationDate"]= str(datetime.now())
        jData["Location"]= "/-/kind/" + creator + "/" + str(doc_id)
        jData["Description"]= description
        jData["Type"]= "Kind"
        provider = {"local":[],"remote":[]}
        jData["Provider"]= provider
        try:
            database[doc_id] = jData
            logger.debug("Document has been successfully added to database : " + jData["Location"])
            return jData["Location"]
        except Exception as e:
            logger.error(e.message)
            raise Exception(" A problem has occured")

    def update_part_of_kind(self,doc_id,newData,j_oldData,newData_keys):
        """
        update only a part of the kind description (can be called only after a failed try to fully update the kind description)
        """
        database = self.server.get_or_create_db(config.Kind_DB)
        #Try to change parts of the kind description
        oldData_keys =  j_oldData['kinds'][0].keys()
        problems = False
        for key in newData_keys:
            try:
                oldData_keys.index(key)
                j_oldData['kinds'][0][key] = newData[key]
            except Exception:
                #Keep the record of the keys(=parts) that couldn't be updated
                logger.debug(key + 'could not be found')
                problems = True
        if problems:
            message = "Document " + str(doc_id) + " has not been totally updated. Check log for more details"
        else:
            message = "Document " + str(doc_id) + " has been updated successfully"
        return j_oldData,message

    def update_kind(self,doc_id=None,new_Data=None):
        """
        update all of the kind description
        """
        #Get the old kind data from the database
        database = self.server.get_or_create_db(config.Kind_DB)
        oldData = database.get(doc_id)
        if oldData is not None:
            j_oldData = oldData['Description']
            newData_keys =  new_Data.keys()
            #Try to change the hole kind description
            try:
                val = newData_keys.index('kinds')
                j_oldData['kinds'] = new_Data['kinds']
                oldData['Description'] = j_oldData
                mesg = "Document " + str(doc_id) + " has been updated successfully"
            except Exception:
                res,mesg = self.update_part_of_kind(doc_id,new_Data,j_oldData,newData_keys)
                oldData['Description'] = res
            #Update the document
            database.save_doc(oldData,force_update = True)
            return mesg
        else:
            return 'Document ' + str(doc_id) + 'couldn\'t be found'



    def delete_document(self,doc_id):
        database = self.server.get_or_create_db(config.Kind_DB)
        #Verify the existence of such document
        if database.doc_exist(doc_id):
        #If so then delete
            try:
                database.delete_doc(doc_id)
                message = "Document " + str(doc_id) + " has been successfully deleted "
                logger.debug(message)
                return message
            except Exception as e:
                return e.message
        else:
            #else reply with kind not found
            message = "Document " + str(doc_id) + " not found"
            logger.debug(message)
            return message
