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
Created on Oct 02 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@license: Apache License, Version 2.0
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
    Converts the data contained inside the request to the application/occi+json data format.
    """

    def __init__(self):
        self.from_text_plain_f = From_Text_Plain_to_JSON()
        self.from_text_occi_f = From_Text_OCCI_to_JSON()

    def convert_request_category_content(self, req):

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

    def convert_request_entity_content(self, req):

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

    def convert_request_entity_content_v2(self, req):
        """
        Used only for partial update.
        """

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



