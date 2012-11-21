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
Created on Oct 03, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@version: 0.3
@license: LGPL - Lesser General Public License
"""

import pyocni.pyocni_tools.config as config
try:
    import simplejson as json
except ImportError:
    import json

from pyocni.suppliers.resourceSupplier import ResourceSupplier


# getting the Logger
logger = config.logger

class ResourceDataBaker():
    """
    DataBaker prepares resources (extracted by the supplier from DB) for Junglers
    """

    def __init__(self):

        self.resource_sup = ResourceSupplier()

    def bake_to_put_single(self,path_url):
        """
        Prepare data for creating custom single resource method
        @param: path_url: Path of resource
        """

        #Step[1]: get the data from the supplier
        query1 = self.resource_sup.get_for_register_entities()
        if query1 is None:
            return None,None
        else:

            db_occi_ids_locs = list()
            #Step[2]: prepare data
            for q in query1:
                db_occi_ids_locs.append({"OCCI_ID" : q['key'],"OCCI_Location":q['value']})
            #Step[3]: get more data
            query2 = self.resource_sup.get_my_resources(path_url)

            if query2 is None:
                return None,None
            else:

                db_nb_resources = query2.count()
            #Step[4]: return all data
            return db_occi_ids_locs,db_nb_resources

    def bake_to_put_single_updateCase(self,path_url):

        """
        Prepare data for update single resource method
        @param path_url: URL of the resource
        """

        #Step[1]: Get data from suppliers
        query = self.resource_sup.get_for_update_entities(path_url)

        if query is None:

            return None
        else:
            #Step[2]: prepare data
            to_update = query.first()['value']

        #Step[3]: return Data
        return to_update

    def bake_to_get_single_res(self, path_url):

        """
        Prepare data for get single resource method
        @param path_url: URL of the resource
        """

        #Step[1]: get data from supplier
        query = self.resource_sup.get_my_resources(path_url)

        if query is None:
            return None,None
        else:
            if query.count() is 0:
                return 0,0
            else:
                #Step[2]: prepare data
                if query.first()['value'][0] == "Resource":
                    res = { "resources": [query.first()['value'][1]]}
                else:
                    res = { "links": [query.first()['value'][1]]}

                #Step[3]: return data
                return res,query.first()['value'][1]

    def bake_to_post_single(self, path_url):

        """
        Prepare data for post single resource
        @param path_url: URL of the resource
        """

        #Step[1]: get the data
        query = self.resource_sup.get_for_register_entities()

        if query is None:
            return None,None

        else:
            db_occi_ids_locs = list()
            #Step[2]: prepare data
            for q in query:
                db_occi_ids_locs.append({"OCCI_ID" : q['key'],"OCCI_Location":q['value']})

            #Step[3]: Get more data
            query2 = self.resource_sup.get_for_update_entities(path_url)
            if query2 is None:
                return None,None

            #Step[4]: return data
            elif query2.count() is 0:
                return db_occi_ids_locs,0

            else:
                return db_occi_ids_locs,query2.first()['value']

    def bake_to_delete_single_resource(self, path_url):
        """
        Prepare data for delete single resource method
        @param path_url: URL of the resource
        """
        #Step[1]: get data
        query = self.resource_sup.get_for_update_entities(path_url)

        if query is None:
            return None,None

        elif query.count() is 0:
            return 0,None

        else:
            #Step[2]: prepare data, then return it
            return query.count(),query.first()['value']

    def bake_to_trigger_action_on_single_resource(self, path_url):
        """
        Prepare data for trigger an action on single resource method
        @param path_url: URL of the resource
        """
        #Step[1]: Get data from supplier
        query = self.resource_sup.get_for_trigger_action(path_url)

        if query is None:
            return None,None

        elif query.count() is 0:
            return 0,None

        else:
            #Step[2]: prepare and then return the data
            return query.count(), query.first()['value']

    def bake_to_get_provider(self,kind_id):
        """
        Prepare data for get provider method
        @param kind_id: kind OCCI ID
        """
        #Step[1]: Get the data
        query = self.resource_sup.get_providers(kind_id)

        if query is None:
            return None
        else:
            #Step[2]: return data
            return query.first()['value']

    def bake_to_post_multi_resources_2a(self):
        """
        Prepare for post multi resources method (scenario 2a)
        """
        #Step[1]: get data
        query = self.resource_sup.get_for_register_entities()

        if query is None:
            return None
        else:
            #Step[2]: prepare data
            db_occi_ids_locs = list()
            for q in query:
                db_occi_ids_locs.append({"OCCI_ID" : q['key'],"OCCI_Location":q['value']})
            #Step[3]: return data
            return  db_occi_ids_locs

    def bake_to_post_multi_resources_2b(self,url_path):
        """
        Prepare data for post on multi resources 2b scenario
        @param url_path: resource URL
        """
        #Step[1]: get data

        query = self.resource_sup.get_my_mixins(url_path)

        if query is None:
            return None,None

        elif query.count() is 0:
            return 0,None

        else:
            #Step[2]: return data
            return query.count(), query.first()['value']


    def bake_to_post_multi_resources_2b2(self,OCCI_locations):

        """
        Prepare data for post on mutli resource 2b2 scenario
        @param OCCI_locations: OCCI locations of resources
        """

        db_docs = list()

        for item in OCCI_locations:
           #Step[1]: get data
           query = self.resource_sup.get_for_associate_mixin(item)

           if query is None:
               return None

           elif query.count() is 0:

               logger.error("===== bake_to_post_multi_resources_2b2  : " + item + "was not found =====")
               return None

           else:
                #Step[2]: prepare data
                q = query.first()
                db_docs.append(q['value'])
        #Step[3]: return data
        return db_docs

    def bake_to_get_all_entities(self, cat_type,cat_id):

        """
        Prepare data for get all entities method
        @param cat_type: Category type (kind/mixin)
        @param cat_id: OCCI category ID
        """

        #Step[1]: get data

        if cat_type == "Kind":

            query = self.resource_sup.get_entities_of_kind(cat_id)

        elif cat_type == "Mixin":

            query = self.resource_sup.get_entities_of_mixin(cat_id)

        else:

            return None

        to_return_res = list()
        to_return_link = list()
        #Step[2]: prepare data

        for entity in query:

            if entity['value'][1] == "Resource":
                to_return_res.append(entity['value'][0])
            else:
                to_return_link.append((entity['value'][0]))

        result = to_return_res + to_return_link
        #Step[3]: return data
        return result

    def bake_to_channel_get_all_entities(self, req_path):

        """
        Prepare data for channel get all entities method
        @param req_path: path of the request
        """
        #Step[1]: get data
        query = self.resource_sup.get_for_get_entities(req_path)

        if query is None:
            return None
        elif query.count() is 0:
            return 0
        else:
            #Step[2]: return data
            return query

    def bake_to_get_on_path(self):

        """
        Prepare data for get on path method
        """
        query = self.resource_sup.get_my_occi_locations()
        if query is None:
            return None
        else:
            occi_location = list()

            for q in query:
                occi_location.append(q['value'])

            return occi_location

    def bake_to_get_on_path_filtered(self,locations):

        """
        Prepare data for get on path filtered method
        @param locations: location to look for
        """

        descriptions = list()
        #Step[1]: get data

        for loc in locations:
            query = self.resource_sup.get_my_resources(loc)
            if query is None:
                return None
            else:
                descriptions.append({'OCCI_Description' : query.first()['value'][1],'OCCI_ID':loc})
        #Step[2]: return data
        return descriptions

    def bake_to_get_filtered_entities(self, entities):

        """
        Prepare data for get filtered entities
        @param entities: OCCI ID of entities
        """

        descriptions_res = list()
        descriptions_link = list()

        #Step[1]: Get data
        for entity in entities:
            query = self.resource_sup.get_for_get_filtered(entity)

            if query is None:
                return None,None
            else:
                #Step[2]: prepare data
                if query.first()['value'][1] == "Resource":
                    descriptions_res.append({'OCCI_ID' : entity,'OCCI_Description' : query.first()['value'][0]})
                else:
                    descriptions_link.append({'OCCI_ID' : entity,'OCCI_Description' : query.first()['value'][0]})
        #Step[3]: return data
        return descriptions_res,descriptions_link

    def bake_to_get_filtered_entities_2(self, result):

        """
        Prepare data for get filtered entities method scenario 2
        @param result: resource OCCI location
        """
        occi_descriptions = list()
        #Step[1]: get data
        for item in result:

            res = self.resource_sup.get_my_resources(item)
            if res is None:
                return None
            else:
                #Step[2]: prepare data
                occi_descriptions.append(res['value'][1])
        #Step[3]: return data
        return occi_descriptions

    def bake_to_channel_trigger_actions(self, req_url):
        """
        Prepare data for channgel trigger actions method
        @param req_url: URL request
        """
        #Step[1]: get data
        query = self.resource_sup.get_for_get_entities(req_url)

        if query is None:
            return None,None

        elif query.count() is 0:
            return 0,0

        else:
            #Step[2]: prepare data
            occi_id = query.first()['value'][0]
            occi_type = query.first()['value'][1]

            #Get resources that has this mixin or kind
            if occi_type == "Kind":
                query2 = self.resource_sup.get_entities_of_kind(occi_id)

            else:
                query2 = self.resource_sup.get_entities_of_mixin(occi_id)

            if query2 is None:
                return None,None

            else:
                entity_kind_ids = list()
                for q in query2:
                    entity = q['value'][0]
                    query3 = self.resource_sup.get_for_trigger_action(entity)
                    entity_kind_ids.append(query3.first()['value'][0])
                #Step[3]: return data
                return entity_kind_ids,query2

    def bake_to_get_default_attributes(self, req_path):
        """
        Prepare data to get default attributes
        @param req_path: URL of the request
        """

        #Step[1]: get data
        query = self.resource_sup.get_default_attributes_from_kind(req_path)

        if query is None:
            return None
        else:
            #Step[2]: prepare data
            res = recursive_for_default_attributes(query.first()['value'])

            default = {}
            for item in res:
                default = (cnv_attribute_from_http_to_json(item+"=None",json_result=default))
            #Step[3]: return data
            return default

    def recursive_get_attribute_names(self,kind_attribute_description):

        for key in kind_attribute_description.keys():
            if type(kind_attribute_description[key]) is dict:
                self.recursive_get_attribute_names(kind_attribute_description)

    def bake_to_delete_on_path(self):

        query = self.resource_sup.get_delete_on_path()

        if query is None:
            return None, None
        else:
            doc_locations = list()
            occi_locations = list()
            for q in query:
                doc_locations.append({'_id': q['value'][0], '_rev': q['value'][1]})
                occi_locations.append(q['key'])

            return occi_locations, doc_locations

#=======================================================================================================================
#                                                   Independant functions
#=======================================================================================================================
def recursive_for_default_attributes(attributes):
    """
    Method to extract attributes from kind desctiption and complete the missing ones in the resource description
    """

    att_http = list()
    for key in attributes.keys():
        if type(attributes[key]) is dict:
            items = recursive_for_default_attributes(attributes[key])
            for item in items:
                if not (item.find('{')):
                    att_http.append(key + item)
                else:
                    att_http.append(key + "." + item)
        else:
            attributes = [""]
            return attributes
    final_att = list()
    for item in att_http:
        if item.endswith('.'):
            final_att.append(item[:-1])
        else:
            final_att.append(item)
    return final_att

def cnv_attribute_from_http_to_json(attribute,json_result={}):
    """

    method to convert and add one OCCI HTTP attribute to an OCCI JSON object

    # the attribute 'attribute' contains the OCCI HTTP Attribute. e.g. 'occi.compute.hostname="foobar"'
    # the attribute 'json_result' contains an OCCI JSON object. e.g. {} or {'occi': {'compute': {'cores': 2, 'hostname': 'foobar'}}}
    """
    attribute_partitioned = attribute.partition('=')
    attribute_name = attribute_partitioned[0]
    attribute_value = attribute_partitioned[2]
    attribute_name_partitioned = attribute_name.split('.')

    a = json_result
    for i in range(len(attribute_name_partitioned)):
        if a.has_key(attribute_name_partitioned[i]):
            if i < (len(attribute_name_partitioned) - 1):
                a = a[attribute_name_partitioned[i]]
            else:
                try:
                    a[attribute_name_partitioned[i]] = json.loads(attribute_value)
                except Exception :
                    a[attribute_name_partitioned[i]] = attribute_value

        else:
            if i < (len(attribute_name_partitioned) - 1):
                a[attribute_name_partitioned[i]] = {}
                a = a[attribute_name_partitioned[i]]
                json_result.update(a)
            else:
                try:
                    a[attribute_name_partitioned[i]] = json.loads(attribute_value)
                except Exception :
                    a[attribute_name_partitioned[i]] = attribute_value

    return json_result











