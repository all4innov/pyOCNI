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
Created on Jun 12, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@license: Apache License, Version 2.0
"""

#
##=======================================================================================================================
##                                           LinkManager
##=======================================================================================================================
#
class LinkManager(object):
    """
    Manager of link documents in the couch database.
    """
    pass
#    def register_links_explicit(self,creator,occi_descriptions,url_path,db_occi_ids_locs):
#        """
#        Add new links to database
#        Args:
#            @param creator: Issuer of the register request
#            @param occi_descriptions: Link OCCI descriptions
#            @param db_occi_ids_locs: OCCI ID and locations extracted from the database
#            @param url_path: URL path of the request
#        """
#
#        loc_res = list()
#        kind_occi_id = None
#        for elem in db_occi_ids_locs:
#            if elem['OCCI_Location'] == url_path:
#                kind_occi_id = elem['OCCI_ID']
#                break
#        if kind_occi_id is not None:
#            for desc in occi_descriptions:
#
#                #Verify if the kind to which this request is sent is the same as the one in the link description
#                if desc['kind'] == kind_occi_id:
#
#                    ok_target_source = joker.verify_existences_teta([desc['target'],desc['source']],db_occi_ids_locs)
#                    if ok_target_source is True:
#                        ok_kappa = joker.verify_existences_kappa([desc['target'],desc['source']],db_occi_ids_locs)
#                        if ok_kappa is True:
#                            if desc.has_key('actions'):
#                                ok_a = joker.verify_existences_delta(desc['actions'],db_occi_ids_locs)
#                            else:
#                                ok_a = True
#                            if ok_a is True:
#                                if desc.has_key('mixins'):
#                                    ok_m = joker.verify_existences_beta(desc['mixins'],db_occi_ids_locs)
#                                else:
#                                    ok_m = True
#                                if ok_m is True:
#                                    loc = joker.make_entity_location_from_url(creator,url_path,desc['id'])
#                                    exist_same = joker.verify_existences_teta([loc],db_occi_ids_locs)
#                                    if exist_same is False:
#                                        jData = dict()
#                                        jData['_id'] = uuid_Generator.get_UUID()
#                                        jData['Creator'] = creator
#                                        jData['CreationDate'] = str(datetime.now())
#                                        jData['LastUpdate'] = ""
#                                        jData['OCCI_Location']= loc
#                                        jData['OCCI_Description']= desc
#                                        jData['Type']= "Link"
#                                        loc_res.append(jData)
#                                    else:
#                                        logger.error("Reg links exp : Bad Link id ")
#                                        return list(),return_code['Conflict']
#                                else:
#                                    logger.error("Reg links exp : Bad Mixins description ")
#                                    return list(),return_code['Not Found']
#                            else:
#                                logger.error("Reg links exp : Bad Actions description ")
#                                return list(),return_code['Not Found']
#                        else:
#                            logger.error("Reg links exp : Bad resources description ")
#                            return list(),return_code['Bad Request']
#                    else:
#                        logger.error("Reg links exp : Bad resources description ")
#                        return list(),return_code['Not Found']
#                else:
#                    mesg = "Kind description and kind location don't match"
#                    logger.error("Reg links exp: " + mesg)
#                    return list(),return_code['Conflict']
#            logger.debug("Reg links exp: links sent for creation")
#            return loc_res,return_code['OK, and location returned']
#        else:
#            mesg = "No kind corresponding to this location was found"
#            logger.error("Reg links exp: " + mesg)
#            return list(),return_code['Not Found']
#
#    def get_filtered_links(self, filters, descriptions_link):
#        """
#        Retrieve the resources  that match the filters provided
#        Args:
#            @param filters: Filters
#            @param descriptions_link: Link descriptions
#        """
#        var = list()
#        try:
#            for desc in descriptions_link:
#                for filter in filters:
#                    checks =joker.filter_occi_description(desc['OCCI_Description'],filter)
#                    if checks is True:
#                        var.append(desc['OCCI_ID'])
#                        logger.debug("Entity filtered : document found")
#                        break
#            return var,return_code['OK']
#        except Exception as e:
#            logger.error("filtered link : " + e.message)
#            return list(),return_code['Internal Server Error']
#
#    def register_custom_link(self, user_id, occi_description, path_url, db_occi_ids_locs):
#        """
#        Add a new link with a custom URL to the database
#        Args:
#            @param user_id: Issuer of the request
#            @param occi_description: link description
#            @param path_url: Custom URL of the link
#            @param db_occi_ids_locs: Ids and locations from the database
#        """
#        ok_k = joker.verify_existences_beta([occi_description['kind']],db_occi_ids_locs)
#
#        #Verify if the kind to which this request is sent is the same as the one in the link description
#        if ok_k is True:
#            ok_target_source = joker.verify_existences_teta([occi_description['target'],occi_description['source']],db_occi_ids_locs)
#            if ok_target_source is True:
#                ok_kappa = joker.verify_existences_kappa([occi_description['target'],occi_description['source']],db_occi_ids_locs)
#                if ok_kappa is True:
#                    if occi_description.has_key('actions'):
#                        ok_a = joker.verify_existences_delta(occi_description['actions'],db_occi_ids_locs)
#                    else:
#                        ok_a = True
#                    if ok_a is True:
#                        if occi_description.has_key('mixins'):
#                            ok_m = joker.verify_existences_beta(occi_description['mixins'],db_occi_ids_locs)
#                        else:
#                            ok_m = True
#                        if ok_m is True:
#                            jData = dict()
#                            jData['_id'] = uuid_Generator.get_UUID()
#                            jData['Creator'] = user_id
#                            jData['CreationDate'] = str(datetime.now())
#                            jData['LastUpdate'] = ""
#                            jData['OCCI_Location']= path_url
#                            jData['OCCI_Description']= occi_description
#                            jData['Type']= "Link"
#
#                        else:
#                            logger.error("Reg link cus : Bad Mixins description ")
#                            return list(),return_code['Not Found']
#                    else:
#                        logger.error("Reg link cus : Bad Actions description ")
#                        return list(),return_code['Not Found']
#                else:
#                    logger.error("Reg link cus : Bad resources description ")
#                    return list(),return_code['Bad Request']
#            else:
#                logger.error("Reg link cus : Bad resources description ")
#                return list(),return_code['Not Found']
#        else:
#            mesg = "Kind description does not exist"
#            logger.error("Reg link cus: " + mesg)
#            return list(),return_code['Not Found']
#
#        logger.debug("Reg link cus: Link sent for creation")
#        return jData,return_code['OK, and location returned']
#
#    def update_link(self, user_id, occi_description, db_occi_ids_locs):
#        """
#        Update the link description attached to the custom URL
#        Args:
#            @param user_id: Issuer of the request
#            @param occi_description: link description
#            @param db_occi_ids_locs: Ids and locations from the database
#        """
#        ok_k = joker.verify_existences_beta([occi_description['kind']],db_occi_ids_locs)
#
#        #Verify if the kind to which this request is sent is the same as the one in the link description
#        if ok_k is True:
#            ok_target_source = joker.verify_existences_teta([occi_description['target'],occi_description['source']],db_occi_ids_locs)
#            if ok_target_source is True:
#                ok_kappa = joker.verify_existences_kappa([occi_description['target'],occi_description['source']],db_occi_ids_locs)
#                if ok_kappa is True:
#                    if occi_description.has_key('actions'):
#                        ok_a = joker.verify_existences_delta(occi_description['actions'],db_occi_ids_locs)
#                    else:
#                        ok_a = True
#                    if ok_a is True:
#                        if occi_description.has_key('mixins'):
#                            ok_m = joker.verify_existences_beta(occi_description['mixins'],db_occi_ids_locs)
#                        else:
#                            ok_m = True
#                        if ok_m is True:
#                            logger.debug("UP link cus: Link sent for update")
#                            return occi_description,return_code['OK']
#                        else:
#                            logger.error("UP link cus: Bad Mixins description ")
#                            return list(),return_code['Not Found']
#                    else:
#                        logger.error("UP link cus: Bad Actions description ")
#                        return list(),return_code['Not Found']
#                else:
#                    logger.error("UP link cus: Bad resources description ")
#                    return list(),return_code['Bad Request']
#            else:
#                logger.error("UP link cus: Bad resources description ")
#                return list(),return_code['Not Found']
#        else:
#            mesg = "Kind description does not exist"
#            logger.error("UP link cus: " + mesg)
#            return list(),return_code['Not Found']
#
#
#    def partial_link_update(self, user_id, old_data, occi_description, db_occi_ids_locs):
#        """
#        Update the link description attached to the custom URL
#        Args:
#            @param user_id: Issuer of the request
#            @param occi_description: link description
#            @param old_data: Old link description
#            @param db_occi_ids_locs: Ids and locations from the database
#        """
#        #Verify if the kind to which this request is sent is the same as the one in the link description
#        ok_target_source = joker.verify_existences_teta([occi_description['target'],occi_description['source']],db_occi_ids_locs)
#        if ok_target_source is True:
#            ok_kappa = joker.verify_existences_kappa([occi_description['target'],occi_description['source']],db_occi_ids_locs)
#            if ok_kappa is True:
#                if occi_description.has_key('actions'):
#                    ok_a = joker.verify_existences_delta(occi_description['actions'],db_occi_ids_locs)
#                else:
#                    ok_a = True
#                if ok_a is True:
#                    if occi_description.has_key('mixins'):
#                        ok_m = joker.verify_existences_beta(occi_description['mixins'],db_occi_ids_locs)
#                    else:
#                        ok_m = True
#                    if ok_m is True:
#                        problems,updated_data = joker.update_occi_entity_description(old_data,occi_description)
#                        if problems is False:
#                            logger.debug("Up part link: Link sent for update")
#                            return updated_data,return_code['OK']
#                        else:
#                            logger.error("Up part link: Link couldn't have been fully updated")
#                            return updated_data,return_code['Conflict']
#                    else:
#                        logger.error("UP partial link cus: Bad Mixins description ")
#                        return list(),return_code['Not Found']
#                else:
#                    logger.error("UP partial link cus: Bad Actions description ")
#                    return list(),return_code['Not Found']
#            else:
#                logger.error("UP partial link cus: Bad resources description ")
#                return list(),return_code['Bad Request']
#        else:
#            logger.error("UP partial link cus: Bad resources description ")
#            return list(),return_code['Not Found']


