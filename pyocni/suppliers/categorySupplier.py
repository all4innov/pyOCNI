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