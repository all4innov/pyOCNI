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


from webob import Response
from pyocni.adapters.httpResponse_Formater import To_HTTP_Text_OCCI,To_HTTP_Text_Plain,To_HTTP_Text_URI_List
try:
    import simplejson as json
except ImportError:
    import json

class ResponseAdapter():
    """
    Converts the response data into the required data format.
    """
    def __init__(self):

        self.text_plain_f = To_HTTP_Text_Plain()
        self.text_occi_f = To_HTTP_Text_OCCI()
        self.text_uri_f = To_HTTP_Text_URI_List()

    def convert_response_category_content(self,res,jdata):


        if str(res.content_type) == "application/occi+json":
            res.body = json.dumps(jdata)

        elif str(res.content_type) == "text/occi":
            #reformat the response to text/occi
            res.body = "OK"
            res.headers.extend(self.text_occi_f.format_to_text_occi_categories(jdata))

        else:
            #reformat the response to text/plain (default OCCI response format)
            res.headers.extend({"content_type" : "text/plain"})
            res.body = self.text_plain_f.format_to_text_plain_categories(jdata)

        return res


    def convert_response_entity_multi_location_content(self,var,res):

        if str(res.content_type) == "application/occi+json":
            res.body = json.dumps(var)

        elif str(res.content_type) == "text/occi":
            #reformat the response to text/occi
            res.body = "OK"
            res.headers = self.text_occi_f.format_to_text_occi_locations(var)

        elif str(res.content_type) == "text/uri-list":
            #reformat the response to text/occi
            res,ok = self.text_uri_f.check_for_uri_locations(var)
            if ok is True:
                res.body = res
            else:
                res.content_type = "text/plain"
                res.body = self.text_plain_f.format_to_text_plain_locations(var)

        else :
            #reformat the response to text/plain (default OCCI response format)
            res.content_type = "text/plain"
            res.body = self.text_plain_f.format_to_text_plain_locations(var)

        return res

    def convert_response_entity_location_content(self,var,res):

        if str(res.content_type) == "application/occi+json":
            res.body = var

        elif str(res.content_type) == "text/occi":
            #reformat the response to text/occi
            res.body = "OK"
            res.location = var

        else :
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

        else :
            #reformat the response to text/plain (default OCCI response format)
            res.content_type = "text/plain"
            res.body = self.text_plain_f.format_to_text_plain_entities(var)

        return res




