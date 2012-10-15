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

import logging.config
from configobj import ConfigObj
from couchdbkit import *
import os

def get_absolute_path_from_relative_path(filename):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), filename))



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

class PostMan():

    def __init__(self):

        try:
            server = Server('http://' + str(DB_IP) + ':' + str(DB_PORT))
        except Exception:
            raise Exception("Database is unreachable")

        self.database = server.get_db(PyOCNI_DB)

    def save_registered_docs_in_db(self,docs):

        self.database.save_docs(docs,use_uuids=True, all_or_nothing=True)

    def save_updated_docs_in_db(self, categories):

        self.database.save_docs(categories,force_update=True, all_or_nothing=True)

    def save_deleted_categories_in_db(self, categories,to_update):

        self.database.delete_docs(categories)
        self.database.save_docs(to_update,force_update=True, all_or_nothing=True)

    def save_custom_resource(self, entity):

        self.database.save_doc(entity,use_uuids=True, all_or_nothing=True)

    def delete_single_resource_in_db(self, res_value):

        self.database.delete_doc(res_value)


