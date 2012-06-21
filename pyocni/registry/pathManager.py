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
Created on Jun 21, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@version: 0.3
@license: LGPL - Lesser General Public License
"""

import pyocni.pyocni_tools.config as config
from pyocni.registry.categoryManager import KindManager,MixinManager
import pyocni.pyocni_tools.occi_Joker as joker
import pyocni.pyocni_tools.couchdbdoc_Joker as doc_Joker
try:
    import simplejson as json
except ImportError:
    import json
from datetime import datetime
from pyocni.pyocni_tools import uuid_Generator
from couchdbkit import *
from pyocni.pyocni_tools.config import return_code
# getting the Logger
logger = config.logger


# Get the database server configuration

DB_server_IP = config.DB_IP
DB_server_PORT = config.DB_PORT

class PathManager(object):
    """

    """

    def __init__(self):
        self.manager_k = KindManager()
        self.manager_m = MixinManager()

    def channel_post_path(self,user_id,jreq,location):
        """
        Identifies the post path's goal : create a resource instance or update a mixin
        Args:
            @param user_id: ID of the issuer of the post request
            @param jreq: Body content of the post request
            @param location: Address to which this post request was sent
        """
        #Verify if this is a kind location
        ok_k = self.manager_k.verify_kind_location(location)
        #if yes : call the ResourceManager to create a new resource instance
        if ok_k is True:
            logger.debug("Post path : Post on kind path channeled")
        else:
        #if no : verify if this is a mixin location
            ok_m = self.manager_m.verify_mixin_location(location)
            if ok_m is True:
                #if yes: call the ResourceManager to attach this mixin to resources
                logger.debug("Post path : Post on mixin path channeled")
            else:
                logger.error("Post path : Unknown location")


    def channel_get_path(self,user_id,jreq,location):
        """
        Channel the get request to the right method
        Args:
            @param user_id: ID of the issuer of the post request
            @param jreq: Body content of the post request
            @param location: Address to which this post request was sent
        """
        #Verify if this is a kind location
        ok_k = self.manager_k.verify_kind_location(location)
        #if yes : call the ResourceManager to retrieve resource instances belonging to this kind
        if ok_k is True:
            logger.debug("Get path : Get on kind path channeled")
        else:
        #if no : verify if this is a mixin location
            ok_m = self.manager_m.verify_mixin_location(location)
            if ok_m is True:
                #if yes: call the ResourceManager to retrieve all resource instances belonging to this mixin
                logger.debug("Get path : Get on mixin path channeled")
            else:
                #Get all locations and state hierarchy below this path
                logger.debug("Get path : Get on path channeled")
