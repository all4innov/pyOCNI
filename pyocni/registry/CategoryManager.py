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
import couchdb
import base64
# getting the Logger
logger = config.logger


# Get the database server configuration

DB_server_IP = config.DB_IP
DB_server_PORT = config.DB_PORT

entity_children = Enum("resources","links")


def purgeCategoryDBs():

    try:
        server = couchdb.Server('http://' + str(DB_server_IP) + ':' + str(DB_server_PORT))
    except Exception:
        logger.error("Database is unreachable")

    try:
        del server[config.Kind_DB]
        server.create(config.Kind_DB)
    except Exception:
        logger.debug("No DB named: '" + config.Kind_DB + "' to delete.")
        server.create(config.Kind_DB)
    try:
        del server[config.Action_DB]
        server.create(config.Action_DB)
    except Exception:
        logger.debug("No DB named: '" + config.Action_DB + "' to delete")
        server.create(config.Action_DB)
    try:
        del server[config.Mixin_DB]
        server.create(config.Mixin_DB)
    except Exception:
        logger.debug("No DB named: '" + config.Mixin_DB + "' to delete")
        server.create(config.Mixin_DB)

class KindManager:
    """

        CRUD operation on kind

    """


    def __init__(self,req, id=None,user_id=None):

        self.req = req
        self.id=id
        self.user_id=user_id
        self.res = Response()
        self.res.content_type = req.accept
        self.res.server = 'ocni-server/1.1 (linux) OCNI/1.1'
        try:
            self.server = couchdb.Server('http://' + str(DB_server_IP) + ':' + str(DB_server_PORT))
        except Exception:
            logger.error("Database is unreachable")
            self.res.body = "Nothing has been added to the database, please check log for more informations"
        try:
            self.server.create(config.Kind_DB)
        except Exception:
            logger.debug("Database '" + config.Kind_DB + "' already exists")


    def get(self):

        """
        Retrieval of registered Kinds that belongs to the user_id
        """

        _kind_values = list()

        #retrieve all kinds from the KindDB

        #convert _kind_values to json

        self.res.body = None

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
            raise ValueError("Unknown content type")

        #Decode authorization header to get the user_id
        var,user_id = self.req.authorization
        user_id = base64.decodestring(user_id)
        user_id = user_id.split(':')[0]
        #Some modification to the request body are needed
        self.req.body=self.req.body.strip()
        self.req.body = self.req.body[1:]
        #add the JSON to database
        jData = dict()
        jData["KindDescription"]= self.req.body
        jData["Creator"]= user_id
        jData["CreationDate"]= str(datetime.now())

        self.server[config.Kind_DB].save(jData)
        self.res.body = "A new kind has been successfully added to database"

        return self.res

    def put(self):
        """
        Update a kind using the id and user_id attributes

        """
        return 'QueryInterface response from PUT '

    def delete(self):
        """

        Delete a kind using the id and user_id attributes

        """
        return 'QueryInterface response from DELETE'
