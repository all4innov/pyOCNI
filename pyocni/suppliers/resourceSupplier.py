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
# getting the Logger
logger = config.logger

class ResourceSupplier():
    """
    Consults the database to get the data asked for by the dataBakers
    """
    def __init__(self):

        self.database = config.prepare_PyOCNI_db()

    def get_my_resources(self,path_url):

        try:
            query = self.database.view('/db_views/my_resources',key=path_url)
        except Exception as e:
            logger.error("===== Get_resources : " + e.message + " ===== ")
            return None

        return query

    def get_for_update_entities(self,path_url):

        try:
            query = self.database.view('/db_views/for_update_entities',key=path_url)
        except Exception as e:
            logger.error("===== Get_old_occi_resource_description : " + e.message + " ===== ")
            return None

        return query

    def get_for_register_entities(self):


        try:
            query = self.database.view('/db_views/for_register_entities')
        except Exception as e:
            logger.error("===== Get_for_register_entities : " + e.message + " ===== ")
            return None

        return query

    def get_for_trigger_action(self, path_url):

        try:
            query = self.database.view('/db_views/for_trigger_action', key=path_url)
        except Exception as e:
            logger.error("===== Get_for_trigger_action : " + e.message + " ===== ")
            return None

        return query

    def get_actions_of_kind_mix(self, kind_id):

        try:
            query = self.database.view('/db_views/actions_of_kind_mix', key=kind_id)

        except Exception as e:
            logger.error("===== Get_actions_of_kind_mix : " + e.message + " ===== ")
            return None

        return query

    def get_my_mixins(self,url_path):

        try:
            query = self.database.view('/db_views/my_mixins',key = url_path)

        except Exception as e:

            logger.error("===== Get_my_mixins : " + e.message + " ===== ")
            return None

        return query

    def get_for_associate_mixin(self, item):

        try:
            query = self.database.view('/db_views/for_associate_mixin',key=[item])
        except Exception as e:
            logger.error("===== Get_for_associate_mixin : " + e.message + " ===== ")
            return None

        return query

    def get_for_get_entities(self, req_path):


        try:
            query = self.database.view('/db_views/for_get_entities',key=req_path)
        except Exception as e:
            logger.error("===== Get_for_get_entities : " + e.message + " ===== ")
            return None

        return query

    def get_entities_of_kind(self, cat_id):

        try:
            query = self.database.view('/db_views/entities_of_kind',key = cat_id)

        except Exception as e:
            logger.error("===== Get_entities_of_kind : " + e.message + " ===== ")
            return None

        return query

    def get_entities_of_mixin(self, cat_id):

        try:

            query = self.database.view('/db_views/entities_of_mixin',key = cat_id)

        except Exception as e:
            logger.error("===== Get_entities_of_mixin : " + e.message + " ===== ")
            return None

        return query

    def get_my_occi_locations(self):

        try:
            query = self.database.view('/db_views/my_occi_locations')

        except Exception as e:

            logger.error("===== Get_my_occi_locations : " + e.message + " ===== ")
            return None

        return query

    def get_for_get_filtered(self, entity):

        try:
            query = self.database.view('/db_views/for_get_filtered',key=entity)
        except Exception as e:

            logger.error("===== Get_for_get_filtered : " + e.message + " ===== ")
            return None

        return query

    def get_default_attributes_from_kind(self, req_path):

        try:
            query = self.database.view('/db_views/get_default_attributes_from_kind',key=req_path)
        except Exception as e:

            logger.error("===== Get_for_get_filtered : " + e.message + " ===== ")
            return None

        return query



def recursive_for_attribute(attributes):
    """

    """

    att_http = list()
    for key in attributes.keys():
        if type(attributes[key]) is dict:
            items = recursive_for_attribute(attributes[key])
            for item in items:
                if not (item.find('{')):
                    att_http.append(key + item)
                else:
                    att_http.append(key + "." + item)
        else:
            attributes = treat_attribute_members(attributes)
            return attributes
    final_att = list()
    for item in att_http:
        if item.endswith('.'):
            final_att.append(item[:-1])
        else:
            final_att.append(item)
    return final_att







