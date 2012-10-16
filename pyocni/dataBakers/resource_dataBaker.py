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

    def __init__(self):

        self.resource_sup = ResourceSupplier()

    def bake_to_put_single(self,path_url):

        query1 = self.resource_sup.get_for_register_entities()
        if query1 is None:
            return None,None
        else:

            db_occi_ids_locs = list()

            for q in query1:
                db_occi_ids_locs.append({"OCCI_ID" : q['key'],"OCCI_Location":q['value']})

            query2 = self.resource_sup.get_my_resources(path_url)
            if query2 is None:
                return None,None
            else:

                db_nb_resources = query2.count()

            return db_occi_ids_locs,db_nb_resources

    def bake_to_put_single_updateCase(self,path_url):

        query = self.resource_sup.get_for_update_entities(path_url)

        if query is None:

            return None
        else:
            to_update = query.first()['value']
            old_data = to_update['OCCI_Description']

        return old_data

    def bake_to_get_single_res(self, path_url):

        query = self.resource_sup.get_my_resources()

        if query is None:
            return None,None
        else:
            if query.count() is 0:
                return 0,0
            else:
                if query.first()['value'][0] == "Resource":
                    res = { "resources": [query.first()['value'][1]]}
                else:
                    res = { "links": [query.first()['value'][1]]}

                return res,query.first()['value'][1]

    def bake_to_post_single(self, path_url):

        query = self.resource_sup.get_for_register_entities()

        if query is None:
            return None,None

        else:
            db_occi_ids_locs = list()

            for q in query:
                db_occi_ids_locs.append({"OCCI_ID" : q['key'],"OCCI_Location":q['value']})

            query2 = self.resource_sup.get_for_update_entities(path_url)

            if query2 is None:
                return None,None

            elif query2.count():
                return db_occi_ids_locs,0

            else:
                return db_occi_ids_locs,query2.first()['value']

    def bake_to_delete_single_resource(self, path_url):

        query = self.resource_sup.get_for_update_entities(path_url)

        if query is None:
            return None,None

        elif query.count() is 0:
            return 0,None

        else:
            return query.count(),query.first()['value']

    def bake_to_trigger_action_on_single_resource(self, path_url):

        query = self.resource_sup.get_for_trigger_action(path_url)

        if query is None:
            return None,None

        elif query.count() is 0:
            return 0,None

        else:
            return query.count(), query.first()['value']

    def bake_to_get_provider(self,kind_id):

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
                db_occi_ids_locs.append({"OCCI_ID" : q['key'],"OCCI_Location":q['value']})

            return  db_occi_ids_locs

    def bake_to_post_multi_resources_2b(self,url_path):

        query = self.resource_sup.get_my_mixins(url_path)

        if query is None:
            return None,None

        elif query.count() is 0:
            return 0,None

        else:
            return query.count(), query.first()['value']


    def bake_to_post_multi_resources_2b2(self,OCCI_locations):

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

    def bake_to_get_all_entities(self, cat_type,cat_id):



        if cat_type == "Kind":

            query = self.resource_sup.get_entities_of_kind(cat_id)

        elif cat_type == "Mixin":

            query = self.resource_sup.get_entities_of_mixin(cat_id)

        else:

            return None


        occi_descriptions = list()

        for entity in query:
            res = self.resource_sup.get_my_resources(entity['value'][0])

            if res is None:
                return None
            else:
                occi_descriptions.append(res['value'][1])

        to_return_res = list()
        to_return_link = list()

        for entity in occi_descriptions:

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

    def bake_to_get_on_path_filtered(self,locations):

        descriptions = list()
        for loc in locations:
            query = self.resource_sup.get_my_resources(loc)
            if query is None:
                return None
            else:
                descriptions.append({'OCCI_Description' : query.first()['value'],'OCCI_ID':loc})

        return descriptions

    def bake_to_get_filtered_entities(self, entities):

        descriptions_res = list()
        descriptions_link = list()

        for entity in entities:
            query = self.resource_sup.get_for_get_filtered(entity)
            if query is None:
                return None,None
            else:
                if query.first()['value'][1] == "Resource":
                    descriptions_res.append({'OCCI_ID' : entity,'OCCI_Description' : query.first()['value'][0]})
                else:
                    descriptions_link.append({'OCCI_ID' : entity,'OCCI_Description' : query.first()['value'][0]})

            return descriptions_res,descriptions_link

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
            return None,None

        elif query.count() is 0:
            return 0,0

        else:
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

                return entity_kind_ids,query2















