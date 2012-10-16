
import pyocni.pyocni_tools.config as config
import pyocni.pyocni_tools.occi_Joker as joker


import pyocni.pyocni_tools.uuid_Generator as uuid_Generator
try:
    import simplejson as json
except ImportError:
    import json


from pyocni.pyocni_tools.config import return_code

# getting the Logger
logger = config.logger

class ResourceManager(object):
    """
    Manager of resource documents in the couch database.
    """

    def register_resources(self,occi_descriptions,url_path,db_occi_ids_locs):

        """
        Add new resources to the database
        Args:

            @param occi_descriptions: the OCCI description of the new resources
            @param db_occi_ids_locs: OCCI IDs and OCCI Location extracted from the database
            @param url_path: URL path of the request
        """
        loc_res = list()
        kind_occi_id = None
        #Get the kind on which the request was sent
        for elem in db_occi_ids_locs:
            if elem['OCCI_Location'] == url_path:
                kind_occi_id = elem['OCCI_ID']
                break

        if kind_occi_id is not None:

            for desc in occi_descriptions:

                #Verify if the kind to which this request is sent is the same as the one in the link description
                if desc['kind'] == kind_occi_id:

                    loc = joker.make_entity_location_from_url(url_path,desc['id'])
                    exist_same = joker.verify_existences_teta([loc],db_occi_ids_locs)

                    if exist_same is False:
                        jData = dict()
                        jData['_id'] = uuid_Generator.get_UUID()
                        jData['OCCI_Location']= loc
                        jData['OCCI_Description']= desc
                        jData['Type']= "Resource"
                        loc_res.append(jData)
                    else:
                        logger.error(" ===== Register_resources : Bad Resource id ===== ")
                        return list(),return_code['Conflict']

                else:
                    mesg = "Kind description and kind location don't match"
                    logger.error("===== Register_resources: " + mesg + " ===== ")
                    return list(),return_code['Conflict']

            logger.debug("===== Register_resources: Resources sent for creation =====")
            return loc_res,return_code['OK, and location returned']
        else:
            mesg = "No kind corresponding to this location was found"
            logger.error("===== Register_resources: " + mesg+ " =====")
            return list(),return_code['Not Found']


#

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
                        logger.debug("===== Get_filtered_resources: A resource document is found =====")
                        break

            return var,return_code['OK']

        except Exception as e:
            logger.error("Get_filtered_resources : " + e.message+ " =====")
            return list(),return_code['Internal Server Error']

    def register_custom_resource(self, occi_description, path_url, db_occi_ids_locs):
        """
        Add a new resource with a custom URL to the database
        Args:

            @param occi_description: Resource description
            @param path_url: Custom URL of the resource
            @param db_occi_ids_locs: Ids and locations from the database
        """

        #Verify if the kind of the new resource exists
        ok_k = joker.verify_existences_beta([occi_description['kind']],db_occi_ids_locs)

        if ok_k is True:

            jData = dict()
            jData['_id'] = uuid_Generator.get_UUID()
            jData['OCCI_Location']= path_url
            jData['OCCI_Description']= occi_description
            jData['Type']= "Resource"

        else:
            mesg = "This kind does not exist"
            logger.error(" ===== Register_custom_resource : " + mesg + " =====")
            return list(),return_code['Not Found']

        logger.debug("===== Register_custom_resource :  Resources sent for creation")
        return jData,return_code['OK, and location returned']

    def update_resource(self, old_description,occi_description, db_occi_ids_locs):
        """
        Verifies the validity of a resource's new data
        Args:

            @param old_description: Old resource description
            @param occi_description: Resource description
            @param db_occi_ids_locs: Ids and locations from the database
        """
        #Verify if the kind of the resource exists in the database
        ok_k = joker.verify_existences_beta([occi_description['kind']],db_occi_ids_locs)

        if ok_k is True:

            problems,occi_description = joker.update_occi_entity_description(old_description,occi_description)

            if problems is False:
                logger.debug("===== Update_resource: Resource sent for update =====")
                return occi_description,return_code['OK, and location returned']

        else:
            mesg = "Kind description does not exist match"
            logger.error("===== Update_resource: " + mesg+" =====")
            return list(),return_code['Not Found']

    def partial_resource_update(self, old_data,occi_description, db_occi_ids_locs):
        """
        Verifies the validity of a resource's new data
        Args:

            @param occi_description: Resource description
            @param old_data: Old resource description
            @param db_occi_ids_locs: Ids and locations from the database
        """

        problems,updated_data = joker.update_occi_entity_description(old_data,occi_description)

        if problems is False:
            logger.debug("===== Update_partial_resource: Resource sent for update =====")
            return updated_data,return_code['OK, and location returned']
        else:
            logger.error("===== Update_partial_resource: Resource couldn't have been fully updated =====")
            return updated_data,False,return_code['Conflict']



#=======================================================================================================================
#                                                             Functions to review
#=======================================================================================================================

#def verify_links_implicit(self,occi_descriptions,creator,db_occi_ids_locs):
#        """
#        Checks the integrity of internal resource links (Called only during the creation of a new resource instance)
#        Args:
#
#            @param occi_descriptions: the OCCI descriptions of new links
#            @param creator: Issuer of the request
#            @param db_occi_ids_locs: OCCI IDs and locations contained in the database
#        """
#        impl_link_locs = list()
#        for desc in occi_descriptions:
#            ok_k = joker.verify_existences_beta([desc['kind']],db_occi_ids_locs)
#            #Verify if the kind to which this request is sent is the same as the one in the link description
#            if ok_k is True:
#                ok_target = joker.verify_existences_teta([desc['target']],db_occi_ids_locs)
#                if ok_target is True:
#                    if desc.has_key('actions'):
#                        ok_a = joker.verify_existences_delta(desc['actions'],db_occi_ids_locs)
#                    else:
#                        ok_a = True
#                    if ok_a is True:
#                        if desc.has_key('mixins'):
#                            ok_m = joker.verify_existences_beta(desc['mixins'],db_occi_ids_locs)
#                        else:
#                            ok_m = True
#                        if ok_m is True:
#                            loc = joker.make_implicit_link_location(desc['id'],desc['kind'],creator,db_occi_ids_locs)
#                            exist_same = joker.verify_existences_teta([loc],db_occi_ids_locs)
#                            if exist_same is True:
#                                logger.error("Reg links impl : Bad link id ")
#                                return False,return_code['Conflict']
#                            else:
#                                impl_link_locs.append(loc)
#                        else:
#                            logger.error("Reg links impl : Bad Mixins description ")
#                            return False,return_code['Not Found']
#                    else:
#                        logger.error("Reg links impl : Bad Actions description ")
#                        return False,return_code['Not Found']
#                else:
#                    logger.error("Reg links impl : Bad target description ")
#                    return False,return_code['Not Found']
#            else:
#                mesg = "Kind description does not exist"
#                logger.error("Reg links impl: " + mesg)
#                return False,return_code['Not Found']
#        logger.debug("Internal links validated with success")
#        return True,impl_link_locs