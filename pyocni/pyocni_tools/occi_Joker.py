# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

# Copyright (C) 2012 Bilel Msekni - Institut Mines-Telecom
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
Created on Jun 12, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@version: 0.3
@license: LGPL - Lesser General Public License

"""
import pyocni.pyocni_tools.config as config

# getting the Logger
logger = config.logger

def update_occi_category_description(oldData,newData):
    """
    Update only a part of the occi category description
    Args:
        @param newData: The new OCCI category description
        @param oldData: The old OCCI category description
        @return : Updated data and a boolean (false if all fields are updated, true if there were some un-updated fields)
    """

    #Try to get the keys from occi category description dictionary
    oldData_keys = oldData.keys()
    newData_keys = newData.keys()
    forbidden_keys = ["term","scheme","location"]
    for key in newData_keys:
        try:
            forbidden_keys.index(key)
            if oldData[key] != newData[key]:
                logger.debug("update description : " + key + " is forbidden to change")
                return True,None
        except ValueError:
            try:
                oldData_keys.index(key)
                oldData[key] = newData[key]
            except ValueError:
                #Keep the record of the keys(=parts) that couldn't be updated
                logger.debug("update category description : " + key + " could not be found")
                return True,None

    return False,oldData

def update_occi_entity_description(oldData,newData):
    """
    Update only a part of the occi entity description
    Args:
        @param newData: The new OCCI entity description
        @param oldData: The old OCCI entity description
        @return : Updated data and a boolean (false if all fields are updated, true if there were some un-updated fields)
    """

    #Try to get the keys from occi entity description dictionary
    oldData_keys = oldData.keys()
    newData_keys = newData.keys()
    forbidden_keys = ["id","kind"]
    for key in newData_keys:
        try:
            forbidden_keys.index(key)
            if oldData[key] != newData[key]:
                logger.debug("update description : " + key + " is forbidden to change")
                return True,None
        except ValueError:
            try:
                oldData_keys.index(key)
                if key == 'attributes':
                    print "GOGOATTributes"
                else:
                    oldData[key] = newData[key]
            except ValueError:
                #Keep the record of the keys(=parts) that couldn't be updated
                logger.debug("update entity description : " + key + " could not be found")
                return True,None

    return False,oldData

def get_description_id(occi_description):
    """
    Retrieve the ID (proof of uniqueness) from the occi description
    Args:
        @param occi_description: OCCI description
        @return : ID of the OCCI description
    """
    try:
        #retrieve the term and scheme from the occi description
       desc_term = occi_description['term']
       desc_scheme = occi_description['scheme']
    except Exception as e:
        logger.error("description ID: " + e.message)
        return  None
    #Concatenate the term and scheme to get the ID of the description
    res = desc_scheme+desc_term
    return res

def filter_occi_description(description,filter):
    """
    Checks if the occi description meets the filter values
    Args:
        @param description: The OCCI description
        @param filter: The filter description
        @return : Updated  a boolean (false if no match, true if there is a match)
    """

    #Try to get the keys from filter dictionary
    filter_keys = filter.keys()
    desc_keys = description.keys()
    for key in filter_keys:
        try:
            desc_keys.index(key)
            if description[key]!= filter[key]:
                return False
        except ValueError:
            #Keep the record of the keys(=parts) that couldn't be updated
            logger.debug("filter description : "+ key + " could not be found")
            return False

    return True

def verify_existences_alpha(description,db_data):
    """
    Verify the existence of items in db_data
    Args:
        @param description: OCCI IDs to test the existence of the related urls
        @param db_data: Data already stored in database
    """
    if description.has_key('related'):
        items = description['related']
        if description.has_key('actions'):
            items += description['actions']
    elif description.has_key('actions'):
        items = description['actions']
    else:
        return True


    if not items:
        return True
    try:
        for item in items:
            db_data.index(item)
    except ValueError as e:
        logger.error(" exist alpha : " + e.message)
        return False

    return True


def verify_existences_beta(occi_ids, db_occi_ids_locs):
    """
    Verifies the existence of occi_ids in db_occi_ids_locs
    Args
        @param occi_ids: OCCI IDs to verify its existence
        @param db_occi_ids_locs: OCCI IDs and locations contained in the database
    """
    var_ids = list()
    for occi_ids_locs in db_occi_ids_locs:
        var_ids.append(occi_ids_locs['OCCI_ID'])
    try:
        for occi_id in occi_ids:
            var_ids.index(occi_id)
    except ValueError as e:
        logger.debug("exist beta : " + e.message)
        return False

    return True

def verify_existences_delta(actions, db_occi_ids_locs):
    """
    Verifies the existence of occi_ids in db_occi_ids_locs
    Args
        @param actions: OCCI IDs to verify its existence
        @param db_occi_ids_locs: OCCI IDs and locations contained in the database
    """
    var_ids = list()
    for occi_ids_locs in db_occi_ids_locs:
        var_ids.append(occi_ids_locs['OCCI_ID'])

    var_action_ids = list()
    for action in actions:
        var_action_ids.append(action['category'])
    try:
        for action_id in var_action_ids:
            var_ids.index(action_id)
    except ValueError as e:
        logger.debug("exist delta : " + e.message)
        return False

    return True

def verify_existences_teta(occi_locs, db_occi_ids_locs):
    """
    Verifies the existence of occi_locations in db_occi_ids_locs
    Args
        @param occi_locs: OCCI IDs to verify its existence
        @param db_occi_ids_locs: OCCI IDs and locations contained in the database
    """
    var_ids = list()
    for occi_ids_locs in db_occi_ids_locs:
        var_ids.append(occi_ids_locs['OCCI_Location'])
    try:
        for occi_loc in occi_locs:
            var_ids.index(occi_loc)
    except ValueError as e:
        logger.debug("exist teta : " + e.message)
        return False

    return True

def make_category_location(occi_description):
    """
    Creates the location of the kind or mixin using the occi_description
    Args:
        @param occi_description: the occi description of the kind or mixin
        @return :<string> Location of the kind or mixin
    """
    try:
        loc = occi_description['location']
        entity_location = "http://" + config.OCNI_IP + ":" + config.OCNI_PORT  + loc
    except Exception as e:
        logger.error("===== Make_category_location ======: " + e.message )
        return  None
    return entity_location


def verify_occi_uniqueness(occi_term, db_categories):
    """
    Verifies the uniqueness of the occi_term
    Args:
        @param occi_term: OCCI term to verify its uniqueness
        @param db_categories: Collection of OCCI IDs
    """
    try:
        db_categories.index(occi_term)
        return False
    except ValueError as e:
        logger.error("===== Verify_occi_uniqueness =====: " + e.message )
        return True

def verify_exist_occi_id(occi_id,db_data):
    """
    Verify the existence of a document with such an OCCI ID  and creator in db_data
    Args:
        @param occi_id: OCCI ID to be checked
        @param db_data: Data to search in
    """
    for data in db_data:
        if data['OCCI_ID'] == occi_id:
            return {"_id" : data['_id'],"_rev" : data['_rev']}
    return None


def extract_doc(occi_id, db_data):
    """
    Extracts the document corresponding to the OCCI ID from the data provided
    Args:
        @param occi_id: OCCI ID
        @param db_data: Data containing docs
    """
    for data in db_data:
        if data['OCCI_ID'] == occi_id:
            logger.debug("Document " + occi_id + " is found")
            return data['Doc']
    logger.error("Document " + occi_id + "couldn't be found")
    return None


def make_entity_location_from_url(creator, url_path, uuid):
    """
    Creates the location of the resource/link from the occi resource/link description
    Args:
        @param url_path: Kind OCCI location to which this resource/link instance belongs to
        @param uuid: UUID of the resource/link contained in the resource/link description
        @param creator: ID creator of the resource/link instance
        @return :<string> Location of the resource/link
    """
    kind_loc = url_path.split('/-/')[1]
    entity_location = "http://" + config.OCNI_IP + ":" + config.OCNI_PORT + "/" + creator + "/" + kind_loc + uuid
    return entity_location



def make_implicit_link_location(uuid, kind_id, creator, db_occi_ids_locs):
    """
    Creates the location of the resource/link from the occi resource/link description
    Args:
        @param kind_id: Kind OCCI id to which this link instance belongs to
        @param uuid: UUID of the link contained in the link description
        @param creator: ID creator of the link instance
        @param db_occi_ids_locs: OCCI IDs and locations stored in the database
        @return :<string> Location of the resource/link
    """
    for occi_id_loc in db_occi_ids_locs:
        if occi_id_loc['OCCI_ID'] == kind_id:
            kind_loc = occi_id_loc['OCCI_Location'].split('/-/')[1]
            entity_location = "http://" + config.OCNI_IP + ":" + config.OCNI_PORT + "/" + creator + "/" + kind_loc + uuid
            return entity_location

    return None


def verify_existences_kappa(occi_ids, db_occi_ids_locs):
    #verify that the target and source are different resources
    #verify that the target and source are resources and not links
    return True

def reformat_url_path(url_path):
    """
    Reformat the URL path to a category path
    Args:
        @param url_path: URL path
    """
    loc = url_path.split(config.PyOCNI_Server_Address)
    new_path = config.PyOCNI_Server_Address+"/-"+loc[1]
    return new_path

def format_url_path(cat_path):
    """
    format the category path to a URL path
    Args:
        @param cat_path: Category path
    """
    loc = cat_path.split("/-/")
    new_path = config.PyOCNI_Server_Address+"/"+loc[1]
    return new_path


def update_occi_entity_attributes(old_attr,new_attr):
    """

    """

def look_for_update_key_values(new_attr):

    for key in new_attr:
        if type(new_attr[key]) is dict:
            look_for_update_key_values(new_attr[key])
        else:
            return key