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
Created on Oct 03, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@license: Apache License, Version 2.0
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
    def __init__(self):
        self.resource_sup = ResourceSupplier()

    def bake_to_put_single(self, path_url):
        query1 = self.resource_sup.get_for_register_entities()
        if query1 is None:
            return None, None
        else:
            db_occi_ids_locs = list()

            for q in query1:
                db_occi_ids_locs.append({"OCCI_ID": q['key'], "OCCI_Location": q['value']})

            query2 = self.resource_sup.get_my_resources(path_url)
            if query2 is None:
                return None, None
            else:
                db_nb_resources = query2.count()

            return db_occi_ids_locs, db_nb_resources

    def bake_to_put_single_updateCase(self, path_url):
        query = self.resource_sup.get_for_update_entities(path_url)

        if query is None:
            return None
        else:
            to_update = query.first()['value']

        return to_update

    def bake_to_get_single_res(self, path_url):
        query = self.resource_sup.get_my_resources(path_url)

        if query is None:
            return None, None
        else:
            if query.count() is 0:
                return 0, 0
            else:
                if query.first()['value'][0] == "Resource":
                    res = {"resources": [query.first()['value'][1]]}
                else:
                    res = {"links": [query.first()['value'][1]]}

                return res, query.first()['value'][1]

    def bake_to_post_single(self, path_url):
        query = self.resource_sup.get_for_register_entities()

        if query is None:
            return None, None

        else:
            db_occi_ids_locs = list()

            for q in query:
                db_occi_ids_locs.append({"OCCI_ID": q['key'], "OCCI_Location": q['value']})
            query2 = self.resource_sup.get_for_update_entities(path_url)
            if query2 is None:
                return None, None

            elif query2.count() is 0:
                return db_occi_ids_locs, 0

            else:
                return db_occi_ids_locs, query2.first()['value']

    def bake_to_delete_single_resource(self, path_url):
        query = self.resource_sup.get_for_update_entities(path_url)

        if query is None:
            return None, None

        elif query.count() is 0:
            return 0, None

        else:
            return query.count(), query.first()['value']

    def bake_to_trigger_action_on_single_resource(self, path_url):
        query = self.resource_sup.get_for_trigger_action(path_url)

        if query is None:
            return None, None

        elif query.count() is 0:
            return 0, None

        else:
            return query.count(), query.first()['value']

    def bake_to_get_provider(self, kind_id):
        query = self.resource_sup.get_actions_of_kind_mix(kind_id)

        if query is None:
            return None
        else:
            return query['value']

    def bake_to_post_multi_resources_2a(self):
        query = self.resource_sup.get_for_register_entities()

        if query is None:
            return None
        else:
            db_occi_ids_locs = list()
            for q in query:
                db_occi_ids_locs.append({"OCCI_ID": q['key'], "OCCI_Location": q['value']})

            return  db_occi_ids_locs

    def bake_to_post_multi_resources_2b(self, url_path):
        query = self.resource_sup.get_my_mixins(url_path)

        if query is None:
            return None, None

        elif query.count() is 0:
            return 0, None

        else:
            return query.count(), query.first()['value']


    def bake_to_post_multi_resources_2b2(self, OCCI_locations):
        db_docs = list()

        for item in OCCI_locations:
            query = self.resource_sup.get_for_associate_mixin(item)

            if query is None:
                return None

            elif query.count() is 0:
                logger.error("===== bake_to_post_multi_resources_2b2  : " + item + "was not found =====")
                return None

            else:
                q = query.first()
                db_docs.append(q['value'])

        return db_docs

    def bake_to_get_all_entities(self, cat_type, cat_id):
        if cat_type == "Kind":
            query = self.resource_sup.get_entities_of_kind(cat_id)

        elif cat_type == "Mixin":
            query = self.resource_sup.get_entities_of_mixin(cat_id)

        else:
            return None

        to_return_res = list()
        to_return_link = list()

        for entity in query:
            if entity['value'][1] == "Resource":
                to_return_res.append(entity['value'][0])
            else:
                to_return_link.append((entity['value'][0]))

        result = to_return_res + to_return_link

        return result

    def bake_to_channel_get_all_entities(self, req_path):
        query = self.resource_sup.get_for_get_entities(req_path)

        if query is None:
            return None
        elif query.count() is 0:
            return 0
        else:
            return query

    def bake_to_get_on_path(self):
        query = self.resource_sup.get_my_occi_locations()

        return query

    def bake_to_get_on_path_filtered(self, locations):
        descriptions = list()
        for loc in locations:
            query = self.resource_sup.get_my_resources(loc)
            if query is None:
                return None
            else:
                descriptions.append({'OCCI_Description': query.first()['value'], 'OCCI_ID': loc})

        return descriptions

    def bake_to_get_filtered_entities(self, entities):
        descriptions_res = list()
        descriptions_link = list()

        for entity in entities:
            query = self.resource_sup.get_for_get_filtered(entity)

            if query is None:
                return None, None
            else:
                if query.first()['value'][1] == "Resource":
                    descriptions_res.append({'OCCI_ID': entity, 'OCCI_Description': query.first()['value'][0]})
                else:
                    descriptions_link.append({'OCCI_ID': entity, 'OCCI_Description': query.first()['value'][0]})

        return descriptions_res, descriptions_link

    def bake_to_get_filtered_entities_2(self, result):
        occi_descriptions = list()

        for item in result:
            res = self.resource_sup.get_my_resources(item)
            if res is None:
                return None
            else:
                occi_descriptions.append(res['value'][1])

        return occi_descriptions

    def bake_to_channel_trigger_actions(self, req_url):
        query = self.resource_sup.get_for_get_entities(req_url)

        if query is None:
            return None, None

        elif query.count() is 0:
            return 0, 0

        else:
            occi_id = query.first()['value'][0]
            occi_type = query.first()['value'][1]

            #Get resources that has this mixin or kind
            if occi_type == "Kind":
                query2 = self.resource_sup.get_entities_of_kind(occi_id)

            else:
                query2 = self.resource_sup.get_entities_of_mixin(occi_id)

            if query2 is None:
                return None, None

            else:
                entity_kind_ids = list()
                for q in query2:
                    entity = q['value'][0]
                    query3 = self.resource_sup.get_for_trigger_action(entity)
                    entity_kind_ids.append(query3.first()['value'][0])

                return entity_kind_ids, query2

    def recursive_get_attribute_names(self, kind_attribute_description):
        for key in kind_attribute_description.keys():
            if type(kind_attribute_description[key]) is dict:
                self.recursive_get_attribute_names(kind_attribute_description)
                print "i am "

    def bake_to_get_default_attributes(self, req_path):
        query = self.resource_sup.get_default_attributes_from_kind(req_path)

        if query is None:
            return None
        else:
            res = recursive_for_default_attributes(query.first()['value'])

            default = {}
            for item in res:
                default = (cnv_attribute_from_http_to_json(item + "=None", json_result=default))

            return default


#=======================================================================================================================
#                                                   Independant functions
#=======================================================================================================================
def recursive_for_default_attributes(attributes):
    """

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


def cnv_attribute_from_http_to_json(attribute, json_result={}):
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
                except Exception:
                    a[attribute_name_partitioned[i]] = attribute_value

        else:
            if i < (len(attribute_name_partitioned) - 1):
                a[attribute_name_partitioned[i]] = {}
                a = a[attribute_name_partitioned[i]]
                json_result.update(a)
            else:
                try:
                    a[attribute_name_partitioned[i]] = json.loads(attribute_value)
                except Exception:
                    a[attribute_name_partitioned[i]] = attribute_value

    return json_result











