#  Copyright 2010-2012 Institut Mines-Telecom
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""
Created on Feb 25, 2011

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@contact: Providence Salumu Munga
@organization: Institut Mines-Telecom - Telecom SudParis
@license: Apache License, Version 2.0
"""

import logging.config
from configobj import ConfigObj
from couchdbkit import *
import os


def get_absolute_path_from_relative_path(filename):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), filename))

# Loading the logging configuration file
logging.config.fileConfig(get_absolute_path_from_relative_path("../OCCILogging.conf"))
logger = logging.getLogger("OCCILogging")

# Loading the OCCI server configuration file
config = ConfigObj(get_absolute_path_from_relative_path("../occi_server.conf"))
OCNI_IP = config['OCNI_IP']
OCNI_PORT = config['OCNI_PORT']

# Loading the DB server configuration file
DB_config = ConfigObj(get_absolute_path_from_relative_path("../couchdb_server.conf"))
DB_IP = DB_config['CouchDB_IP']
DB_PORT = DB_config['CouchDB_PORT']
PyOCNI_DB = DB_config['CouchDB_PyOCNI']
PyOCNI_Server_Address = 'http://' + str(OCNI_IP) + ':' + str(OCNI_PORT)

# ======================================================================================
# HTTP Return Codes
# ======================================================================================
return_code = {'OK': 200,
               'OK, and location returned': 201,
               'Accepted': 202,
               'OK, but no content returned': 204,
               'Bad Request': 400,
               'Unauthorized': 401,
               'Forbidden': 403,
               'Not Found': 404,
               'Method Not Allowed': 405,
               'Not Acceptable': 406,
               'Conflict': 409,
               'Gone': 410,
               'Unsupported Media Type': 415,
               'Internal Server Error': 500,
               'Not Implemented': 501,
               'Service Unavailable': 503}

# ======================================================================================
#                                   PyOCNI database
# ======================================================================================

design_doc = {
    "_id": "_design/db_views",
    "language": "javascript",
    "type": "DesignDoc",
    "views": {
        "for_get_categories": {
            "map": "(function(doc) { if ((doc.Type == \"Kind\")||(doc.Type == \"Mixin\")||(doc.Type == \"Action\")) "
                   "emit (doc.Type, doc.OCCI_Description) });"
        },
        "for_update_categories": {
            "map": "(function(doc) { if ((doc.Type == \"Kind\")||(doc.Type == \"Mixin\")||(doc.Type == \"Action\")) "
                   "emit (doc.OCCI_ID,doc) });"
        },
        "for_associate_mixin": {
            "map": "(function(doc) { if ((doc.Type == \"Resource\")||(doc.Type == \"Link\"))"
                   " emit([doc.OCCI_Location,],doc);});"
        },
        "for_delete_categories": {
            "map": "(function(doc) { if ((doc.Type == \"Kind\")||(doc.Type == \"Mixin\")||(doc.Type == \"Action\"))"
                   "emit(doc._id,[doc._rev,doc.OCCI_ID])});"
        },
        "for_register_categories": {
            "map": "(function(doc) { if ((doc.Type == \"Kind\")||(doc.Type == \"Mixin\")||(doc.Type == \"Action\")) "
                   "emit (doc.OCCI_ID,doc.OCCI_Location) });"
        },
        "for_register_entities": {
            "map": "(function(doc) { emit (doc.OCCI_ID,doc.OCCI_Location) });"
        },
        "for_get_entities": {
            "map": "(function(doc) { if ((doc.Type == \"Kind\")||(doc.Type == \"Mixin\"))"
                   "emit (doc.OCCI_Location,[doc.OCCI_ID,doc.Type]) });"
        },
        "entities_of_kind": {
            "map": "(function(doc) { if ((doc.Type == \"Resource\")||(doc.Type == \"Link\"))"
                   "emit (doc.OCCI_Description.kind,[doc.OCCI_Location,doc.Type]) });"
        },
        "entities_of_mixin": {
            "map": "(function(doc) { if ((doc.Type == \"Resource\")||(doc.Type == \"Link\"))"
                   "{for (elem in doc.OCCI_Description.mixins) "
                   "emit (doc.OCCI_Description.mixins[elem],[doc.OCCI_Location,doc.Type]) }});"
        },
        "for_get_filtered": {
            "map": "(function(doc) { if ((doc.Type == \"Resource\")||(doc.Type == \"Link\"))"
                   "emit (doc.OCCI_Location,[doc.OCCI_Description,doc.Type]) });"
        },
        "my_mixins": {
            "map": "(function(doc) { if (doc.Type == \"Mixin\")"
                   "emit (doc.OCCI_Location,doc.OCCI_ID) });"
        },
        "my_resources": {
            "map": "(function(doc) {if ((doc.Type == \"Resource\")||(doc.Type == \"Link\"))"
                   "emit (doc.OCCI_Location,[doc.Type, doc.OCCI_Description]) });"
        },
        "for_update_entities": {
            "map": "(function(doc) { if ((doc.Type == \"Resource\")||(doc.Type == \"Link\")) "
                   "emit (doc.OCCI_Location,doc)});"
        },
        "entities_of_mixin_v2": {
            "map": "(function(doc) { if ((doc.Type == \"Resource\")||(doc.Type == \"Link\"))"
                   "{for (elem in doc.OCCI_Description.mixins)"
                   "emit (doc.OCCI_Description.mixins[elem],doc) }});"
        },
        "for_trigger_action": {
            "map": "(function(doc) { if ((doc.Type == \"Resource\")||(doc.Type == \"Link\"))"
                   "emit ([doc.OCCI_Location,],[doc.OCCI_Description.kind,doc.OCCI_Description.mixins]) });"
        },
        "actions_of_kind_mix": {
            "map": "(function(doc) { if ((doc.Type == \"Kind\")||(doc.Type == \"Mixin\"))"
                   "{doc_id = doc.OCCI_Description.scheme + doc.OCCI_Description.term; "
                   "for (elem in doc.OCCI_Description.actions) "
                   "emit ([doc.OCCI_Description.actions[elem],doc_id],doc.Provider) }});"
        },
        "my_providers": {
            "map": "(function(doc) { if (doc.Type == \"Kind\")"
                   "emit (doc.OCCI_ID,doc.Provider)});"
        },
        "get_default_attributes_from_kind": {
            "map": "(function(doc) { if (doc.Type == \"Kind\")"
                   "emit (doc.OCCI_Location,doc.OCCI_Description.attributes)});"
        }


    }

}

def prepare_PyOCNI_db():
    """
    Start the server, get the database and add Category design documents to it.
    """
    try:
        server = Server('http://' + str(DB_IP) + ':' + str(DB_PORT))
        database = server.get_or_create_db(PyOCNI_DB)
        database.save_doc(design_doc, force_update=True)
        return database
    except Exception as e:
        logger.error("===== Prepare_PyOCNI_db : Database prepare has failed " + e.message + "=====")


def get_PyOCNI_db():
    """
    Start the server and get the database.
    """
    try:
        server = Server('http://' + str(DB_IP) + ':' + str(DB_PORT))
        database = server.get_or_create_db(PyOCNI_DB)
        return database
    except Exception as e:
        logger.error("===== Get_PyOCNI_db : Database prepare has failed " + e.message + "=====")


def purge_PyOCNI_db():
    try:
        server = Server('http://' + str(DB_IP) + ':' + str(DB_PORT))
        server.delete_db(PyOCNI_DB)
    except Exception as e:
        logger.error("===== Purge_PyOCNI_db: Database purge has failed + " + e.message + "=====")

def check_db():
     s = Server('http://' + str(DB_IP) + ':' + str(DB_PORT))
     if len(s.info())>0:
        logger.info("===== The DB is ON  =====" + str(s.info()))
        return 1
     else:
        logger.warning("===== The DB is OFF:  ")
        return 0

        #=======================================================================================================================
        #
        #        "my_occi_locations":{
        #            "map": "(function(doc) {emit (doc.OCCI_Location,) });"
        #        }

        #"for_delete_entities" :{
        #                           "map": "(function(doc) {if ((doc.Type == \"Resource\")||(doc.Type == \"Link\"))"
        #                                  "emit (,[doc.OCCI_Location,doc._id,doc._rev]) });"
        #                       },