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
Created on Jun 21, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@license: Apache License, Version 2.0
"""

from webob import Response, Request
from pyocni.adapters.i_ResponseAdapter import ResponseAdapter
from pyocni.adapters.i_RequestAdapter import RequestAdapter
from pyocni.junglers.single_entityJungler import SingleEntityJungler
from pyocni.pyocni_tools.config import return_code

try:
    import simplejson as json
except ImportError:
    import json


#=======================================================================================================================
#                                           SingleEntityInterface
#=======================================================================================================================
class SingleEntityDispatcher(object):
    """
    Dispatches requests concerning a single entity

    """

    def __init__(self, req, location, idontknow=None, idontcare=None):

        self.req = req

        self.location = location
        self.idontknow = idontknow
        self.idontcare = idontcare

        self.path_url = self.req.path_url
        self.triggered_action = None

        self.res = Response()
        self.res.content_type = str(req.accept)
        self.res.server = 'ocni-server/1.1 (linux) OCNI/1.1'

        self.req_adapter = RequestAdapter()
        self.res_adapter = ResponseAdapter()
        self.jungler = SingleEntityJungler()


    def put(self):
        """
        Create a new entity instance with a customized URL or perform a full update of the resource

        """
        #Step[1]: Detect the data type (HTTP ,JSON:OCCI or OCCI+JSON)

        jBody = self.req_adapter.convert_request_entity_content(self.req)

        if jBody is None:
            self.res.status = return_code['Not Acceptable']
            self.res.body = self.req.content_type + " is an unknown request content type"

        else:
            #Step[2]: create the resource with custom URL
            var, self.res.status = self.jungler.channel_put_single_resource(jBody, self.path_url)

            #Step[3]: Adapt the response to the required accept-type

            if self.res.status == return_code['OK, and location returned']:
                self.res = self.res_adapter.convert_response_entity_location_content(var, self.res)
            else:
                self.res.content_type = "text/html"
                self.res.body = var

        #Step[4]: Send back the response to the caller

        return self.res

    def get(self):
        """
        Retrieve the OCCI resource description

        """

        #Step[1]: get the resource description

        var, self.res.status = self.jungler.channel_get_single_resource(self.path_url)

        #Step[2]: Adapt the response to the required accept-type

        if self.res.status == return_code['OK']:
            self.res = self.res_adapter.convert_response_entity_content(self.res, var)

        else:
            self.res.content_type = "text/html"
            self.res.body = var

        #Step[3]: Send back the response to the caller

        return self.res

    def post(self):
        """
        Perform a partial update of a resource OCCI description or Trigger an action on a resource

        """
        #Step[1]: Identify the action name (if there is)

        if self.req.params.has_key('action'):

            self.triggered_action = self.req.params['action']

        #Step[2]: Detect the data type (HTTP ,OCCI:JSON or OCCI+JSON)

        jBody = self.req_adapter.convert_request_entity_content_v2(self.req)

        if jBody is None:
            self.res.status = return_code['Not Acceptable']
            self.res.body = self.req.content_type + " is an unknown request content type"

        else:
            #Step[3a]: Partially update the resource if there was no action defined.

            if self.triggered_action is None:

                var, self.res.status = self.jungler.channel_post_single_resource(jBody, self.path_url)

                if self.res.status == return_code['OK, and location returned']:

                    #Step[4a]: Adapt the response to the required accept-type
                    self.res = self.res_adapter.convert_response_entity_location_content(var, self.res)
                else:
                    self.res.content_type = "text/html"
                    self.res.body = var

            else:
                # Step[3b]: Trigger an action on a resource

                self.res.body, self.res.status = self.jungler.channel_triggered_action_single(jBody, self.path_url,
                    self.triggered_action)

        return self.res


    def delete(self):
        """
        Delete a resource instance

        """

        #Step[1]: Delete a single resource

        self.res.body, self.res.status = self.jungler.channel_delete_single_resource(self.path_url)

        #Step[2]: return the response back to the caller

        return self.res

