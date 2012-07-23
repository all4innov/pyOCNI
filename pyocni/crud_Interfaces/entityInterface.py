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

from webob import Response,Request
from pyocni.registry.entityManager import MultiEntityManager,SingleEntityManager
from pyocni.pyocni_tools.config import return_code
try:
    import simplejson as json
except ImportError:
    import json
from pyocni.serialization.httpResponse_Formater import To_HTTP_Text_OCCI,To_HTTP_Text_Plain,To_HTTP_Text_URI_List
from pyocni.serialization.httpRequest_Formater import From_Text_Plain_to_JSON, From_Text_OCCI_to_JSON
import base64

#=======================================================================================================================
#                                           SingleEntityInterface
#=======================================================================================================================
class SingleEntityInterface(object):
    """

        CRUD operation on resources and links

    """
    def __init__(self,req,location,idontknow=None,idontcare=None):

        self.req = req
        self.location=location
        self.idontknow = idontknow
        self.idontcare = idontcare
        self.path_url = self.req.path_url
        self.triggered_action = None
        self.res = Response()
        self.res.content_type = req.accept
        self.res.server = 'ocni-server/1.1 (linux) OCNI/1.1'
        self.text_occi_f = To_HTTP_Text_OCCI()
        self.text_plain_f = To_HTTP_Text_Plain()
        self.text_uri_f = To_HTTP_Text_URI_List()
        self.from_text_plain_f = From_Text_Plain_to_JSON()
        self.from_text_occi_f = From_Text_OCCI_to_JSON()
        try:
            self.manager = SingleEntityManager()
        except Exception:
            self.res.body = "An error has occurred, please check log for more details"
            self.res.status_code = return_code["Internal Server Error"]

    def put(self):
        """
        Create a new entity instance with a customized URL or perform a full update of the resource
        """
        #Detect the body type (HTTP ,OCCI:JSON or OCCI+JSON)

        jBody = ""
        if self.req.content_type == "text/plain":
            # Solution To adopt : Validate HTTP then convert to JSON
            jBody = self.from_text_plain_f.format_text_plain_entity_to_json(self.req.body)

        elif self.req.content_type == "text/occi":
            jBody = self.from_text_occi_f.format_text_occi_entity_to_json(self.req.headers)

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
        var,self.res.status_code = self.manager.channel_put_single(user_id,jBody,self.path_url)

        if self.res.status_code == return_code['OK, and location returned']:
            if str(self.req.accept) == "application/occi+json":
                self.res.body = var

            elif str(self.req.accept) == "text/occi":
                #reformat the response to text/occi
                self.res.body = "OK"
                self.res.location = var

            else :
                #reformat the response to text/plain (default OCCI response format)
                self.res.content_type = "text/plain"
                self.res.location = var
        else:
            self.res.content_type = "text/html"
            self.res.body = var

        return self.res

    def get(self):
        """
        Retrieve the representation of a resource
        """

        #Decode authorization header to get the user_id
        var,user_id = self.req.authorization
        user_id = base64.decodestring(user_id)
        user_id = user_id.split(':')[0]
        #add the JSON to database along with other attributes
        var,self.res.status_code = self.manager.channel_get_single(user_id,self.path_url)

        if self.res.status_code == return_code['OK']:
            if str(self.req.accept) == "application/occi+json":
                self.res.body = json.dumps(var)

            elif str(self.req.accept) == "text/occi":
                #reformat the response to text/occi
                self.res.body = "OK"
                self.res.headers.extend(self.text_occi_f.format_to_text_occi_entities(var))

            else :
                #reformat the response to text/plain (default OCCI response format)
                self.res.content_type = "text/plain"
                self.res.body = self.text_plain_f.format_to_text_plain_entities(var)
        else:
            self.res.content_type = "text/html"
            self.res.body = var

        return self.res

    def post(self):
        """
        Perform a partial update of a resource
        """
        if self.req.params.has_key('action'):
            self.triggered_action = self.req.params['action']

        #Detect the body type (HTTP ,OCCI:JSON or OCCI+JSON)
        jBody = ""
        if self.req.content_type == "text/plain":
            # Solution To adopt : Validate HTTP then convert to JSON
            jBody = self.from_text_plain_f.format_text_plain_entity_to_json_v2(self.req.body)

        elif self.req.content_type == "text/occi":
            jBody = self.from_text_occi_f.format_text_occi_entity_to_json_v2(self.req.headers)

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
        if self.triggered_action is None:
            var,self.res.status_code = self.manager.channel_post_single(user_id,jBody,self.path_url)
            if self.res.status_code == return_code['OK, and location returned']:
                if str(self.req.accept) == "application/occi+json":
                    self.res.body = var

                elif str(self.req.accept) == "text/occi":
                    #reformat the response to text/occi
                    self.res.body = "OK"
                    self.res.location = var

                else :
                    #reformat the response to text/plain (default OCCI response format)
                    self.res.content_type = "text/plain"
                    self.res.location = var

            else:
                self.res.content_type = "text/html"
                self.res.body = var

        else:
            print self.triggered_action
            self.res.body,self.res.status_code = self.manager.channel_triggered_action_single(user_id,jBody,self.path_url,self.triggered_action)

        return self.res


    def delete(self):
        """
        Delete a resource instance

        """

        #Detect the body type (HTTP ,OCCI:JSON or OCCI+JSON)

        #Decode authorization header to get the user_id
        var,user_id = self.req.authorization
        user_id = base64.decodestring(user_id)
        user_id = user_id.split(':')[0]

        #add the JSON to database along with other attributes
        self.res.body,self.res.status_code = self.manager.channel_delete_single(user_id,self.path_url)

        return self.res

