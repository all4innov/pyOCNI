# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

# Copyright (C) 2011 Houssem Medhioub - Institut Telecom
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
@version: 0.2
@license: LGPL - Lesser General Public License
"""
from webob import Request, Response
from pyocni.registry.CategoryManager import KindManager
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
            self.res.body = "Nothing has been added to the database, please check log for more details"
            self.res.status_code = return_code["Internal Server Error"]

    def get(self):

        """
        Retrieval of all registered Kinds or just one kind
        """
        #if the doc_id is specified then only one kind will be returned if it exists
        if self.doc_id is not None:
            res = self.manager.get_kind_by_id(self.doc_id)
            self.res.body = json.dumps(res)
            self.res.status = return_code['OK']
            #No doc_id specified, all kinds will be returned
        else:
            var = self.manager.get_all_kinds()
            self.res.body = json.dumps(var)
            self.res.status_code = return_code['OK']
        return self.res

    def post(self):
        """
        Create a new document

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
        try:
            path = self.manager.register_kind(user_id,jBody)
            self.res.body = "A new kind has been successfully added to database : " + path
            self.res.status_code = return_code['OK']
        except Exception:
            self.res.body = "A problem has occured, please check log for more details"
            self.res.status_code = return_code['Internal Server Error']

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
        try:
            self.res.body = self.manager.update_kind(self.doc_id,j_newData)
        except Exception:
            self.res.status = return_code['Internal Server Error']
        return self.res

    def delete(self):
        """

        Delete a document using the doc_id provided in the request

        """
        self.res.body = self.manager.delete_document(self.doc_id)
        self.res.status_code = return_code['OK']
        return self.res


