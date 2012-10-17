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
# getting the Logger
logger = config.logger

class ResourceSupplier():
    """
    Consults the database to get the data asked for by the dataBakers
    """
    def __init__(self):

        self.database = config.prepare_PyOCNI_db()

#    def get_for_register_categories(self):
#
#        try:
#            query = self.database.view('/db_views/for_register_categories')
#        except Exception as e:
#            logger.error("===== Get_ids_and_location_categories : " + e.message + " ===== ")
#            return None
#
#        return query

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










