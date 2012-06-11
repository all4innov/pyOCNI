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

from couchdbkit import *

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












