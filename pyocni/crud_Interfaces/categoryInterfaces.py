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
Created on Jun 09, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@version: 0.3
@license: LGPL - Lesser General Public License
"""
from webob import Request,Response
from pyocni.registry.categoryManager import KindManager,MixinManager,ActionManager
try:
    import simplejson as json
except ImportError:
    import json

import base64

# ======================================================================================
# HTTP Return Codes
# ======================================================================================
return_code = {'OK': 200,
               'Accepted': 202,
               'Bad Request': 400,
               'Unauthorized': 401,
               'Forbidden': 403,
               'Resource not found': 404,
               'Method Not Allowed': 405,
               'Conflict': 409,
               'Gone': 410,
               'Unsupported Media Type': 415,
               'Internal Server Error': 500,
               'Not Implemented': 501,
               'Service Unavailable': 503}

class KindInterface(object):
    """

        CRUD operation on kinds

    """
    def __init__(self,req, doc_id=None,user_id=None):

        self.req = req
        self.doc_id=doc_id
        self.user_id=user_id
        self.res = Response()
        self.res.content_type = req.accept
        self.res.server = 'ocni-server/1.1 (linux) OCNI/1.1'
        try:
            self.manager = KindManager()
        except Exception:
            self.res.body = "An error has occurred, please check log for more details"
            self.res.status_code = return_code["Internal Server Error"]

    def get(self):

        """
        Retrieval of all registered Kinds or just one kind
        """
        #if the doc_id is specified then only one kind will be returned if it exists
        if self.doc_id is not None:
            var,self.res.status_code = self.manager.get_kind_by_id(self.doc_id)
            self.res.body = '\n====================\n'.join(var)
            #No doc_id specified, all kinds will be returned
        else:
            var,self.res.status_code = self.manager.get_all_kinds()
            self.res.body = '\n====================\n'.join(var)
        return self.res

    def post(self):
        """
        Create new kind documents in the database

        """

        #Detect the body type (HTTP ,OCCI:JSON or OCCI+JSON)

        if self.req.content_type == "text/occi" or self.req.content_type == "text/plain" or self.req.content_type == "text/uri-list":
            # Solution To adopt : Validate HTTP then convert to JSON
            pass
        elif self.req.content_type == "application/occi:json":
            #  Solution To adopt : Validate then convert to application/occi+json
            pass
        elif self.req.content_type == "application/occi+json":
            #Validate the JSON message
            pass
        else:
            self.res.status_code = return_code["Unsupported Media Type"]
            self.res.body = self.req.content_type + " is an unknown request content type"
            return self.res

        #Decode authorization header to get the user_id
        var,user_id = self.req.authorization
        user_id = base64.decodestring(user_id)
        user_id = user_id.split(':')[0]
        jBody = json.loads(self.req.body)
        #add the JSON to database along with other attributes
        mylist,self.res.status_code = self.manager.register_kinds(user_id,jBody)
        self.res.body = '\n'.join(mylist)
        return self.res

    def put(self):
        """
        Update the document specific to the id provided in the request with new data

        """

        #Detect the body type (HTTP ,OCCI:JSON or OCCI+JSON)

        if self.req.content_type == "text/occi" or self.req.content_type == "text/plain" or self.req.content_type == "text/uri-list":
            # Solution To adopt : Validate HTTP then convert to JSON
            pass
        elif self.req.content_type == "application/occi:json":
            #  Solution To adopt : Validate then convert to application/occi+json
            pass
        elif self.req.content_type == "application/occi+json":
            #Validate the JSON message
            pass
        else:
            self.res.status_code = return_code["Unsupported Media Type"]
            self.res.body = self.req.content_type + " is an unknown request content type"
            return self.res
        #Get the new data from the request
        j_newData = json.loads(self.req.body)
        self.res.body,self.res.status_code = self.manager.update_kind(self.doc_id,self.user_id,j_newData)
        return self.res

    def delete(self):
        """

        Delete a document using the doc_id provided in the request

        """
        self.res.body,self.res.status_code = self.manager.delete_kind_document(self.doc_id,self.user_id)
        return self.res

class MixinInterface(object):
    """

        CRUD operation on mixins

    """
    def __init__(self,req, doc_id=None,user_id=None):

        self.req = req
        self.doc_id=doc_id
        self.user_id=user_id
        self.res = Response()
        self.res.content_type = req.accept
        self.res.server = 'ocni-server/1.1 (linux) OCNI/1.1'
        try:
            self.manager = MixinManager()
        except Exception:
            self.res.body = "An error has occurred, please check log for more details"
            self.res.status_code = return_code["Internal Server Error"]


    def get(self):

        """
        Retrieval of all registered mixins or just one mixin
        """
        #if the doc_id is specified then only one mixin will be returned if it exists
        if self.doc_id is not None:
            var,self.res.status_code = self.manager.get_mixin_by_id(self.doc_id)
            self.res.body = '\n====================\n'.join(var)
            #No doc_id specified, all mixins will be returned
        else:
            var,self.res.status_code = self.manager.get_all_mixins()
            self.res.body = '\n====================\n'.join(var)
        return self.res

    def post(self):

        """
        Create a new mixin document in the database

        """

        #Detect the body type (HTTP ,OCCI:JSON or OCCI+JSON)

        if self.req.content_type == "text/occi" or self.req.content_type == "text/plain" or self.req.content_type == "text/uri-list":
            # Solution To adopt : Validate HTTP then convert to application/occi+json
            pass
        elif self.req.content_type == "application/occi:json":
            #  Solution To adopt : Validate then convert to application/occi+json
            pass
        elif self.req.content_type == "application/occi+json":
            #Validate the JSON message
            pass
        else:
            self.res.status_code = return_code["Unsupported Media Type"]
            self.res.body = self.req.content_type + " is an unknown request content type"
            return self.res

        #Decode authorization header to get the user_id
        var,user_id = self.req.authorization
        user_id = base64.decodestring(user_id)
        user_id = user_id.split(':')[0]
        jBody = json.loads(self.req.body)
        #add the JSON data to database

        mylist,self.res.status_code = self.manager.register_mixins(user_id,jBody)
        self.res.body = '\n'.join(mylist)
        return self.res

    def put(self):
        """
        Update the document specific to the id provided

        """

        #Detect the body type (HTTP ,OCCI:JSON or OCCI+JSON)

        if self.req.content_type == "text/occi" or self.req.content_type == "text/plain" or self.req.content_type == "text/uri-list":
            # Solution To adopt : Validate HTTP then convert to JSON
            pass
        elif self.req.content_type == "application/occi:json":
            #  Solution To adopt : Validate then convert to application/occi+json
            pass
        elif self.req.content_type == "application/occi+json":
            #Validate the JSON message
            pass
        else:
            self.res.status_code = return_code["Unsupported Media Type"]
            self.res.body = self.req.content_type + " is an unknown request content type"
            return self.res
            #Get the new data from the request
        j_newData = json.loads(self.req.body)

        self.res.body, self.res.status_code = self.manager.update_mixin(self.doc_id,self.user_id,j_newData)
        return self.res

    def delete(self):
        """

        Delete a document using the doc_id

        """
        self.res.body, self.res.status_code = self.manager.delete_mixin_document(self.doc_id,self.user_id)
        return self.res

class ActionInterface(object):
    """

        CRUD operation on actions

    """
    def __init__(self,req, doc_id=None,user_id=None):

        self.req = req
        self.doc_id=doc_id
        self.user_id=user_id
        self.res = Response()
        self.res.content_type = req.accept
        self.res.server = 'ocni-server/1.1 (linux) OCNI/1.1'
        try:
            self.manager = ActionManager()
        except Exception:
            self.res.body = "An error has occurred, please check log for more details"
            self.res.status_code = return_code["Internal Server Error"]

    def get(self):

        """
        Retrieval of all registered actions or just one action
        """
        #if the doc_id is specified then only one action will be returned if it exists
        if self.doc_id is not None:
            var,self.res.status_code = self.manager.get_action_by_id(self.doc_id)
            self.res.body = '\n====================\n'.join(var)
            #No doc_id specified, all actions will be returned
        else:
            var,self.res.status_code = self.manager.get_all_actions()
            self.res.body = '\n====================\n'.join(var)
        return self.res

    def post(self):

        """
        Create a new action document in the database

        """

        #Detect the body type (HTTP ,OCCI:JSON or OCCI+JSON)

        if self.req.content_type == "text/occi" or self.req.content_type == "text/plain" or self.req.content_type == "text/uri-list":
            # Solution To adopt : Validate HTTP then convert to application/occi+json
            pass
        elif self.req.content_type == "application/occi:json":
            #  Solution To adopt : Validate then convert to application/occi+json
            pass
        elif self.req.content_type == "application/occi+json":
            #Validate the JSON message
            pass
        else:
            self.res.status_code = return_code["Unsupported Media Type"]
            self.res.body = self.req.content_type + " is an unknown request content type"
            return self.res

        #Decode authorization header to get the user_id
        var,user_id = self.req.authorization
        user_id = base64.decodestring(user_id)
        user_id = user_id.split(':')[0]
        jBody = json.loads(self.req.body)
        #add the JSON data to database

        mylist,self.res.status_code = self.manager.register_actions(user_id,jBody)
        self.res.body = '\n'.join(mylist)
        return self.res

    def put(self):
        """
        Update the document specific to the id provided with new data

        """

        #Detect the body type (HTTP ,OCCI:JSON or OCCI+JSON)

        if self.req.content_type == "text/occi" or self.req.content_type == "text/plain" or self.req.content_type == "text/uri-list":
            # Solution To adopt : Validate HTTP then convert to JSON
            pass
        elif self.req.content_type == "application/occi:json":
            #  Solution To adopt : Validate then convert to application/occi+json
            pass
        elif self.req.content_type == "application/occi+json":
            #Validate the JSON message
            pass
        else:
            self.res.status_code = return_code["Unsupported Media Type"]
            self.res.body = self.req.content_type + " is an unknown request content type"
            return self.res
            #Get the new data from the request
        j_newData = json.loads(self.req.body)

        self.res.body, self.res.status_code = self.manager.update_action(self.doc_id,self.user_id,j_newData)
        return self.res

    def delete(self):
        """

        Delete a document using the doc_id

        """
        self.res.body, self.res.status_code = self.manager.delete_action_document(self.doc_id,self.user_id)
        return self.res

class CategoryInterface(object):
    """

        CRUD operation on actions

    """
    def __init__(self,req, doc_id=None,user_id=None):

        self.req = req
        self.doc_id=doc_id
        self.user_id=user_id
        self.res = Response()
        self.res.content_type = req.accept
        self.res.server = 'ocni-server/1.1 (linux) OCNI/1.1'
        try:
            self.manager = ActionManager()
        except Exception:
            self.res.body = "An error has occurred, please check log for more details"
            self.res.status_code = return_code["Internal Server Error"]

    def get(self):

        """
        Retrieval of all registered actions or just one action
        """
        #if the doc_id is specified then only one action will be returned if it exists
        if self.doc_id is not None:
            var,self.res.status_code = self.manager.get_action_by_id(self.doc_id)
            self.res.body = '\n====================\n'.join(var)
            #No doc_id specified, all actions will be returned
        else:
            var,self.res.status_code = self.manager.get_all_actions()
            self.res.body = '\n====================\n'.join(var)
        return self.res

    def post(self):

        """
        Create a new action document in the database

        """

        #Detect the body type (HTTP ,OCCI:JSON or OCCI+JSON)

        if self.req.content_type == "text/occi" or self.req.content_type == "text/plain" or self.req.content_type == "text/uri-list":
            # Solution To adopt : Validate HTTP then convert to application/occi+json
            pass
        elif self.req.content_type == "application/occi:json":
            #  Solution To adopt : Validate then convert to application/occi+json
            pass
        elif self.req.content_type == "application/occi+json":
            #Validate the JSON message
            pass
        else:
            self.res.status_code = return_code["Unsupported Media Type"]
            self.res.body = self.req.content_type + " is an unknown request content type"
            return self.res

        #Decode authorization header to get the user_id
        var,user_id = self.req.authorization
        user_id = base64.decodestring(user_id)
        user_id = user_id.split(':')[0]
        jBody = json.loads(self.req.body)
        #add the JSON data to database

        mylist,self.res.status_code = self.manager.register_actions(user_id,jBody)
        self.res.body = '\n'.join(mylist)
        return self.res

    def put(self):
        """
        Update the document specific to the id provided with new data

        """

        #Detect the body type (HTTP ,OCCI:JSON or OCCI+JSON)

        if self.req.content_type == "text/occi" or self.req.content_type == "text/plain" or self.req.content_type == "text/uri-list":
            # Solution To adopt : Validate HTTP then convert to JSON
            pass
        elif self.req.content_type == "application/occi:json":
            #  Solution To adopt : Validate then convert to application/occi+json
            pass
        elif self.req.content_type == "application/occi+json":
            #Validate the JSON message
            pass
        else:
            self.res.status_code = return_code["Unsupported Media Type"]
            self.res.body = self.req.content_type + " is an unknown request content type"
            return self.res
            #Get the new data from the request
        j_newData = json.loads(self.req.body)

        self.res.body, self.res.status_code = self.manager.update_action(self.doc_id,self.user_id,j_newData)
        return self.res

    def delete(self):
        """

        Delete a document using the doc_id

        """
        self.res.body, self.res.status_code = self.manager.delete_action_document(self.doc_id,self.user_id)
        return self.res
