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
Created on May 29, 2012

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


from pyocni.pyocni_tools.config import return_code
from pyocni.junglers.managers.actionManager import ActionManager
from pyocni.junglers.managers.kindManager import KindManager
from pyocni.junglers.managers.mixinManager import MixinManager
from pyocni.dataBakers.category_dataBaker import CategoryDataBaker
from postMan.the_post_man import PostMan
# getting the Logger
logger = config.logger

class CategoryJungler:
    """

        Extracts category (a.k.a Kinds, Mixins and Actions) data from the database

    """

    def __init__(self):

        self.manager_k = KindManager()
        self.manager_m = MixinManager()
        self.manager_a = ActionManager()
        self.d_baker = CategoryDataBaker()
        self.PostMan = PostMan()


    def channel_register_categories(self,jreq):
        """
        Channel the post request to the right methods
        Args:
            @param jreq: Body content of the post request

        """

        #Step[1]: Get the data from the database to avoid replicates:

        db_occi_ids,db_occi_locs= self.d_baker.bake_to_register_categories()

        #Step[2]: Verify the uniqueness of the new categories:
        if (db_occi_ids is None) or (db_occi_locs is None):

            return "An error has occurred, please check log for more details",return_code['Bad Request']
        else:

            if jreq.has_key('actions'):

                logger.debug("===== channel_register_categories ==== : Actions channeled")
                new_actions,resp_code_a = self.manager_a.register_actions(jreq['actions'],db_occi_ids)

            else:
                logger.debug("===== channel_register_categories ==== : no actions found")
                new_actions = list()
                resp_code_a = return_code['OK']

            if jreq.has_key('kinds'):

                logger.debug("===== channel_register_categories ==== : Kinds channeled")
                new_kinds,resp_code_k = self.manager_k.register_kinds(jreq['kinds'],db_occi_ids)

            else:
                logger.debug("===== channel_register_categories ==== : no kinds found")
                new_kinds = list()
                resp_code_k = return_code['OK']

            if jreq.has_key('mixins'):
                logger.debug("===== channel_register_categories ==== : Mixins channeled")
                new_mixins,resp_code_m = self.manager_m.register_mixins(jreq['mixins'],db_occi_ids)
            else:
                logger.debug("===== channel_register_categories ==== : No mixins found")
                new_mixins= list()
                resp_code_m = return_code['OK']

            if resp_code_a is not return_code['OK'] or resp_code_k is not return_code['OK'] or resp_code_m is not return_code['OK']:
                return "An error has occurred, please check log for more details",return_code['Bad Request']

            else:
                #Step[3]: Save the new categories in the database
                categories = new_kinds + new_mixins + new_actions
                self.PostMan.save_registered_docs_in_db(categories)

                return "",return_code['OK']

    def channel_get_all_categories(self):
        """
        Retrieve all categories to show the server's capacity

        """
        #Step[1]: Call the dataBakers to get the Data

        res = self.d_baker.bake_to_get_all_categories()

        #Step[2]: Return all the results back to the dispatcher
        if res is None:

            return return_code['Internal Server Error'],res
        else:
            return return_code['OK'],res


    def channel_get_filtered_categories(self,jreq):
        """
        Channel the post request to the right methods
        Args:
            @param jreq: Body content of the post request

        """
        res = self.d_baker.bake_to_get_all_categories()

        #Step[2]: filter the results
        if res is None:

            return return_code['Internal Server Error'],res
        else:

            if jreq.has_key('kinds'):
                logger.debug("===== Get filtered categories : Kinds filter is found and channeled =====")
                filtered_kinds,resp_code_k = self.manager_k.get_filtered_kinds(jreq['kinds'],res['kinds'])
            else:
                logger.debug("===== Get filtered categories : No kind filter was found =====")
                filtered_kinds = ""
                resp_code_k = return_code['OK']

            if jreq.has_key('mixins'):
                logger.debug("===== Get filtered categories : Mixins filter is found and channeled =====")
                filtered_mixins,resp_code_m = self.manager_m.get_filtered_mixins(jreq['mixins'],res['mixins'])
            else:
                logger.debug("Get filtered categories : No mixin filter was found" )
                filtered_mixins = ""
                resp_code_m = return_code['OK']

            if jreq.has_key('actions'):
                logger.debug("===== Get filtered categories : Actions filter is found and channeled =====")
                filtered_actions,resp_code_a = self.manager_a.get_filtered_actions(jreq['actions'],res['actions'])
            else:
                logger.debug("ch get filter : No actions found")
                filtered_actions = ""
                resp_code_a = return_code['OK']

            #Step[3]: send them back to the dispatcher

            if resp_code_a is not return_code['OK'] or resp_code_k is not return_code['OK'] or resp_code_m is not return_code['OK']:
                return "An error has occurred, please check logs for more details",return_code['Bad Request']
            else:
                result = {'kinds': filtered_kinds, 'mixins': filtered_mixins, 'actions': filtered_actions}
                return result,return_code['OK']

    def channel_delete_categories(self,jreq):
        """
        Channel the delete request to the right methods
        Args:
            @param user_id: ID of the issuer of the post request
            @param jreq: Body content of the post request

        """
        #Step[1]: Get the data from the database to avoid replicates:

        db_occi_id = self.d_baker.bake_to_delete_categories()

        if db_occi_id is None:

            return "An error has occurred, please check log for more details",return_code['Bad Request']

        else:
            if jreq.has_key('kinds'):
                logger.debug("===== Delete categories : Kind filter is found and channeled =====")
                delete_kinds,resp_code_k = self.manager_k.delete_kind_documents(jreq['kinds'],db_occi_id)
            else:
                logger.debug("===== Delete categories : No Kind filter was found =====")
                delete_kinds=list()
                resp_code_k = return_code['OK']

            if jreq.has_key('mixins'):

                db_mixin_entities = self.d_baker.bake_to_delete_categories_mixins(jreq['mixins'])
                logger.debug("===== Delete categories : Mixin filter is found and channeled =====")
                delete_mixins,to_update,resp_code_m = self.manager_m.delete_mixin_documents(jreq['mixins'],db_occi_id,db_mixin_entities)
            else:
                logger.debug("===== Delete categories : No Mixin filter was found =====")
                delete_mixins=list()
                to_update = list()
                resp_code_m = return_code['OK']

            if jreq.has_key('actions'):
                logger.debug("===== Delete categories : Action filter is found and channeled =====")
                delete_actions,resp_code_a = self.manager_a.delete_action_documents(jreq['actions'],db_occi_id)
            else:
                logger.debug("===== Delete categories : Action filter is found and channeled =====")
                delete_actions = list()
                resp_code_a = return_code['OK']

            if resp_code_a is not return_code['OK'] or resp_code_k is not return_code['OK'] or resp_code_m is not return_code['OK']:
                return "An error has occurred, please check log for more details",return_code['Bad Request']

            categories = delete_kinds + delete_mixins + delete_actions

            self.PostMan.save_deleted_categories_in_db(categories)


            return "",return_code['OK']


    def channel_update_categories(self,j_newData):
        """
        Channel the PUT requests to their right methods
        Args:
            @param j_newData: Body content of the post request
        """
        #Step[1]: Get the data from the database to avoid replicates:

        db_occi_id_doc = self.d_baker.bake_to_update_categories()

        if db_occi_id_doc is None:
            return "An error has occurred, please check log for more details",return_code['Bad Request']
        else:

            if j_newData.has_key('actions'):
                logger.debug("===== Update categories : Action filter is found and channeled =====")
                updated_actions,resp_code_a = self.manager_a.update_OCCI_action_descriptions(j_newData['actions'],db_occi_id_doc)
            else:
                logger.debug("===== Update categories : No Action filter was found =====")
                updated_actions=list()
                resp_code_a = return_code['OK']

            if j_newData.has_key('kinds'):
                logger.debug("===== Update categories : Kind filter is found and channeled =====")
                updated_kinds,resp_code_k = self.manager_k.update_OCCI_kind_descriptions(j_newData['kinds'],db_occi_id_doc)
            else:
                logger.debug("===== Update categories : No Kind filter was found =====")
                updated_kinds = list()
                resp_code_k = return_code['OK']

            if j_newData.has_key('providers'):
                logger.debug("===== Update categories : Provider filter is found and channeled =====")
                updated_providers,resp_code_p = self.manager_k.update_kind_providers(j_newData['providers'],db_occi_id_doc)
            else:
                logger.debug("===== Update categories : No Provider filter was found =====")
                updated_providers=list()
                resp_code_p = return_code['OK']

            if j_newData.has_key('mixins'):

                logger.debug("===== Update categories : Mixin filter is found and channeled =====")
                updated_mixins,resp_code_m = self.manager_m.update_OCCI_mixin_descriptions(j_newData['mixins'],db_occi_id_doc)
            else:
                logger.debug("===== Update categories : No Mixin filter was found =====")
                updated_mixins = list()
                resp_code_m = return_code['OK']


            if resp_code_a is not return_code['OK'] or resp_code_k is not return_code['OK'] or resp_code_m is not return_code['OK'] or resp_code_p is not return_code['OK']:
                return "An error has occurred, please check log for more details",return_code['Bad Request']

            categories = updated_kinds + updated_providers + updated_mixins + updated_actions
            self.PostMan.save_updated_docs_in_db(categories)

            return "",return_code['OK']





#=======================================================================================================================
#                           Independant Functions
#=======================================================================================================================
#def create_temporary_db(data_1,data_2,new_data):
#    """
#    Add new_data to data
#    Args:
#        @param data_1: old data
#        @param data_2: old data
#        @param new_data: new data
#    """
#    for item in new_data:
#        if item.has_key('OCCI_ID'):
#            data_1.append(item['OCCI_ID'])
#        elif item.has_key('OCCI_Location'):
#            data_2.append(item['OCCI_Location'])
#    return data_1,data_2

