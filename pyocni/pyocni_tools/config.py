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

import os

from pyocni.pyocni_tools.arguments import Parameters

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
Kind_DB = DB_config['CouchDB_Kind']
Action_DB = DB_config['CouchDB_Action']
Mixin_DB = DB_config['CouchDB_Mixin']
Resource_DB = DB_config['CouchDB_Resource']
Link_DB = DB_config['CouchDB_Link']

# ======================================================================================
# HTTP Return Codes
# ======================================================================================
return_code = {'OK': "200",
               'OK, and location returned': "201",
               'Accepted': "202",
               'OK, but no content returned': "204",
               'OK, but there were some problems': "205",
               'Bad Request': "400",
               'Unauthorized': "401",
               'Forbidden': "403",
               'Not Found': "404",
               'Method Not Allowed': "405",
               'Not Acceptable': "406",
               'Conflict': "409",
               'Gone': "410",
               'Unsupported Media Type': "415",
               'Internal Server Error': "500",
               'Not Implemented': "501",
               'Service Unavailable': "503"}
