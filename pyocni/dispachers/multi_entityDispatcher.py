from webob import Response,Request
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
    Dispaches operation on kinds, mixins and actions
    """
    def __init__(self,req,location=None,idontknow=None,idontcare=None):

        self.req = req

        self.location=location

        self.idontcare =idontcare
        self.idontknow=idontknow

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
        Create a new entity instance or trigger an action on all resources belonging to a kind or attach a mixin to a
        resource instance

        """

        #Step[1]: Detect the body type (HTTP ,OCCI:JSON or OCCI+JSON)

   
        jBody = self.req_adapter.convert_request_entity_content(self.req)

        if jBody is None:

            self.res.status_code = return_code['Not Acceptable']
            self.res.body = self.req.content_type + " is an unknown request content type"
    
        else:
            #Step[2]: Treat the data and define what the request really wants:

            if self.req.params.has_key('action'):
                self.triggered_action = self.req.params['action']

            #add the JSON to database along with other attributes
            if self.triggered_action is None:

                var,self.res.status_code = self.jungler.channel_post_multi_resources(jBody,self.path_url)

                if self.res.status_code == return_code['OK, and location returned']:
                    self.res_adapter.convert_response_entity_multi_location_content(var,self.res)

                else:
                    self.res.content_type = "text/html"
                    self.res.body = str(var)

            else:
                self.res.body,self.res.status_code = self.jungler.channel_trigger_actions(jBody,self.path_url,self.triggered_action)

            return self.res

    def get(self):
        """
        Gets entities belonging to a kind or a mixin

        """

        #Detect the body type (HTTP ,OCCI:JSON or OCCI+JSON)

        if  self.req.content_type == 'text/occi' or (self.req.body != "") or self.req.content_type == 'application/occi+json':

            jBody = self.req_adapter.convert_request_entity_content_v2(self.req)

            if jBody is None:

                self.res.status_code = return_code['Not Acceptable']
                self.res.body = self.req.content_type + " is an unknown request content type"

            else:
                var,self.res.status_code = self.jungler.channel_get_filtered_entities(self.path_url,jBody)

        else:

            var,self.res.status_code = self.jungler.channel_get_all_entities(self.path_url,"")

        if self.res.status_code == return_code['OK']:

            self.res_adapter.convert_response_entity_multi_x_occi_location_content(var,self.res)

        else:
            self.res.content_type = "text/html"
            self.res.body = str(var)

        return self.res

    def put(self):
        """
        Update the mixin collection of entities

        """

        #Detect the body type (HTTP ,OCCI:JSON or OCCI+JSON)
        #Not implemented yet for text/plain and text/occi formats


        jBody = self.req_adapter.convert_request_category_content(self.req)

        if jBody is None:

            self.res.status_code = return_code['Not Acceptable']
            self.res.body = self.req.content_type + " is an unknown request content type"
        else:

            #add the JSON to database along with other attributes
            self.res.body,self.res.status_code = self.jungler.channel_put_multi(jBody,self.path_url)

        return self.res

    def delete(self):
        """
        Dissociates a resource instance from a mixin

        """

        #Detect the body type (HTTP ,OCCI:JSON or OCCI+JSON)
        #Not implemented yet for text/plain and text/occi formats

        jBody = self.req_adapter.convert_request_category_content(self.req)

        if jBody is None:

            self.res.status_code = return_code['Not Acceptable']
            self.res.body = self.req.content_type + " is an unknown request content type"
        else:


            if self.req.body is not "":
                #This is a dissociate mixin request:
                self.res.body,self.res.status_code = self.jungler.channel_delete_multi(jBody,self.path_url)
            else:
                #This is a delete on path request:
                self.jungler_p.channel_delete_on_path(self.path_url)

        return self.res