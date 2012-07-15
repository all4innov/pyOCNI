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
Created on Jun 19, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@version: 0.3
@license: LGPL - Lesser General Public License
"""

from webob import Response
from pyocni.registry.categoryManager import CategoryManager
try:
    import simplejson as json
except ImportError:
    import json

import base64
from pyocni.pyocni_tools.config import return_code
from pyocni.serialization.httpResponse_Formater import To_HTTP_Text_OCCI,To_HTTP_Text_Plain,To_HTTP_Text_URI_List
from pyocni.serialization.httpRequest_Formater import From_Text_Plain_to_JSON, From_Text_OCCI_to_JSON
class QueryInterface(object):
    """

        CRUD operation on kinds, mixins and actions

    """
    def __init__(self,req):

        self.req = req
        self.res = Response()
        self.res.content_type = req.accept
        self.res.server = 'ocni-server/1.1 (linux) OCNI/1.1'
        self.text_plain_f = To_HTTP_Text_Plain()
        self.text_occi_f = To_HTTP_Text_OCCI()
        self.text_uri_f = To_HTTP_Text_URI_List()
        self.from_text_plain_f = From_Text_Plain_to_JSON()
        self.from_text_occi_f = From_Text_OCCI_to_JSON()
        try:
            self.manager = CategoryManager()
        except Exception:
            self.res.body = "An error has occurred, please check log for more details"
            self.res.status_code = return_code["Internal Server Error"]

    def get(self):

        """
        Retrieval of all registered Kinds, mixins and actions
        """
        #Detect the body type (HTTP ,JSON:OCCI or OCCI+JSON)
        jreq = ""
        if self.req.content_type == "text/plain":
            # Solution To adopt : Validate HTTP then convert to JSON
            jreq = self.from_text_plain_f.format_text_plain_categories_to_json(self.req.body)

        elif self.req.content_type == "text/occi":
            jreq = self.from_text_occi_f.format_text_occi_categories_to_json(self.req.headers)

        elif self.req.content_type == "application/json:occi":
            #  Solution To adopt : Validate then convert to application/occi+json
            pass

        elif self.req.content_type == "application/occi+json":
            #Validate the JSON message
            jreq = json.loads(self.req.body)

        else:
            self.res.status_code = return_code['Not Acceptable']
            self.res.body = self.req.content_type + " is an unknown request content type"
            return self.res

        if jreq == "":
            var,self.res.status_code = self.manager.channel_get_all_categories()
        else:
            var,self.res.status_code = self.manager.channel_get_filtered_categories(jreq)

        if self.res.status_code == return_code['OK']:
            if str(self.req.accept) == "application/occi+json":
                self.res.body = json.dumps(var)

            elif str(self.req.accept) == "text/occi":
                #reformat the response to text/occi
                self.res.body = "OK"
                self.res.headers.extend(self.text_occi_f.format_to_text_occi_categories(var))

            else :
                #reformat the response to text/plain (default OCCI response format)
                self.res.content_type = "text/plain"
                self.res.body = self.text_plain_f.format_to_text_plain_categories(var)
        else:
            self.res.content_type = "text/html"
            self.res.body = var

        return self.res

    def post(self):
        """
        Create new mixin or kind or action document in the database

        """

        #Detect the body type (HTTP ,JSON:OCCI or OCCI+JSON)
        jBody=dict()

        if self.req.content_type == "text/plain":
            # Solution To adopt : Validate HTTP then convert to JSON
            jBody = self.from_text_plain_f.format_text_plain_categories_to_json(self.req.body)

        elif self.req.content_type == "text/occi":
            jBody = self.from_text_occi_f.format_text_occi_categories_to_json(self.req.headers)

        elif self.req.content_type == "application/json:occi":
            #  Solution To adopt : Validate then convert to application/occi+json
            pass

        elif self.req.content_type == "application/occi+json":
            #Validate the JSON message
            jBody = json.loads(self.req.body)

        else:
            self.res.status_code = return_code['Not Acceptable']
            self.res.body = self.req.content_type + " is an unknown request content type"
            return self.res

        #Decode authorization header to get the user_id
        var,user_id = self.req.authorization
        user_id = base64.decodestring(user_id)
        user_id = user_id.split(':')[0]

        #add the JSON to database along with other attributes
        self.res.body,self.res.status_code = self.manager.channel_register_categories(user_id,jBody)
        return self.res

    def put(self):
        """
        Update the document specific to the id provided in the request with new data

        """

        #Detect the body type (HTTP ,JSON:OCCI or OCCI+JSON)
        j_newData = dict()
        if self.req.content_type == "text/plain":
            # Solution To adopt : Validate HTTP then convert to JSON
            j_newData = self.from_text_plain_f.format_text_plain_categories_to_json(self.req.body)

        elif self.req.content_type == "text/occi":
            j_newData = self.from_text_occi_f.format_text_occi_categories_to_json(self.req.headers)

        elif self.req.content_type == "application/json:occi":
            #  Solution To adopt : Validate then convert to application/occi+json
            pass

        elif self.req.content_type == "application/occi+json":
            #Validate the JSON message
            j_newData = json.loads(self.req.body)

        else:
            self.res.status_code = return_code['Not Acceptable']
            self.res.body = self.req.content_type + " is an unknown request content type"
            return self.res

        #Decode authorization header to get the user_id
        var,user_id = self.req.authorization
        user_id = base64.decodestring(user_id)
        user_id = user_id.split(':')[0]
        #Get the new data from the request

        self.res.body, self.res.status_code = self.manager.channel_update_categories(user_id,j_newData)
        return self.res

    def delete(self):
        """

        Delete a category document using the data provided in the request

        """
        #Detect the body type (HTTP ,JSON:OCCI or OCCI+JSON)

        if self.req.content_type == "text/plain":
            # Solution To adopt : Validate HTTP then convert to JSON
            jBody = self.from_text_plain_f.format_text_plain_categories_to_json(self.req.body)

        elif self.req.content_type == "text/occi":
            jBody = self.from_text_occi_f.format_text_occi_categories_to_json(self.req.headers)

        elif self.req.content_type == "application/json:occi":
            #  Solution To adopt : Validate then convert to application/occi+json
            pass

        elif self.req.content_type == "application/occi+json":
            #Validate the JSON message
            jBody = json.loads(self.req.body)

        else:
            self.res.status_code = return_code['Not Acceptable']
            self.res.body = self.req.content_type + " is an unknown request content type"
            return self.res

        #Decode authorization header to get the user_id
        var,user_id = self.req.authorization
        user_id = base64.decodestring(user_id)
        user_id = user_id.split(':')[0]

        self.res.body,self.res.status_code= self.manager.channel_delete_categories(jBody,user_id)

        return self.res