#=======================================================================================================================
#                                           MultiEntityInterface
#=======================================================================================================================
class MultiEntityInterface(object):
    """
    CRUD operation on kinds, mixins and actions
    """
    def __init__(self,req,location=None,idontknow=None,idontcare=None):

        self.req = req
        self.location=location
        self.idontcare =idontcare
        self.idontknow=idontknow
        self.triggered_action = None
        self.path_url = self.req.path_url
        self.res = Response()
        self.res.content_type = req.accept
        self.res.server = 'ocni-server/1.1 (linux) OCNI/1.1'
        self.text_occi_f = To_HTTP_Text_OCCI()
        self.text_plain_f = To_HTTP_Text_Plain()
        self.text_uri_f = To_HTTP_Text_URI_List()
        self.from_text_plain_f = From_Text_Plain_to_JSON()
        self.from_text_occi_f = From_Text_OCCI_to_JSON()
        try:
            self.manager = MultiEntityManager()
        except Exception:
            self.res.body = "An error has occurred, please check log for more details"
            self.res.status_code = return_code["Internal Server Error"]


    def post(self):
        """
        Create a new entity instance or attach resource instance to a mixin database

        """

        #Detect the body type (HTTP ,OCCI:JSON or OCCI+JSON)

        jBody = ""
        if self.req.content_type == "text/plain":
            # Solution To adopt : Validate HTTP then convert to JSON
            self.res.body = ""
            self.res.status_code = return_code['Not Implemented']
            return self.res

        elif self.req.content_type == "text/occi":
            self.res.body = ""
            self.res.status_code = return_code['Not Implemented']
            return self.res

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
        if self.triggered_action is None:
            var,self.res.status_code = self.manager.channel_post_multi(user_id,jBody,self.path_url)
            if type(var) is not str:
                self.res.body = json.dumps(var)
            else:
                self.res.body = var
        else:
            self.res.body,self.res.status_code = self.manager.channel_trigger_actions(user_id,jBody,self.path_url,self.triggered_action)

        return self.res

    def get(self):
        """
        Gets entities belonging to a kind or a mixin

        """

        #Detect the body type (HTTP ,OCCI:JSON or OCCI+JSON)

        jBody = ""
        if self.req.content_type == "text/plain":
            # Solution To adopt : Validate HTTP then convert to JSON
            if self.req.body != "":
                jBody = self.from_text_plain_f.format_text_plain_categories_to_json(self.req.body)

        elif self.req.content_type == "text/occi":
            if self.req.body != "":
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

        if jBody == "":
            var,self.res.status_code = self.manager.channel_get_all_entities(self.path_url,user_id,"")
        else:
            var,self.res.status_code = self.manager.channel_get_filtered_entities(self.path_url,user_id,jBody)

        if self.res.status_code == return_code['OK, and location returned']:
            if str(self.req.accept) == "application/occi+json":
                self.res.body = json.dumps(var)

            elif str(self.req.accept) == "text/occi":
                #reformat the response to text/occi
                self.res.body = "OK"
                self.res.headers = self.text_occi_f.format_to_text_occi_locations(var)

            elif str(self.req.accept) == "text/uri-list":
                #reformat the response to text/occi
                res,ok = self.text_uri_f.check_for_uri_locations(var)
                if ok is True:
                    self.res.body = res
                else:
                    self.res.content_type = "text/plain"
                    self.res.body = self.text_plain_f.format_to_text_plain_locations(var)

            else :
                #reformat the response to text/plain (default OCCI response format)
                self.res.content_type = "text/plain"
                self.res.body = self.text_plain_f.format_to_text_plain_locations(var)

        else:
            self.res.content_type = "text/html"
            self.res.body = var

            return self.res

    def put(self):
        """
        Update the mixin collection of entities

        """

        #Detect the body type (HTTP ,OCCI:JSON or OCCI+JSON)

        jBody = ""
        if self.req.content_type == "text/plain":
            # Solution To adopt : Validate HTTP then convert to JSON
            self.res.body = ""
            self.res.status_code = return_code['Not Implemented']
            return self.res

        elif self.req.content_type == "text/occi":
            self.res.body = ""
            self.res.status_code = return_code['Not Implemented']
            return self.res

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
        self.res.body,self.res.status_code = self.manager.channel_put_multi(user_id,jBody,self.path_url)
        return self.res

    def delete(self):
        """
        Dissociates a resource instance from a mixin

        """

        #Detect the body type (HTTP ,OCCI:JSON or OCCI+JSON)

        jBody = ""
        if self.req.content_type == "text/plain":
            # Solution To adopt : Validate HTTP then convert to JSON
            self.res.body = ""
            self.res.status_code = return_code['Not Implemented']
            return self.res

        elif self.req.content_type == "text/occi":
            self.res.body = ""
            self.res.status_code = return_code['Not Implemented']
            return self.res

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

        if self.req.body is not "":
            jBody = json.loads(self.req.body)
            #add the JSON to database along with other attributes
            self.res.body,self.res.status_code = self.manager.channel_delete_multi(user_id,jBody,self.path_url)
        else:
            #add the JSON to database along with other attributes
            self.res.body,self.res.status_code = self.manager.channel_delete_multi(user_id,"",self.path_url)
        return self.res