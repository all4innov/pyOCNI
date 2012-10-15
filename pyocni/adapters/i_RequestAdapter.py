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
Created on Oct 02, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@version: 0.3
@license: LGPL - Lesser General Public License
"""


from httpRequest_Formater import From_Text_Plain_to_JSON
from httpRequest_Formater import From_Text_OCCI_to_JSON
import pyocni.pyocni_tools.config as config
# getting the Logger
logger = config.logger
try:
    import simplejson as json
except ImportError:
    import json

class RequestAdapter():
    """
    Converts the data contained inside the request to the occi+json data format.
    """
    def __init__(self):

        self.from_text_plain_f = From_Text_Plain_to_JSON()
        self.from_text_occi_f = From_Text_OCCI_to_JSON()

    def convert_request_category_content(self,req):

        if req.content_type == "text/plain":
            # Solution To adopt : Validate HTTP then convert to JSON
            jdata = self.from_text_plain_f.format_text_plain_categories_to_json(req.body)

        elif req.content_type == "text/occi":
            jdata = self.from_text_occi_f.format_text_occi_categories_to_json(req.headers)

        elif req.content_type == "application/occi+json":
        #Validate the JSON message
            jdata = json.loads(req.body)

        elif req.content_type == "application/json:occi":
            #  Solution To adopt : Validate then convert to application/occi+json
            pass
        else:
            logger.error("========== This is an unknown data format ==========")
            jdata = None

        return jdata

    def convert_request_entity_content(self,req):

        if req.content_type == "text/plain":
            # Solution To adopt : Validate HTTP then convert to JSON
            jdata = self.from_text_plain_f.format_text_plain_entity_to_json(req.body)

        elif req.content_type == "text/occi":
            jdata = self.from_text_occi_f.format_text_occi_entity_to_json(req.headers)

        elif req.content_type == "application/occi+json":
        #Validate the JSON message
            jdata = json.loads(req.body)

        elif req.content_type == "application/json:occi":
            #  Solution To adopt : Validate then convert to application/occi+json
            pass
        else:
            logger.error("========== This is an unknown data format ==========")
            jdata = None

        return jdata

    def convert_request_entity_content_v2(self,req):
        '''
        Used only for partial update.
        '''

        if req.content_type == "text/plain":
            # Solution To adopt : Validate HTTP then convert to JSON
            jdata = self.from_text_plain_f.format_text_plain_entity_to_json_v2(req.body)

        elif req.content_type == "text/occi":
            jdata = self.from_text_occi_f.format_text_occi_entity_to_json_v2(req.headers)

        elif req.content_type == "application/occi+json":
        #Validate the JSON message
            jdata = json.loads(req.body)

        elif req.content_type == "application/json:occi":
            #  Solution To adopt : Validate then convert to application/occi+json
            pass
        else:
            logger.error("========== This is an unknown data format ==========")
            jdata = None

        return jdata
#=======================================================================================================================
#Register the Request adapter class under the I_RequestAdapter abstract base class
#=======================================================================================================================

