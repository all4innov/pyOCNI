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
Created on May 29, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@license: Apache License, Version 2.0
"""

import pyocni.pyocni_tools.config as config


class PostMan():

    def __init__(self):

        self.database = config.get_PyOCNI_db()

    def save_registered_docs_in_db(self,docs):

        self.database.save_docs(docs,use_uuids=True, all_or_nothing=True)

    def save_updated_docs_in_db(self, categories):

        self.database.save_docs(categories,force_update=True, all_or_nothing=True)

    def save_deleted_categories_in_db(self, categories,to_update):

        self.database.delete_docs(categories)
        self.database.save_docs(to_update,force_update=True, all_or_nothing=True)

    def save_custom_resource(self, entity):

        self.database.save_doc(entity,use_uuids=True, all_or_nothing=True)

    def delete_single_resource_in_db(self, res_value):

        self.database.delete_doc(res_value)


