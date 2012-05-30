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
import couchdb

# getting the Logger
logger = config.logger


# Get the database server configuration

DB_server_IP = config.DB_IP
DB_server_PORT = config.DB_PORT
DB_Category_children = config.DB_CATEGORY_CHILDREN
DB_Entity_children = config.DB_ENTITY_CHILDREN

entity_children = Enum("resources","links")
category_children = Enum("mixins", "actions", "kinds")

#====================CategoryRegistry====================

class Category_registry(object):
    """

    A registry containing default Kinds, Mixins, actions and more.

    """
    content = ""

    def __init__(self):
        """
        Initialize db for the upcoming inputs
        """

        try:
            self.server = couchdb.Server()
        except Exception:
            logger.error("Database is unreachable")
        # ======================================================================================
        # Reinitialization of the database
        # ======================================================================================
        result = shell_ask.query_yes_no_quit(" \n_______________________________________________________________\n"
        "   Do you want to purge all databases (DB  reinitialization)?", "no")
        if result == 'yes':
            try:
                del self.server[DB_Category_children]
                self.server.create(DB_Category_children)
            except Exception:
                logger.debug("No DB named: '" + DB_Category_children + "' to delete.")
                self.server.create(DB_Category_children)
            try:
                del self.server[DB_Entity_children]
                self.server.create(DB_Entity_children)
            except Exception:
                logger.debug("No DB named: '" + DB_Entity_children + "' to delete")
                self.server.create(DB_Entity_children)
        else:
            try:
                self.server[DB_Category_children]
            except couchdb.http.ResourceNotFound:
                logger.debug("The database named: '" + DB_Category_children + "' does not exist.")
                self.server.create(DB_Category_children)
            try:
                self.server[DB_Entity_children]
            except couchdb.http.ResourceNotFound:
                logger.debug("The database named: '" + DB_Entity_children + "'does not exist.")
                self.server[DB_Entity_children]


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
        key = "hello"

        if key in entity_children.__dict__.keys():
            self.DataBase = self.server[DB_Entity_children]
        elif key in category_children.__dict__.keys():
            self.DataBase = self.server[DB_Category_children]
        else:
            raise Exception(str(key)+ " is an unknown type")







if __name__=='__main__':
    Cat_Reg=Category_registry()
    Cat_Reg.load_defaults()





