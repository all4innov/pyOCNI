class ActionManager:
    """

        Manager for Action documents on couch database

    """

    def get_filtered_actions(self,jfilters,db_actions):
        """
        Returns action documents matching the filter provided
        Args:
            @param jfilters: description of the action document to retrieve
            @param db_actions: action descriptions that already exist in database
            @return : <list> OCCI action description contained inside of the action document
        """
        var = list()
        #Extract action descriptions from the dictionary
        try:
            for elem in db_actions:
                for jfilter in jfilters:
                    ok = joker.filter_occi_description(elem,jfilter)
                    if ok is True:
                        var.append(elem)
                        logger.debug("action filtered document found")
                        break
            return var,return_code['OK']
        except Exception as e:
            logger.error("filtered actions : " + e.message)
            return "An error has occurred",return_code['Internal Server Error']

    def register_actions(self,creator,descriptions,db_actions):

        """
        Add new actions to the database
        Args:
            @param creator: the id of the issuer of the creation request
            @param descriptions: OCCI action descriptions
            @param db_actions: Existing actions in database
        """
        loc_res = list()
        resp_code = return_code['OK']
        for desc in descriptions:
            occi_id = joker.get_description_id(desc)
            ok_k = joker.verify_occi_uniqueness(occi_id,db_actions)
            if ok_k is True:
                jData = dict()
                jData['_id'] = uuid_Generator.get_UUID()
                jData['Creator'] = creator
                jData['CreationDate'] = str(datetime.now())
                jData['LastUpdate'] = ""
                jData['OCCI_Description']= desc
                jData['OCCI_ID'] = occi_id
                jData['Type']= "Action"
                loc_res.append(jData)
            else:
                message = "This Action description already exists in document. "
                logger.error("Register Action : " + message)
                resp_code = return_code['Conflict']
                return list(),resp_code
        return loc_res,resp_code



    def update_OCCI_action_descriptions(self,user_id,new_data,db_data):
        """
        Updates the OCCI description field of the action which document OCCI_ID is equal to OCCI_ID contained in data
        (Can only be done by the creator of the action document)
        Args:
            @param user_id: ID of the creator of the action document
            @param new_data: Data containing the OCCI ID of the action and the new OCCI action description
            @param db_data: Data already contained in the database
            @return : <string>, return_code
        """
        to_update = list()
        resp_code = return_code['OK']
        for desc in new_data:
            occi_id = joker.get_description_id(desc)
            old_doc = joker.extract_doc(occi_id,db_data)
            if old_doc is not None:
                if user_id == old_doc['Creator']:
                    problems,occi_description= joker.update_occi_category_description(old_doc['OCCI_Description'],desc)
                    if problems is True:
                        message = "Action OCCI description " + occi_id + " has not been totally updated."
                        logger.error("Action OCCI description update " + message)
                        return list(),return_code['Bad Request']
                    else:
                        message = "Action OCCI description " + occi_id + " has been updated successfully"
                        old_doc['OCCI_Description'] = occi_description
                        old_doc['LastUpdate'] = str(datetime.now())
                        to_update.append(old_doc)
                        logger.debug("Update Action OCCI description : " + message)
                else:
                    message = "You have no right to update this Action document " + occi_id
                    logger.error("Update Action OCCI des : " + message)
                    return list(),return_code['Forbidden']
            else:
                message = "Action document " + occi_id + " couldn\'t be found "
                logger.error("Update Action OCCI des : " + message)
                return list(),return_code['Not Found']
        return to_update,resp_code

    def delete_action_documents(self,descriptions,user_id,db_categories):
        """
        Delete action documents that is related to the scheme + term contained in the description provided
        Args:
            @param descriptions: OCCI description of the action document to delete
            @param user_id: id of the issuer of the delete request
            @param db_categories: Category data already contained in the database
        """

        message = list()
        res_code = return_code['OK']
        #Verify the existence of such action document
        for desc in descriptions:
            occi_id = joker.get_description_id(desc)
            action_id_rev = joker.verify_exist_occi_id_creator(occi_id,user_id,db_categories)
            if action_id_rev is not None:
                message.append(action_id_rev)
                event = "Action document " + occi_id + " is sent for delete "
                logger.debug("Delete action : " + event)
            else:
                event = "Could not find this action document " + occi_id +" or you are not authorized for for delete"
                logger.error("Delete action : " + event)
                return list(), return_code['Bad Request']
        return message,res_code


