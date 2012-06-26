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
Created on Feb 25, 2011

@author: Houssem Medhioub, Providence Salumu Munga
@contact: houssem.medhioub@it-sudparis.eu
@author: Bilel Msekni (Database configuration)
@organization: Institut Mines-Telecom - Telecom SudParis
@version: 0.3
@license: LGPL - Lesser General Public License

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
# Prepare the PyOCNI database
# ======================================================================================

def prepare_PyOCNI_db():
    """
    Start the server, get the database and add Category design documents to it.
    """
    try:
        server = Server('http://' + str(DB_IP) + ':' + str(DB_PORT))
    except Exception:
        logger.error("CategoryManager : Database is unreachable")
        raise Exception("Database is unreachable")
    database = server.get_or_create_db(PyOCNI_DB)
    design_doc = {
        "_id": "_design/get_views",
        "language": "javascript",
        "type": "DesignDoc",
        "views": {
            "occi_id_occi_location": {
                "map": "(function(doc){emit(doc.OCCI_ID,doc.OCCI_Location)});"
            },
            "type_occi_desc":{
                "map":"(function(doc) { emit (doc.Type, doc.OCCI_Description) });"
            },
            "_id_rev_occi_id_creator": {
                "map": "(function(doc) { emit (doc._id,[doc._rev,doc.OCCI_ID, doc.Creator]) });"
            },
            "occi_id_doc": {
                "map": "(function(doc) { emit (doc.OCCI_ID,doc) });"
            },
            "occi_location_doc": {
                "map": "(function(doc) { emit (doc.OCCI_Location,doc) });"
            }

        }

    }
    database.save_doc(design_doc,force_update=True)
    return database

def purge_PyOCNI_db():

    try:
        server = Server('http://' + str(DB_IP) + ':' + str(DB_PORT))
    except Exception:
        logger.error("Database is unreachable")

    try:
        server.get_db(PyOCNI_DB).flush()
    except Exception:
        logger.debug("No DB named: '" + PyOCNI_DB + "' to delete.")
        server.create_db(PyOCNI_DB)