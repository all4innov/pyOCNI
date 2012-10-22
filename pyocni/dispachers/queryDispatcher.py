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
from pyocni.junglers.categoryJungler import CategoryJungler
try:
    import simplejson as json
except ImportError:
    import json
from pyocni.pyocni_tools.config import return_code
from pyocni.adapters.i_ResponseAdapter import ResponseAdapter
from pyocni.adapters.i_RequestAdapter import RequestAdapter

class QueryDispatcher(object):
    """
        Dispatches operations concerning the Query Interface.

    """
    def __init__(self,req):

        self.req = req
        self.res = Response()
        self.res.content_type = str(req.accept)
        self.res.server = 'ocni-server/1.1 (linux) OCNI/1.1'
        self.req_adapter = RequestAdapter()
        self.res_adapter = ResponseAdapter()
        self.jungler = CategoryJungler()

    def get(self):

        """
        Retrieval of all registered Kinds, mixins and actions
        """

        #Step[1]: Detect the body type (HTTP ,JSON:OCCI or OCCI+JSON) if there is a body:

        if not (self.req.headers.__contains__('content_type')) or self.req.body is "":

            var,self.res.status_code = self.jungler.channel_get_all_categories()

        else:

            jreq = self.req_adapter.convert_request_category_content(self.req)

            #Step[2]: Treat the converted data:
            if jreq is None:

                self.res.status_code = return_code['Not Acceptable']
                self.res.body = self.req.content_type + " is an unknown request content type"

            else:

                var,self.res.status_code = self.jungler.channel_get_filtered_categories(jreq)



        #Step[3]: Adapt the response to the required accept-type

        if self.res.status_code == return_code['OK']:

            self.res = self.res_adapter.convert_response_category_content(self.res,var)

        else:
            self.res.content_type = "text/html"
            self.res.body = var

        return self.res

    def post(self):
        """
        Create new mixin or kind or action document in the database

        """

        #Step[1]: Detect the body type (HTTP ,JSON:OCCI or OCCI+JSON)

        jBody = self.req_adapter.convert_request_category_content(self.req)

        if jBody is None:

            self.res.status_code = return_code['Not Acceptable']
            self.res.body = self.req.content_type + " is an unknown request content type"

        else:
            #add the JSON to database along with other attributes
            self.res.body,self.res.status_code = self.jungler.channel_register_categories(jBody)

        return self.res

    def put(self):

        """
        Update the document specific to the id provided in the request with new data

        """

        #Step[1]: Detect the body type (HTTP ,JSON:OCCI or OCCI+JSON)

        jBody = self.req_adapter.convert_request_category_content(self.req)

        if jBody is None:

            self.res.status_code = return_code['Not Acceptable']
            self.res.body = self.req.content_type + " is an unknown request content type"

        else:
        #Step[2]: Update new data from the request

            self.res.body, self.res.status_code = self.jungler.channel_update_categories(jBody)

        return self.res

    def delete(self):
        """

        Delete a category document using the data provided in the request

        """
        #Step[1]: Detect the body type (HTTP ,JSON:OCCI or OCCI+JSON)

        jBody = self.req_adapter.convert_request_category_content(self.req)

        if jBody is None:

            self.res.status_code = return_code['Not Acceptable']
            self.res.body = self.req.content_type + " is an unknown request content type"

        else:

            self.res.body,self.res.status_code= self.jungler.channel_delete_categories(jBody)

        return self.res




