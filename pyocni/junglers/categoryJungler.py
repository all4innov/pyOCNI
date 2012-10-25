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
                new_kinds,resp_code_k = self.manager_k.register_kinds(jreq['kinds'],db_occi_ids,db_occi_locs)

            else:
                logger.debug("===== channel_register_categories ==== : no kinds found")
                new_kinds = list()
                resp_code_k = return_code['OK']

            if jreq.has_key('mixins'):
                logger.debug("===== channel_register_categories ==== : Mixins channeled")
                new_mixins,resp_code_m = self.manager_m.register_mixins(jreq['mixins'],db_occi_ids,db_occi_locs)
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
                logger.debug("===== channel_register_categories ==== : Done with success")
                return "",return_code['OK']

    def channel_get_all_categories(self):
        """
        Retrieve all categories to show the server's capacity

        """
        #Step[1]: Call the dataBakers to get the Data

        res = self.d_baker.bake_to_get_all_categories()

        #Step[2]: Return all the results back to the dispatcher
        if res is None:
            return res,return_code['Internal Server Error']

        else:

            logger.debug("===== channel_get_all_categories ==== : Done with success")
            return res,return_code['OK']


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
                logger.debug("===== Channel_get_filtered_categories: Kinds filter is found and channeled =====")
                filtered_kinds,resp_code_k = self.manager_k.get_filtered_kinds(jreq['kinds'],res['kinds'])
            else:
                logger.debug("===== Channel_get_filtered_categories: No kind filter was found =====")
                filtered_kinds = ""
                resp_code_k = return_code['OK']

            if jreq.has_key('mixins'):
                logger.debug("===== Channel_get_filtered_categories: Mixins filter is found and channeled =====")
                filtered_mixins,resp_code_m = self.manager_m.get_filtered_mixins(jreq['mixins'],res['mixins'])
            else:
                logger.debug("Channel_get_filtered_categories: No mixin filter was found" )
                filtered_mixins = ""
                resp_code_m = return_code['OK']

            if jreq.has_key('actions'):
                logger.debug("===== Channel_get_filtered_categories: Actions filter is found and channeled =====")
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
                logger.debug("===== channel_get_filtered_categories ==== : Done with success")
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
                logger.debug("===== Channel_delete_categories : Kind filter is found and channeled =====")
                delete_kinds,resp_code_k = self.manager_k.delete_kind_documents(jreq['kinds'],db_occi_id)
            else:
                logger.debug("===== Channel_delete_categories : No Kind filter was found =====")
                delete_kinds=list()
                resp_code_k = return_code['OK']

            if jreq.has_key('mixins'):

                db_mixin_entities = self.d_baker.bake_to_delete_categories_mixins(jreq['mixins'])
                logger.debug("===== Channel_delete_categories : Mixin filter is found and channeled =====")
                delete_mixins,to_update,resp_code_m = self.manager_m.delete_mixin_documents(jreq['mixins'],db_occi_id,db_mixin_entities)
            else:
                logger.debug("===== Channel_delete_categories : No Mixin filter was found =====")
                delete_mixins=list()
                to_update = list()
                resp_code_m = return_code['OK']

            if jreq.has_key('actions'):
                logger.debug("===== Channel_delete_categories : Action filter is found and channeled =====")
                delete_actions,resp_code_a = self.manager_a.delete_action_documents(jreq['actions'],db_occi_id)
            else:
                logger.debug("===== Channel_delete_categories : Action filter is found and channeled =====")
                delete_actions = list()
                resp_code_a = return_code['OK']

            if resp_code_a is not return_code['OK'] or resp_code_k is not return_code['OK'] or resp_code_m is not return_code['OK']:
                return "An error has occurred, please check log for more details",return_code['Bad Request']

            categories = delete_kinds + delete_mixins + delete_actions

            self.PostMan.save_deleted_categories_in_db(categories,to_update)

            logger.debug("===== channel_delete_categories ==== : Done with success")

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
            logger.debug("===== channel_update_categories ==== : Done with success")

            return "",return_code['OK']







