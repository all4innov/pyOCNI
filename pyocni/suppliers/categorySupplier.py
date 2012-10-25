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

class CategorySupplier():
    """
    Consults the database to get the data asked for by the dataBakers
    """
    def __init__(self):

        self.database = config.prepare_PyOCNI_db()

    def get_all_categories(self):

        try:
            query = self.database.view('/db_views/for_get_categories')
        except Exception as e:
            logger.error("===== Get all categories : " + e.message + " ===== ")
            return None

        return query

    def get_ids_and_location_categories(self):

        try:
            query = self.database.view('/db_views/for_register_categories')
        except Exception as e:
            logger.error("===== Get_ids_and_location_categories : " + e.message + " ===== ")
            return None

        return query

    def get_ids_and_docs_categories(self):

        try:
            query = self.database.view('/db_views/for_update_categories')
        except Exception as e:
            logger.error("===== Get_ids_and_docs_categories : " + e.message + " ===== ")
            return None

        return query

    def get_ids_categories(self):

        try:
            query = self.database.view('/db_views/for_delete_categories')
        except Exception as e:
            logger.error("===== Get_ids_categories : " + e.message + " ===== ")
            return None

        return query

    def get_entities_of_mixin(self, occi_id):

        try:
            query = self.database.view('/db_views/entities_of_mixin_v2',key =occi_id)
        except Exception as e:
            logger.error("===== Get_entities_of_mixin : " + e.message + " ===== ")
            return None

        return query