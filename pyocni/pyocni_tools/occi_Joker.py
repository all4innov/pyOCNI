# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

# Copyright (C) 2011 Houssem Medhioub - Institut Telecom
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
@organization: Institut Telecom - Telecom SudParis
@version: 0.2
@license: LGPL - Lesser General Public License

"""
import pyocni.pyocni_tools.config as config

def update_part_of_kind(doc_id,newData,j_oldData,newData_keys):
    """
    update only a part of the kind description (can be called only after a failed try to fully update the kind description)
    """

    #Try to change parts of the kind description
    oldData_keys =  j_oldData['kinds'][0].keys()
    problems = False
    for key in newData_keys:
        try:
            oldData_keys.index(key)
            j_oldData['kinds'][0][key] = newData[key]
        except Exception:
            #Keep the record of the keys(=parts) that couldn't be updated

            problems = True
    if problems:
        message = "Document " + str(doc_id) + " has not been totally updated. Check log for more details"
    else:
        message = "Document " + str(doc_id) + " has been updated successfully"
    return j_oldData,message

def make_kind_location(occi_description, uuid,user_id):
    """
    Creates the location of the Kind from the occi kind description
    Args:
        @param occi_description: OCCI kind description
        @param uuid: UUID of the kind document containing the kind description
        @param user_id: ID of kind document administrator
        @return :<string> Location of the kind
    """
    try:
        kind_term = occi_description['kinds'][0]['term']
    except Exception as e:
        return e.message

    kind_location = "http://" + config.OCNI_IP + ":" + config.OCNI_PORT + "/-/" + kind_term + "/" + user_id + "/" + uuid
    return kind_location

def make_mixin_location(occi_description, uuid,user_id):
    """
    Creates the location of the mixin from the occi mixin description
    Args:
        @param occi_description: OCCI mixin description
        @param uuid: UUID of the mixin document containing the mixin description
        @param user_id: ID of mixin document administrator
        @return :<string> Location of the mixin
    """
    try:
        mixin_term = occi_description['mixins'][0]['term']
    except Exception as e:
        return False,e.message

    mixin_location = "http://" + config.OCNI_IP + ":" + config.OCNI_PORT + "/-/" + mixin_term + "/" + user_id + "/" + uuid
    return True, mixin_location

def make_action_location(occi_description, uuid,user_id):
    """
    Creates the location of the action from the occi action description
    Args:
        @param occi_description: OCCI action description
        @param uuid: UUID of the action document containing the action description
        @param user_id: ID of action document administrator
        @return :<string> Location of the action
    """
    try:
        action_term = occi_description['actions'][0]['term']
    except Exception as e:
        return False,e.message

    action_location = "http://" + config.OCNI_IP + ":" + config.OCNI_PORT + "/-/" + action_term + "/" + user_id + "/" + uuid
    return True, action_location

def make_resource_location(occi_description, uuid,user_id):
    """
    Creates the location of the resource from the occi resource description
    Args:
        @param occi_description: OCCI resource description
        @param uuid: UUID of the resource document containing the resource description
        @param user_id: ID of resource document administrator
        @return :<string> Location of the resource
    """
    try:
        resource_term = occi_description['resources'][0]['kind']
        resource_term = resource_term.split('#')[1]
    except Exception as e:
        return False,e.message

    resource_location = "http://" + config.OCNI_IP + ":" + config.OCNI_PORT + "/" + resource_term + "/" + user_id + "/" + uuid
    return True, resource_location

def make_link_location(occi_description, uuid,user_id):
    """
    Creates the location of the link from the occi link description
    Args:
        @param occi_description: OCCI link description
        @param uuid: UUID of the link document containing the link description
        @param user_id: ID of link document administrator
        @return :<string> Location of the link
    """
    try:
        link_term = occi_description['link'][0]['kind']
        link_term = link_term.split('#')[1]
    except Exception as e:
        return False,e.message

    link_location = "http://" + config.OCNI_IP + ":" + config.OCNI_PORT + "/" + link_term + "/" + user_id + "/" + uuid
    return True, link_location