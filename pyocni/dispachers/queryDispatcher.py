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
Created on Jun 19, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@license: Apache License, Version 2.0
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
        Dispatches requests concerning the Query Interface.

    """

    def __init__(self, req):

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

        #Step[1]: Detect the data type (HTTP ,JSON:OCCI or OCCI+JSON) if there is one:

        if  self.req.content_type == 'text/occi' or (self.req.body != ""):

            jreq = self.req_adapter.convert_request_category_content(self.req)

            if jreq is None:
                self.res.status_int = return_code['Not Acceptable']
                self.res.body = self.req.content_type + " is an unknown request content type"

            else:
                #Step[2a]: Retrieve the categories matching with the filter provided in the request:
                var, self.res.status_int = self.jungler.channel_get_filtered_categories(jreq)

        else:
            #Step[2b]: Retrieve all the categories:
            var, self.res.status_int = self.jungler.channel_get_all_categories()

        #Step[3]: Adapt the response to the required accept-type

        if self.res.status_int == return_code['OK']:
            self.res = self.res_adapter.convert_response_category_content(self.res, var)

        else:
            self.res.content_type = "text/html"
            self.res.body = str(var)

        return self.res

    def post(self):
        """
        Create new mixin or kind or action document in the database

        """

        #Step[1]: Detect the data type (HTTP ,JSON:OCCI or OCCI+JSON)

        jBody = self.req_adapter.convert_request_category_content(self.req)

        if jBody is None:

            self.res.status_int = return_code['Not Acceptable']
            self.res.body = self.req.content_type + " is an unknown request content type"

        else:
            #Step[2]: Create the categories
            self.res.body, self.res.status_int = self.jungler.channel_register_categories(jBody)

        return self.res

    def put(self):
        """
        Update the document specific to the id provided in the request with new data

        """

        #Step[1]: Detect the data type (HTTP ,JSON:OCCI or OCCI+JSON):

        jBody = self.req_adapter.convert_request_category_content(self.req)

        if jBody is None:
            self.res.status_int = return_code['Not Acceptable']
            self.res.body = self.req.content_type + " is an unknown request content type"

        else:

        #Step[2]: Update the new data:
            self.res.body, self.res.status_int = self.jungler.channel_update_categories(jBody)

        return self.res

    def delete(self):
        """
        Delete a category document using the data provided in the request

        """
        #Step[1]: Detect the data type (HTTP ,JSON:OCCI or OCCI+JSON)

        jBody = self.req_adapter.convert_request_category_content(self.req)

        if jBody is None:
            self.res.status_int = return_code['Not Acceptable']
            self.res.body = self.req.content_type + " is an unknown request content type"

        else:
            #Step[2]: Delete the category
            self.res.body, self.res.status_int = self.jungler.channel_delete_categories(jBody)

        return self.res




