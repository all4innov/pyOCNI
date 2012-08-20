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
Created on Jun 21, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@version: 0.3
@license: LGPL - Lesser General Public License
"""

try:
    import simplejson as json
except ImportError:
    import json


def extract_term_from_category(json_object):
    """
    returns the term from a json representation
    Args:
        @param json_object: JSON representation
    """
    if json_object.has_key('term'):
        return json_object['term']
    else:
        return None

def extract_scheme_from_category(json_object):
    """
    returns the scheme from a json representation
    Args:
        @param json_object: JSON representation
    """
    if json_object.has_key('scheme'):
        return json_object['scheme']
    else:
        return None

def extract_location_from_category(json_object):
    """
    returns the location from a json representation
    Args:
        @param json_object: JSON representation
    """
    if json_object.has_key('location'):
        return json_object['location']
    else:
        return None

def extract_title_from_category(json_object):
    """
    returns the title from a json representation
    Args:
        @param json_object: JSON representation
    """
    if json_object.has_key('title'):
        return json_object['title']
    else:
        return None

def extract_related_from_category(json_object):
    """
    returns the related from a json representation
    Args:
        @param json_object: JSON representation
    """
    if json_object.has_key('related'):
        items = json_object['related']
        rel =""
        for item in items:
            rel += item +","
        rel = rel[:-1]
    else:
        rel = None
    return rel

def extract_actions_from_category(json_object):
    """
    returns the actions from a json representation
    Args:
        @param json_object: JSON representation
    """
    if json_object.has_key('actions'):
        items = json_object['actions']
        actions = ""
        for item in items:
            actions += item +","
        actions = actions[:-1]
    else:
        actions = None
    return actions

def extract_attributes_from_category(json_object):
    """
    returns the attributes from a json representation
    Args:
        @param json_object: JSON representation
    """
    if json_object.has_key('attributes'):
        items = json_object['attributes']
        attributes = recursive_for_attribute(items)
        htt_att = ""
        for att in attributes:
            htt_att += att +","
        attributes = htt_att[:-1]
    else:
        attributes = None
    return attributes

def extract_kind_from_entity(json_object):
    """
    returns the HTTP kind description extracted from a json entity representation
    Args:
        @param json_object: JSON representation
    """
    if json_object.has_key('kind'):
        kind_id = json_object['kind']
        kind_scheme,kind_term = kind_id.split('#')
        return kind_term + "; scheme=\"" + kind_scheme +"\"; class=\"kind\";"
    else:
        return None

def extract_mixin_from_entity(json_object):
    """
    returns mixins of the entity
    Args:
        @param json_object: JSON representation
    """
    if json_object.has_key('mixin'):
        mix_http = list()
        mixins = json_object['mixin']
        for item in mixins:
            mix_scheme,mix_term = item.split('#')
            mix_http.append( mix_term + "; scheme=\"" + mix_scheme +"\"; class=\"mixin\";")
        return mix_http
    else:
        return None

def extract_id_from_entity(json_object):
    """
    returns id of the entity
    Args:
        @param json_object: JSON representation
    """
    if json_object.has_key('id'):
        return json_object['id']
    else:
        return None

def extract_title_from_entity(json_object):
    """
    returns title of the entity
    Args:
        @param json_object: JSON representation
    """
    if json_object.has_key('title'):
        return json_object['title']
    else:
        return None

def extract_actions_from_entity(json_object):
    """
    returns actions of the entity
    Args:
        @param json_object: JSON representation
    """
    if json_object.has_key('actions'):
        items = json_object['actions']
        actions = list()
        for item in items:
            actions.append("<" + item['href'] + ">; rel=\"" + item['category'] +"\"")
        return actions
    else:
        return None

def extract_internal_link_from_entity(json_object):
    """
    returns internal links of the entity
    Args:
        @param json_object: JSON representation
    """
    if json_object.has_key('links'):
        items = json_object['links']
        links = list()
        for item in items:
            uri = "|zizi|"
            rel = "|zala|"
            category = item['kind']
            self = "|zolo|"
            link = "<" + uri + ">; rel=\"" + rel +"\"; self=\"" + self + "\"; category=\"" + category + "\";"
            if item.has_key('attributes'):
                attributes = recursive_for_attribute_v2(item['attributes'])
                for att in attributes:
                    link += att[:-1] + ";"
            links.append(link)
        return links
    else:
        return None

def extract_attributes_from_entity(json_object):
    """
    returns the attributes from a json representation
    Args:
        @param json_object: JSON representation
    """
    if json_object.has_key('attributes'):
        items = json_object['attributes']
        attributes = recursive_for_attribute_v2(items)
        return attributes
    else:
        return None

def treat_attribute_members(members):

    to_return = ""
    for key in members.keys():

        if key == "mutable":
            if members[key] is True:
                to_return += ""
            else:
                to_return += "{immutable}"
        elif key == "required":
            if members[key] is True:
                to_return += "{required}"
            else:
                to_return += ""
        else:
            pass

    return [to_return]

def recursive_for_attribute(attributes):
    """

    """

    att_http = list()
    for key in attributes.keys():
        if type(attributes[key]) is dict:
            items = recursive_for_attribute(attributes[key])
            for item in items:
                if not (item.find('{')):
                    att_http.append(key + item)
                else:
                    att_http.append(key + "." + item)
        else:
            attributes = treat_attribute_members(attributes)
            return attributes
    final_att = list()
    for item in att_http:
        if item.endswith('.'):
            final_att.append(item[:-1])
        else:
            final_att.append(item)
    return final_att


def treat_attribute_members_v2(attributes):
    to_return = list()
    for key in attributes.keys():
        to_return.append(key + "=\"" + str(attributes[key]) +"\"")
    return to_return


def recursive_for_attribute_v2(attributes):
    """

    """

    att_http = list()
    for key in attributes.keys():
        if type(attributes[key]) is dict:
            items = recursive_for_attribute_v2(attributes[key])
            for item in items:
                att_http.append(key + "." + item)
        else:
            attributes = treat_attribute_members_v2(attributes)
            return attributes

    return att_http


if __name__ == '__main__':
    print '====== Test ======'


    att = """

{
    "occi": {
        "compute": {
            "speed": 2,
            "memory": 4,
            "cores": 2
        }
    },
    "org": {
        "other": {
            "occi": {
                "my_mixin": {
                    "my_attribute": "my_value"
                }
            }
        }
    }
}

"""
    attold ="""
    {"occi": {
        "compute": {
            "hostname": {
                "mutable": true,
                "required": false,
                "type": "string",
                "pattern": "(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\\\\-]*[a-zA-Z0-9])\\\\.)*",
                "minimum": "1",
                "maximum": "255"
            },
            "state": {
                "mutable": false,
                "required": false,
                "type": "string",
                "pattern": "inactive|active|suspended|failed",
                "default": "inactive"
            }
        }
    }}
"""
    att_obj = json.loads(att)
    res = recursive_for_attribute_v2(att_obj)
#    json_mixin = json.loads(mixin)
#    res = convert_json_action_to_http_action(json_mixin)

    print res
