#=======================================================================================================================
#                                           ResourceManager
#=======================================================================================================================

class ResourceManager(object):
    """
    Manager of resource and link documents in the couch database.
    """

    def register_resources(self,creator,occi_descriptions,url_path,db_occi_ids_locs):

        """
        Add new resources to the database
        Args:
            @param creator: the user who created these new resources
            @param occi_descriptions: the OCCI description of the new resources
            @param db_occi_ids_locs: OCCI IDs and OCCI Location extracted from the database
            @param url_path: URL path of the request
        """
        loc_res = list()
        kind_occi_id = None
        for elem in db_occi_ids_locs:
            if elem['OCCI_Location'] == url_path:
                kind_occi_id = elem['OCCI_ID']
                break
        if kind_occi_id is not None:
            for desc in occi_descriptions:

                #Verify if the kind to which this request is sent is the same as the one in the link description
                if desc['kind'] == kind_occi_id:
                    if desc.has_key('actions'):
                        ok_a = joker.verify_existences_delta(desc['actions'],db_occi_ids_locs)
                    else:
                        ok_a = True
                    if ok_a is True:
                        if desc.has_key('mixins'):
                            ok_m = joker.verify_existences_beta(desc['mixins'],db_occi_ids_locs)
                        else:
                            ok_m = True
                        if ok_m is True:
                            if desc.has_key('links'):
                                ok_l,exist_links = self.verify_links_implicit(desc['links'],creator,db_occi_ids_locs)
                            else:
                                ok_l = True
                                exist_links = False
                            if ok_l is True:
                                loc = joker.make_entity_location_from_url(creator,url_path,desc['id'])
                                exist_same = joker.verify_existences_teta([loc],db_occi_ids_locs)
                                if exist_same is False:
                                    jData = dict()
                                    jData['_id'] = uuid_Generator.get_UUID()
                                    jData['Creator'] = creator
                                    jData['CreationDate'] = str(datetime.now())
                                    jData['LastUpdate'] = ""
                                    jData['OCCI_Location']= loc
                                    jData['OCCI_Description']= desc
                                    jData['Type']= "Resource"
                                    jData['Internal_Links'] = exist_links
                                    loc_res.append(jData)
                                else:
                                    logger.error("Reg resource exp : Bad Resource id ")
                                    return list(),return_code['Conflict']
                            else:
                                logger.error("Reg resources exp : Bad links description ")
                                return list(),exist_links
                        else:
                            logger.error("Reg resources exp : Bad Mixins description ")
                            return list(),return_code['Not Found']
                    else:
                        logger.error("Reg resources exp : Bad Actions description ")
                        return list(),return_code['Not Found']
                else:
                    mesg = "Kind description and kind location don't match"
                    logger.error("Reg resources exp: " + mesg)
                    return list(),return_code['Conflict']
            logger.debug("Reg resouces exp: Resources sent for creation")
            return loc_res,return_code['OK, and location returned']
        else:
            mesg = "No kind corresponding to this location was found"
            logger.error("Reg resources exp: " + mesg)
            return list(),return_code['Not Found']


    def verify_links_implicit(self,occi_descriptions,creator,db_occi_ids_locs):
        """
        Checks the integrity of internal resource links (Called only during the creation of a new resource instance)
        Args:

            @param occi_descriptions: the OCCI descriptions of new links
            @param creator: Issuer of the request
            @param db_occi_ids_locs: OCCI IDs and locations contained in the database
        """
        impl_link_locs = list()
        for desc in occi_descriptions:
            ok_k = joker.verify_existences_beta([desc['kind']],db_occi_ids_locs)
            #Verify if the kind to which this request is sent is the same as the one in the link description
            if ok_k is True:
                ok_target = joker.verify_existences_teta([desc['target']],db_occi_ids_locs)
                if ok_target is True:
                    if desc.has_key('actions'):
                        ok_a = joker.verify_existences_delta(desc['actions'],db_occi_ids_locs)
                    else:
                        ok_a = True
                    if ok_a is True:
                        if desc.has_key('mixins'):
                            ok_m = joker.verify_existences_beta(desc['mixins'],db_occi_ids_locs)
                        else:
                            ok_m = True
                        if ok_m is True:
                            loc = joker.make_implicit_link_location(desc['id'],desc['kind'],creator,db_occi_ids_locs)
                            exist_same = joker.verify_existences_teta([loc],db_occi_ids_locs)
                            if exist_same is True:
                                logger.error("Reg links impl : Bad link id ")
                                return False,return_code['Conflict']
                            else:
                                impl_link_locs.append(loc)
                        else:
                            logger.error("Reg links impl : Bad Mixins description ")
                            return False,return_code['Not Found']
                    else:
                        logger.error("Reg links impl : Bad Actions description ")
                        return False,return_code['Not Found']
                else:
                    logger.error("Reg links impl : Bad target description ")
                    return False,return_code['Not Found']
            else:
                mesg = "Kind description does not exist"
                logger.error("Reg links impl: " + mesg)
                return False,return_code['Not Found']
        logger.debug("Internal links validated with success")
        return True,impl_link_locs

    def get_filtered_resources(self, filters, descriptions_res):
        """
        Retrieve the resources  that match the filters provided
        Args:
            @param filters: Filters
            @param descriptions_res: Resource descriptions
        """
        var = list()
        try:
            for desc in descriptions_res:
                for filter in filters:
                    checks =joker.filter_occi_description(desc['OCCI_Description'],filter)
                    if checks is True:
                        var.append(desc['OCCI_ID'])
                        logger.debug("Entity filtered : document found")
                        break
            return var,return_code['OK']
        except Exception as e:
            logger.error("filtered res : " + e.message)
            return list(),return_code['Internal Server Error']

    def register_custom_resource(self, user_id, occi_description, path_url, db_occi_ids_locs):
        """
        Add a new resource with a custom URL to the database
        Args:
            @param user_id: Issuer of the request
            @param occi_description: Resource description
            @param path_url: Custom URL of the resource
            @param db_occi_ids_locs: Ids and locations from the database
        """
        ok_k = joker.verify_existences_beta([occi_description['kind']],db_occi_ids_locs)
        #Verify if the kind to which this request is sent is the same as the one in the link description
        if ok_k is True:
            if occi_description.has_key('actions'):
                ok_a = joker.verify_existences_delta(occi_description['actions'],db_occi_ids_locs)
            else:
                ok_a = True
            if ok_a is True:
                if occi_description.has_key('mixins'):
                    ok_m = joker.verify_existences_beta(occi_description['mixins'],db_occi_ids_locs)
                else:
                    ok_m = True
                if ok_m is True:
                    if occi_description.has_key('links'):
                        ok_l,exist_links = self.verify_links_implicit(occi_description['links'],user_id,db_occi_ids_locs)
                    else:
                        ok_l = True
                        exist_links = False
                    if ok_l is True:
                        jData = dict()
                        jData['_id'] = uuid_Generator.get_UUID()
                        jData['Creator'] = user_id
                        jData['CreationDate'] = str(datetime.now())
                        jData['LastUpdate'] = ""
                        jData['OCCI_Location']= path_url
                        jData['OCCI_Description']= occi_description
                        jData['Type']= "Resource"
                        jData['Internal_Links'] = exist_links
                    else:
                        logger.error("Reg resource cust : Bad links description ")
                        return list(),exist_links
                else:
                    logger.error("Reg resource cust : Bad Mixins description ")
                    return list(),return_code['Not Found']
            else:
                logger.error("Reg resource cust : Bad Actions description ")
                return list(),return_code['Not Found']
        else:
            mesg = "Kind description does not exist match"
            logger.error("Reg resource cust: " + mesg)
            return list(),return_code['Not Found']

        logger.debug("Reg resource cust: Resources sent for creation")
        return jData,return_code['OK, and location returned']


    def update_resource(self, user_id, old_description,occi_description, db_occi_ids_locs):
        """
        Verifies the validity of a resource's new data
        Args:
            @param user_id: Issuer of the request
            @param old_description: Old resource description
            @param occi_description: Resource description
            @param db_occi_ids_locs: Ids and locations from the database
        """
        ok_k = joker.verify_existences_beta([occi_description['kind']],db_occi_ids_locs)
        #Verify if the kind to which this request is sent is the same as the one in the link description
        if ok_k is True:
            if occi_description.has_key('actions'):
                ok_a = joker.verify_existences_delta(occi_description['actions'],db_occi_ids_locs)
            else:
                ok_a = True
            if ok_a is True:
                if occi_description.has_key('mixins'):
                    ok_m = joker.verify_existences_beta(occi_description['mixins'],db_occi_ids_locs)
                else:
                    ok_m = True
                if ok_m is True:
                    if occi_description.has_key('links'):
                        logger.error("Internal links are not forbidden to update")
                        return list(),return_code['Bad Request']
                    else:
                        problems,occi_description = joker.update_occi_entity_description(old_description,occi_description)
                        if problems is False:
                            logger.debug("Up resource: Resource sent for update")
                            return occi_description,return_code['OK, and location returned']
                        else:
                            logger.error("Up resource : Resource update failed")
                            return list(),return_code['Bad Request']
                else:
                    logger.error("Up resource: Bad Mixins description ")
                    return list(),return_code['Not Found']
            else:
                logger.error("Up resource: Bad Actions description ")
                return list(),return_code['Not Found']
        else:
            mesg = "Kind description does not exist match"
            logger.error("Up resource: " + mesg)
            return list(),return_code['Not Found']

    def partial_resource_update(self, user_id,old_data,occi_description, db_occi_ids_locs):
        """
        Verifies the validity of a resource's new data
        Args:
            @param user_id: Issuer of the request
            @param occi_description: Resource description
            @param old_data: Old resource description
            @param db_occi_ids_locs: Ids and locations from the database
        """

        if occi_description.has_key('actions'):
            ok_a = joker.verify_existences_delta(occi_description['actions'],db_occi_ids_locs)
        else:
            ok_a = True
        if ok_a is True:
            if occi_description.has_key('mixins'):
                ok_m = joker.verify_existences_beta(occi_description['mixins'],db_occi_ids_locs)
            else:
                ok_m = True
            if ok_m is True:
                if occi_description.has_key('links'):
                    ok_l,exist_links = self.verify_links_implicit(occi_description['links'],user_id,db_occi_ids_locs)
                else:
                    ok_l = True
                    exist_links = False
                if ok_l is True:
                    problems,updated_data = joker.update_occi_entity_description(old_data,occi_description)
                    if problems is False:
                        logger.debug("Up partial resource: Resource sent for update")
                        return updated_data,exist_links,return_code['OK, and location returned']
                    else:
                        logger.error("Up partial resource: Resource couldn't have been fully updated")
                        return updated_data,False,return_code['Conflict']
                else:
                    logger.error("Up partial resource: Bad links description ")
                    return list(),False,exist_links
            else:
                logger.error("Up partial resource: Bad Mixins description ")
                return list(),False,return_code['Not Found']
        else:
            logger.error("Up partial resource: Bad Actions description ")
            return list(),False,return_code['Not Found']
