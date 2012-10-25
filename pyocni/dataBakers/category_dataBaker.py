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
from pyocni.suppliers.categorySupplier import CategorySupplier
import pyocni.pyocni_tools.occi_Joker as joker

# getting the Logger
logger = config.logger

class CategoryDataBaker():

    #DataBaker's role is to prepare the data for Junglers

    def __init__(self):

        self.category_sup = CategorySupplier()

    def bake_to_get_all_categories(self):
        """
        Adapt categories to the standard data
        """
        db_kinds = list()
        db_mixins = list()
        db_actions = list()

        #Step[1]: Get all the categories from the supplier

        query = self.category_sup.get_all_categories()
        result = None
        #Step[2]: Adapt categories to the required format

        if query is None:

            return None

        else:
            for q in query:
                if q['key'] == "Kind":
                    db_kinds.append(q['value'])
                elif q['key'] == "Mixin":
                    db_mixins.append(q['value'])
                elif q['key'] == "Action":
                    db_actions.append(q['value'])

            result = {'kinds': db_kinds, 'mixins': db_mixins, 'actions': db_actions}

        #Step[3]: Return the results to the calling jungler

        return result

    def bake_to_register_categories(self):

        query = self.category_sup.get_ids_and_location_categories()

        if query is None:
            return None
        else:
            db_occi_ids = list()
            db_occi_locs = list()

            for q in query:
                db_occi_ids.append( q['key'])
                db_occi_locs.append(q['value'])

            return db_occi_ids,db_occi_locs

    def bake_to_update_categories(self):

        query = self.category_sup.get_ids_and_docs_categories()

        if query is None:
            return None
        else:
            db_occi_id_doc = list()
            for q in query:
                db_occi_id_doc.append( { "OCCI_ID" : q['key'],"Doc" : q['value']})

            return db_occi_id_doc

    def bake_to_delete_categories(self):

        query = self.category_sup.get_ids_categories()
        if query is None:
            return None
        else:
            db_occi_id = list()
            for q in query:
                if q['key'] is not None:
                    db_occi_id.append( { "_id" : q['key'],"_rev" : q['value'][0], "OCCI_ID" : q['value'][1]})
            return db_occi_id

    def bake_to_delete_categories_mixins(self,mixins):

        db_mixin_entities = list()

        for mix in mixins:

            occi_id = joker.get_description_id(mix)
            query = self.category_sup.get_entities_of_mixin(occi_id)

            if query is None:
                return None
            else:
                if query.count() is not 0:
                    db_mixin_entities.append(query.first()['value'])

        return db_mixin_entities



