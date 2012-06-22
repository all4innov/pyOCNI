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
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@version: 0.3
@license: LGPL - Lesser General Public License

"""
import pyocni.pyocni_tools.config as config
# getting the Logger
logger = config.logger

def update_occi_description(oldData,newData):
    """
    Update only a part of the occi description
    Args:
        @param newData: The new OCCI description
        @param oldData: The old OCCI description
        @return : Updated data and a boolean (false if all fields are updated, true if there were some un-updated fields)
    """

    #Try to get the keys from occi description dictionary
    oldData_keys = oldData.keys()
    newData_keys = newData.keys()
    problems = False
    for key in newData_keys:
        try:
            oldData_keys.index(key)
            oldData[key] = newData[key]
        except Exception:
            #Keep the record of the keys(=parts) that couldn't be updated
            logger.debug("update description : " + key + " could not be found")
            problems = True

    return problems,oldData

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
    for key in filter_keys:
        try:
            if description[key] != filter[key]:
                return False
        except Exception:
            #Keep the record of the keys(=parts) that couldn't be updated
            logger.debug("filter description : "+ key + " could not be found")
            return False

    return True

def dissociate_resource_from_mixin(occi_id):
    """
    Dissociates a resource from a mixin upon the deletion of a mixin
    Args:
        @param mix_desc: OCCI description of the mixin
    """
    return True
def get_resources_belonging_to_kind(kind_desc):
    """
    Verifies if there are resources of this kind description
    Args:
        @param kind_desc: OCCI kind description of the kind

    """
    return True


def verify_exist_relaters(description,db_data):
    """
    Verify the existence of the related kinds or mixins
    Args:
        @param description: OCCI description to test the existence of the related urls
        @param db_data: Data already stored in database
    """
    try:
        relaters = description['related']
    except Exception as e:
        logger.debug(" exist relaters : " + e.message)
        return True
    if not relaters:
        return True

    list_occi_id = list()
    for data in db_data:
        id = get_description_id(data)
        list_occi_id.append(id)

    try:
        for related in relaters:
            list_occi_id.index(related)
    except Exception as e:
        logger.error(" exist relaters : " + e.message)
        return False

    return True

def verify_exist_actions(description,actions_data):
    """

    """
    try:
        actions = description['actions']
    except Exception as e:
        logger.debug("exist actions " + e.message)
        return True
    if not actions:
        return True

    list_occi_id = list()
    for data in actions_data:
        id = get_description_id(data)
        list_occi_id.append(id)


    for action in actions:
        try:
            list_occi_id.index(action)
        except Exception as e:
            logger.error(" exist actions : " + e.message)
            return False
    return True




def make_kind_location(occi_description):
    """
    Creates the location of the kind using the occi_description
    Args:
        @param occi_description: the occi description of the kind
        @return :<string> Location of the kind
    """
    try:
        loc = occi_description['location']
        kind_location = "http://" + config.OCNI_IP + ":" + config.OCNI_PORT + "/-" + loc
    except Exception as e:
        logger.error("kind location : " + e.message )
        return  None
    return kind_location

def make_mixin_location(occi_description):
    """
    Creates the location of the mixin using the occi_description
    Args:
        @param occi_description: the occi description of the mixin
        @return :<string> Location of the mixin
    """
    try:
        loc = occi_description['location']
        mixin_location = "http://" + config.OCNI_IP + ":" + config.OCNI_PORT + "/-" + loc
    except Exception as e:
        logger.error("mixin location : " + e.message )
        return None
    return  mixin_location

def make_resource_location(user_id,kind_loc, uuid):
    """
    Creates the location of the resource from the occi resource description
    Args:
        @param kind_loc: Kind OCCI location to which this resource instance belongs to
        @param uuid: UUID of the resource contained in the resource description
        @param user_id: ID creator of the resource instance
        @return :<string> Location of the resource
    """

    resource_location = "http://" + config.OCNI_IP + ":" + config.OCNI_PORT + "/" + user_id + kind_loc + uuid
    return resource_location

def make_link_location(user_id,kind_loc, uuid):
    """
    Creates the location of the resource from the occi resource description
    Args:
        @param kind_loc: Kind OCCI location to which this resource instance belongs to
        @param uuid: UUID of the resource contained in the resource description
        @param user_id: ID creator of the resource instance
        @return :<string> Location of the resource
    """

    link_location = "http://" + config.OCNI_IP + ":" + config.OCNI_PORT + "/" + user_id + kind_loc + uuid
    return link_location