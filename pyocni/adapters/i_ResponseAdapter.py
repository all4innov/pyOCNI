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
Created on Oct 02, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@license: Apache License, Version 2.0
"""

from webob import Response
from pyocni.adapters.httpResponse_Formater import To_HTTP_Text_OCCI, To_HTTP_Text_Plain, To_HTTP_Text_URI_List

try:
    import simplejson as json
except ImportError:
    import json

class ResponseAdapter():
    """
    Converts the response data into the required data format (text/plain, text/occi ,text/uri, application/occi+json).
    """

    def __init__(self):

        self.text_plain_f = To_HTTP_Text_Plain()
        self.text_occi_f = To_HTTP_Text_OCCI()
        self.text_uri_f = To_HTTP_Text_URI_List()

    def convert_response_category_content(self, res, jdata):
        if str(res.content_type) == "application/occi+json":
            res.body = json.dumps(jdata)

        elif str(res.content_type) == "text/occi":
            #reformat the response to text/occi
            res.body = "OK"
            res.headers.extend(self.text_occi_f.format_to_text_occi_categories(jdata))

        else:
            #reformat the response to text/plain (default OCCI response format)
            res.headers.extend({"content_type": "text/plain"})
            res.body = self.text_plain_f.format_to_text_plain_categories(jdata)

        return res


    def convert_response_entity_multi_location_content(self, var, res):
        if str(res.content_type) == "application/occi+json":
            location_dict = {"Location": var}
            res.body = json.dumps(location_dict)

        elif str(res.content_type) == "text/occi":
            #reformat the response to text/occi
            res.body = "OK"
            res.headers = self.text_occi_f.format_to_text_occi_locations(var)

        elif str(res.content_type) == "text/uri-list":
            #reformat the response to text/occi
            res, ok = self.text_uri_f.check_for_uri_locations(var)
            if ok is True:
                res.body = res
            else:
                res.content_type = "text/plain"
                res.body = self.text_plain_f.format_to_text_plain_locations(var)

        else:
            #reformat the response to text/plain (default OCCI response format)
            res.content_type = "text/plain"
            res.body = self.text_plain_f.format_to_text_plain_locations(var)

        return res

    def convert_response_entity_location_content(self, var, res):
        if str(res.content_type) == "application/occi+json":
            res.body = var

        elif str(res.content_type) == "text/occi":
            #reformat the response to text/occi
            res.body = "OK"
            res.location = var

        else:
            #reformat the response to text/plain (default OCCI response format)
            res.content_type = "text/plain"
            res.location = var

        return res

    def convert_response_entity_content(self, res, var):
        if str(res.content_type) == "application/occi+json":
            res.body = json.dumps(var)

        elif str(res.content_type) == "text/occi":
            #reformat the response to text/occi
            res.body = "OK"
            res.headers.extend(self.text_occi_f.format_to_text_occi_entities(var))

        else:
            #reformat the response to text/plain (default OCCI response format)
            res.content_type = "text/plain"
            res.body = self.text_plain_f.format_to_text_plain_entities(var)

        return res

    def convert_response_entity_multi_x_occi_location_content(self, var, res):
        if str(res.content_type) == "application/occi+json":
            x_occi_location_dict = {"X-OCCI-Location": var}
            res.body = json.dumps(x_occi_location_dict)

        elif str(res.content_type) == "text/occi":
            #reformat the response to text/occi
            res.body = "OK"
            res.headers = self.text_occi_f.format_to_text_x_occi_locations(var)

        elif str(res.content_type) == "text/uri-list":
            #reformat the response to text/occi
            res, ok = self.text_uri_f.check_for_uri_locations(var)
            if ok is True:
                res.body = res
            else:
                res.content_type = "text/plain"
                res.body = self.text_plain_f.format_to_text_plain_x_locations(var)

        else:
            #reformat the response to text/plain (default OCCI response format)
            res.content_type = "text/plain"
            res.body = self.text_plain_f.format_to_text_plain_x_locations(var)

        return res



