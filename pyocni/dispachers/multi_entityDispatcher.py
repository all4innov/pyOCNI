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

from webob import Response, Request
from pyocni.adapters.i_ResponseAdapter import ResponseAdapter
from pyocni.adapters.i_RequestAdapter import RequestAdapter
from pyocni.junglers.multi_entityJungler import MultiEntityJungler
from pyocni.junglers.pathJungler import PathManager
from pyocni.pyocni_tools.config import return_code

try:
    import simplejson as json
except ImportError:
    import json

#=======================================================================================================================
#                                           MultiEntityInterface
#=======================================================================================================================
class MultiEntityDispatcher(object):
    """
    Dispatches requests concerning multiple entities

    """

    def __init__(self, req, location=None, idontknow=None, idontcare=None):

        self.req = req

        self.location = location

        self.idontcare = idontcare
        self.idontknow = idontknow

        self.triggered_action = None
        self.path_url = self.req.path_url

        self.res = Response()
        self.res.content_type = str(req.accept)
        self.res.server = 'ocni-server/1.1 (linux) OCNI/1.1'

        self.req_adapter = RequestAdapter()
        self.res_adapter = ResponseAdapter()
        self.jungler = MultiEntityJungler()
        self.jungler_p = PathManager()


    def post(self):
        """
        Create a new entity or trigger an action on all resources belonging to a kind or attach a mixin to a
        resource instance

        """

        #Step[1]: Detect the data type (HTTP ,OCCI:JSON or OCCI+JSON)


        jBody = self.req_adapter.convert_request_entity_content(self.req)

        if jBody is None:
            self.res.status_code = return_code['Not Acceptable']
            self.res.body = self.req.content_type + " is an unknown request content type"

        else:
            #Step[2]: Identify the action name if there is one:

            if self.req.params.has_key('action'):
                self.triggered_action = self.req.params['action']

            #Step[3a]: Dispatch a post request

            if self.triggered_action is None:

                var, self.res.status_code = self.jungler.channel_post_multi_resources(jBody, self.path_url)

                #Step[4a]: Adapt response to the required Accept-Type

                if self.res.status_code == return_code['OK, and location returned']:
                    self.res_adapter.convert_response_entity_multi_location_content(var, self.res)

                else:
                    self.res.content_type = "text/html"
                    self.res.body = str(var)

            #Step[3b]: Trigger an action on all resources belonging to a kind
            else:
                self.res.body, self.res.status_code = self.jungler.channel_trigger_actions(jBody, self.path_url,
                    self.triggered_action)

            return self.res

    def get(self):
        """
        Get entities belonging to a kind or a mixin

        """

        #Step[1]: Detect the body type (HTTP ,OCCI:JSON or OCCI+JSON)

        if  self.req.content_type == 'text/occi' or (
        self.req.body != ""):

            jBody = self.req_adapter.convert_request_entity_content_v2(self.req)

            if jBody is None:
                self.res.status_code = return_code['Not Acceptable']
                self.res.body = self.req.content_type + " is an unknown request content type"

            else:
                #Step[2a]: Retrieve entities matching the filter provided
                var, self.res.status_code = self.jungler.channel_get_filtered_entities(self.path_url, jBody)

        else:
            #Step[2b]: Retrieve all the entities
            var, self.res.status_code = self.jungler.channel_get_all_entities(self.path_url, "")

        #Step[3]: Adapt the response to the format defined in the Accept-Type header

        if self.res.status_code == return_code['OK']:

            self.res_adapter.convert_response_entity_multi_x_occi_location_content(var, self.res)

        else:
            self.res.content_type = "text/html"
            self.res.body = str(var)

        return self.res

    def put(self):
        """
        Fully update the mixin collection of entities

        """

        #Step[1]: Detect the body type (HTTP ,OCCI:JSON or OCCI+JSON)

        jBody = self.req_adapter.convert_request_category_content(self.req)

        if jBody is None:
            self.res.status_code = return_code['Not Acceptable']
            self.res.body = self.req.content_type + " is an unknown request content type"
        else:

            #Step[2]: Fully update the mixin collection of entities

            self.res.body, self.res.status_code = self.jungler.channel_put_multi(jBody, self.path_url)

        return self.res

    def delete(self):
        """
        Dissociates a resource instance from a mixin or delete all resource under a path

        """

        #Step[1]: Detect the body type (HTTP ,OCCI:JSON or OCCI+JSON)
        if  self.req.content_type == 'text/occi' or (
            self.req.body != ""):

            jBody = self.req_adapter.convert_request_category_content(self.req)

            if jBody is None:
                self.res.status_code = return_code['Not Acceptable']
                self.res.body = self.req.content_type + " is an unknown request content type"

                #Step[2a]: This is a dissociate mixin request
                self.res.body, self.res.status_code = self.jungler.channel_delete_multi(jBody, self.path_url)
        else:
                #Step[2b]: This is a delete on path request:
                self.jungler_p.channel_delete_on_path(self.path_url)

        return self.res