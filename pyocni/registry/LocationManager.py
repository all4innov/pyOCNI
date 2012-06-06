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

import pyocni.pyocni_tools.ask_user_details as shell_ask
import pyocni.pyocni_tools.config as config
from pyocni.pyocni_tools.Enum import Enum

try:
    import simplejson as json
except ImportError:
    import json
import os
from couchdbkit import *

# getting the Logger
logger = config.logger


# Get the database server configuration

DB_server_IP = config.DB_IP
DB_server_PORT = config.DB_PORT

entity_children = Enum("resources","links")

def purgeLocationDBs():
    """
    Delete resource and link databases
    """
    try:
        server = Server('http://' + str(DB_server_IP) + ':' + str(DB_server_PORT))
    except Exception:
        logger.error("Database is unreachable")
    try:
        del server[config.Resource_DB]
        server.create_db(config.Resource_DB)

    except Exception:
        logger.debug("No DB named: '" + config.Resource_DB + "' to delete")
        server.create_db(config.Resource_DB)
    try:
        del server[config.Link_DB]
        server.create_db(config.Link_DB)
    except Exception:
        logger.debug("No DB named: '" + config.Link_DB + "' to delete")
        server.create_db(config.Link_DB)


#====================ResourceRegistry====================

class Resource_registry(object):
    """

    A registry containing default Kinds, Mixins, actions and more.

    """
    content = ""

    def __init__(self):
        """
        Initialize databases for the upcoming inputs
        """

        try:
            self.server = Server('http://' + str(DB_server_IP) + ':' + str(DB_server_PORT))
        except Exception:
            logger.error("Database is unreachable")

        # ======================================================================================
        # Reinitialization of the database
        # ======================================================================================

        result = shell_ask.query_yes_no_quit(" \n_______________________________________________________________\n"
                                             "   Do you want to purge all databases (DB  reinitialization)?", "no")
        if result == 'yes':
            try:
                del self.server[config.Kind_DB]
                self.server.create(config.Kind_DB)
            except Exception:
                logger.debug("No DB named: '" + config.Kind_DB + "' to delete.")
                self.server.create(config.Kind_DB)
            try:
                del self.server[config.Action_DB]
                self.server.create(config.Action_DB)
            except Exception:
                logger.debug("No DB named: '" + config.Action_DB + "' to delete")
                self.server.create(config.Action_DB)
            try:
                del self.server[config.Mixin_DB]
                self.server.create(config.Mixin_DB)
            except Exception:
                logger.debug("No DB named: '" + config.Mixin_DB + "' to delete")
                self.server.create(config.Mixin_DB)
            try:
                del self.server[config.Resource_DB]
                self.server.create(config.Resource_DB)
            except Exception:
                logger.debug("No DB named: '" + config.Resource_DB + "' to delete")
                self.server.create(config.Resource_DB)
            try:
                del self.server[config.Link_DB]
                self.server.create(config.Link_DB)
            except Exception:
                logger.debug("No DB named: '" + config.Link_DB + "' to delete")
                self.server.create(config.Link_DB)
        else:
            try:
                self.server[config.Kind_DB]
            except couchdb.http.ResourceNotFound:
                logger.debug("The database named: '" + config.Kind_DB + "' does not exist.")
                self.server.create(config.Kind_DB)
            try:
                self.server[config.Action_DB]
            except couchdb.http.ResourceNotFound:
                logger.debug("The database named: '" + config.Action_DB + "'does not exist.")
                self.server[config.Action_DB]
            try:
                self.server[config.Mixin_DB]
            except couchdb.http.ResourceNotFound:
                logger.debug("The database named: '" + config.Mixin_DB + "'does not exist.")
                self.server[config.Mixin_DB]
            try:
                self.server[config.Resource_DB]
            except couchdb.http.ResourceNotFound:
                logger.debug("The database named: '" + config.Resource_DB + "'does not exist.")
                self.server[config.Resource_DB]
            try:
                self.server[config.Link_DB]
            except couchdb.http.ResourceNotFound:
                logger.debug("The database named: '" + config.Link_DB + "'does not exist.")
                self.server[config.Link_DB]


    def load_defaults(self):

        """
        Load default kinds and mixins from the default folder

        """
        try :
            for file in os.listdir("../Examples"):
                default_file=open("../Examples/"+ file,"r")
                content=default_file.read()
                content = json.loads(content)
                self.JSON_mini_parser(content)
                # must have a way to distinguish between CategoryChildren & EntityChildren
                doc_id,doc_rev=self.DataBase.save(content)
        except Exception as e:
            print e.message

    def JSON_mini_parser(self,jdata):
        """
        Detects the type of the request and stores it in the convenient database
        """

        for key ,val in jdata.items():
            pass

        if key in entity_children.__dict__.keys():
            self.DataBase = self.server[DB_Entity_children]
        elif key in category_children.__dict__.keys():
            self.DataBase = self.server[DB_Category_children]
        else:
            raise Exception(str(key)+ " is an unknown type")







if __name__=='__main__':
    Cat_Reg=Category_registry()
    Cat_Reg.load_defaults()






