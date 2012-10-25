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

try:
    import simplejson as json
except ImportError:
    import json
import pyocni.adapters.cnv_toJSON as extractor
import pyocni.pyocni_tools.uuid_Generator as generator

class From_Text_Plain_to_JSON():

    def format_text_plain_categories_to_json(self, var):
        """
        Converts a HTTP text/plain category into a JSON category
        Args:
            @param var: HTTP text/plain category
        """
        res = extractor.extract_categories_from_body(var)

        kind_list = list()
        mix_list = list()
        act_list = list()

        for item in res:

            term,scheme,ht_class,title,rel,location,attributes,actions = extractor.splitter(item)
            if ht_class == "kind":
                kind_list.append(assemble_category(term,scheme,title,rel,location,attributes,actions))
            elif ht_class == "mixin":
                mix_list.append(assemble_category(term,scheme,title,rel,location,attributes,actions))
            elif ht_class == "action":
                act_list.append(assemble_category(term,scheme,title,rel,location,attributes,actions))

        categories = dict()
        if len(kind_list) is not 0:
            categories['kinds'] = kind_list

        if len(mix_list) is not 0:
            categories['mixins'] = mix_list

        if len(act_list) is not 0:
            categories['actions'] = act_list

        return categories

    def format_text_plain_entity_to_json(self, body):

        kind,mixins,attributes,actions,links = extractor.get_entity_members_from_body(body)
        entity = dict()

        if kind is not None:
            entity['kind'] = kind

        if len(mixins) is not 0:
            entity['mixins'] = mixins

        if attributes is not None:
            entity['attributes'] = attributes

        if len(actions) is not 0:
            entity['actions'] = actions

        if len(links) is not 0:
            entity['links'] = links

        entity['id'] = generator.get_UUID()

        return {'resources' : [entity]}

    def format_text_plain_entity_to_json_v2(self, body):

        kind,mixins,attributes,actions,links = extractor.get_entity_members_from_body(body)
        entity = dict()

        if kind is not None:
            entity['kind'] = kind

        if len(mixins) is not 0:
            entity['mixins'] = mixins

        if attributes is not None:
            entity['attributes'] = attributes

        if len(actions) is not 0:
            entity['actions'] = actions

        if len(links) is not 0:
            entity['links'] = links

        return {'resources' : [entity]}



class From_Text_OCCI_to_JSON():

    def format_text_occi_categories_to_json(self, var):
        """
        Converts a HTTP text/plain category into a JSON category
        Args:
            @param var: HTTP text/plain category
        """
        res = extractor.extract_categories_from_headers(var)

        kind_list = list()
        mix_list = list()
        act_list = list()

        for item in res:

            term,scheme,ht_class,title,rel,location,attributes,actions = extractor.splitter(item)
            if ht_class == "kind":
                kind_list.append(assemble_category(term,scheme,title,rel,location,attributes,actions))
            elif ht_class == "mixin":
                mix_list.append(assemble_category(term,scheme,title,rel,location,attributes,actions))
            elif ht_class == "action":
                act_list.append(assemble_category(term,scheme,title,rel,location,attributes,actions))

        categories = dict()
        if len(kind_list) is not 0:
            categories['kinds'] = kind_list

        if len(mix_list) is not 0:
            categories['mixins'] = mix_list

        if len(act_list) is not 0:
            categories['actions'] = act_list

        return categories

    def format_text_occi_entity_to_json(self, headers):

        kind,mixins,attributes,actions,links = extractor.get_entity_members_from_headers(headers)
        entity = dict()

        if kind is not None:
            entity['kind'] = kind

        if len(mixins) is not 0:
            entity['mixins'] = mixins

        if attributes is not None:
            entity['attributes'] = attributes

        if len(actions) is not 0:
            entity['actions'] = actions

        if len(links) is not 0:
            entity['links'] = links

        entity['id'] = generator.get_UUID()

        return {'resources' : [entity]}

    def format_text_occi_entity_to_json_v2(self, headers):

        kind,mixins,attributes,actions,links = extractor.get_entity_members_from_headers(headers)
        entity = dict()

        if kind is not None:
            entity['kind'] = kind

        if len(mixins) is not 0:
            entity['mixins'] = mixins

        if attributes is not None:
            entity['attributes'] = attributes

        if len(actions) is not 0:
            entity['actions'] = actions

        if len(links) is not 0:
            entity['links'] = links

        return {'resources' : [entity]}


def assemble_category(term,scheme,title,rel,location,attributes,actions):
    """
    Creates a JSON category object
    """
    category = dict()
    if term is not None:
        category['term'] = term
    if scheme is not None:
        category['scheme'] = scheme
    if title is not None:
        category['title'] = title
    if rel is not None:
        category['related'] = extractor.create_JSON_format_relateds(rel)
    if attributes is not None:
        category['attributes'] = extractor.create_JSON_format_attributes (attributes)
    if actions is not None:
        category['actions'] = extractor.create_JSON_format_actions(actions)
    if location is not None:
        category['location'] = location

    return category

