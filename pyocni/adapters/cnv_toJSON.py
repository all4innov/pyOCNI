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
Created on Jun 21, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@license: Apache License, Version 2.0
"""

try:
    import simplejson as json
except ImportError:
    import json


def splitter(http_obj):
    res = http_obj.split(';')
    term = scheme = ht_class = title = rel = location = attributes = actions = None
    for item in res:
        item = clean_quotes(item)
        if term is None:
            term = extract_term_from_category(item)
        if scheme is None:
            scheme = extract_scheme_from_category(item)
        if ht_class is None:
            ht_class = extract_class_from_category(item)
        if title is None:
            title = extract_title_from_category(item)
        if rel is None:
            rel = extract_rel_from_category(item)
        if location is None:
            location = extract_location_from_category(item)
        if attributes is None:
            attributes = extract_attributes_from_category(item)
        if actions is None:
            actions = extract_actions_from_category(item)

    return term, scheme, ht_class, title, rel, location, attributes, actions


def extract_term_from_category(http_item):
    term = None
    if http_item.find('=') == -1:
        to_del = http_item.find(':')
        if to_del != -1:
            term = http_item[:to_del] + http_item[to_del + 1:]
        else:
            term = http_item
    return term


def extract_scheme_from_category(http_item):
    scheme = None
    if http_item.find('=') != -1:
        item_1, item_2 = http_item.split('=')
        if item_1.find('scheme') != -1:
            scheme = item_2
    return scheme


def extract_class_from_category(http_item):
    ht_class = None
    if http_item.find('=') != -1:
        item_1, item_2 = http_item.split('=')
        if item_1.find('class') != -1:
            ht_class = item_2
    return ht_class


def extract_title_from_category(http_item):
    title = None
    if http_item.find('=') != -1:
        item_1, item_2 = http_item.split('=')
        if item_1.find('title') != -1:
            title = item_2
    return title


def extract_rel_from_category(http_item):
    rel = None
    if http_item.find('=') != -1:
        item_1, item_2 = http_item.split('=')
        if item_1.find('rel') != -1:
            rel = item_2
    return rel


def extract_location_from_category(http_item):
    location = None
    if http_item.find('=') != -1:
        item_1, item_2 = http_item.split('=')
        if item_1.find('location') != -1:
            location = item_2
    return location


def extract_attributes_from_category(http_item):
    attributes = None
    if http_item.find('=') != -1:
        item_1, item_2 = http_item.split('=')
        if item_1.find('attributes') != -1:
            attributes = item_2
    return attributes


def extract_actions_from_category(http_item):
    actions = None
    if http_item.find('=') != -1:
        item_1, item_2 = http_item.split('=')
        if item_1.find('actions') != -1:
            actions = item_2
    return actions


def extract_categories_from_body(http_body):
    return http_body.split("Category")


def extract_categories_from_headers(http_headers):
    res = http_headers['Category']
    res = res.split("Category")
    return res


def create_JSON_format_relateds(rel):
    return my_split(rel, [',', ' '])


def create_JSON_format_attributes(attributes):
    att_list = my_split(attributes, [',', ' '])
    atts = list()
    for item in att_list:
        atts.extend(item.split('.'))
    return atts


def create_JSON_format_actions(actions):
    return my_split(actions, [',', ' '])


def clean_quotes(string):
    to_del = string.find("\"")
    if to_del != -1:
        string = string[:to_del] + string[to_del + 1:]
        to_del = string.find("\"")
        if to_del != -1:
            string = string[:to_del] + string[to_del + 1:]
    to_del = string.find(" ")
    if to_del != -1:
        string = string[:to_del] + string[to_del + 1:]
        to_del = string.find(" ")
        if to_del != -1:
            string = string[:to_del] + string[to_del + 1:]

    return string


def clean_quotes_for_attributes(string):
    to_del = string.find("\"")
    if to_del != -1:
        string = string[:to_del] + string[to_del + 1:]
        to_del = string.find("\"")
        if to_del != -1:
            string = string[:to_del] + string[to_del + 1:]
    to_del = string.find(" ")
    if to_del != -1:
        string = string[:to_del] + string[to_del + 1:]
        to_del = string.find(" ")
        if to_del != -1:
            string = string[:to_del] + string[to_del + 1:]
    to_del = string.find(":")
    if to_del != -1:
        string = string[:to_del] + string[to_del + 1:]

    return string

#=======================================================================================================================
#                                                           Entity Zone
#=======================================================================================================================

def extract_kind_from_http_entity(item):
    kind = None
    if item.find("kind") != -1:
        items = item.split(';')
        scheme = term = None
        for item in items:
            item = clean_quotes(item)
            if scheme is None:
                scheme = extract_scheme_from_category(item)
            if term is None:
                term = extract_term_from_category(item)
        if (term is not None) and (scheme is not None):
            kind = scheme + term
    return kind


def extract_mixin_from_http_entity(item):
    mixin = None

    if item.find("mixin") != -1:
        items = item.split(';')
        scheme = term = None
        for item in items:
            item = clean_quotes(item)
            if scheme is None:
                scheme = extract_scheme_from_category(item)
            if term is None:
                term = extract_term_from_category(item)
        if (term is not None) and (scheme is not None):
            mixin = scheme + term
    return mixin


def extract_self_from_category(member):
    selfo = None
    if member.find('=') != -1:
        item_1, item_2 = member.split('=')
        if item_1.find('self') != -1:
            selfo = item_2

    return selfo


def extract_cat_from_http_link(member):
    cat = None
    if member.find('=') != -1:
        item_1, item_2 = member.split('=')
        if item_1.find('category') != -1:
            cat = item_2

    return cat


def extract_loc_from_http_link(member):
    loc = None
    if member.find(':'):
        to_del = member.find(':')
        if to_del != -1:
            loc = member[:to_del] + member[to_del + 1:]
    return loc


def extract_link_from_http_entity(item):
    cat = link_self = rel = loc = attributes = None
    link_list = item.split(';')

    for member in link_list:
        member = clean_quotes(member)
        if loc is None:
            loc = extract_loc_from_http_link(member)

        if rel is None:
            rel = extract_rel_from_category(member)

        if link_self is None:
            link_self = extract_self_from_category(member)

        if cat is None:
            cat = extract_cat_from_http_link(member)

    if attributes is None:
        attributes = extract_attributes_from_http_link(link_list)

    if (loc is not None) and (rel is not None) and (link_self is not None) and (cat is not None) and  (
    attributes is not None):
        return {'kind': cat,
                'attributes': attributes,
                'rel': rel,
                'self': link_self,
                'location': loc}
    else:
        return None


def extract_action_from_http_entity(item):
    cat = href = None
    act_list = item.split(';')

    for member in act_list:
        member = clean_quotes(member)

        if cat is None:
            cat = extract_rel_from_category(member)

        if (href is None) and (cat is None):
            to_del = member.find(':')
            if to_del != -1:
                href = member[:to_del] + member[to_del + 1:]

    if (cat is not None) and (href is not None):
        return {"href": href,
                "category": cat}
    else:
        return None


def extract_attributes_from_http_link(items):
    att_list = list()
    for item in items:
        if item.count('=') == 1:
            item_1, item_2 = item.split('=')
            item_1 = clean_quotes_for_attributes(item_1)
            att_list.append(item_1 + '=' + item_2)

    att_json = {}
    for att in att_list:
        att_json = cnv_attribute_from_http_to_json(att, json_result=att_json)

    return att_json


def extract_attributes_from_http_entity(items):
    att_list = list()
    for item in items:
        if item.count('=') == 1:
            item_1, item_2 = item.split('=')
            item_1 = clean_quotes_for_attributes(item_1)
            att_list.append(item_1 + '=' + item_2)

    if len(att_list) is not 0:
        att_json = {}

        for att in att_list:
            att_json = cnv_attribute_from_http_to_json(att, json_result=att_json)

        return att_json

    else:
        return None


def cnv_attribute_from_http_to_json(attribute, json_result={}):
    """

    method to convert and add one OCCI HTTP attribute to an OCCI JSON object

    # the attribute 'attribute' contains the OCCI HTTP Attribute. e.g. 'occi.compute.hostname="foobar"'
    # the attribute 'json_result' contains an OCCI JSON object. e.g. {} or {'occi': {'compute': {'cores': 2, 'hostname': 'foobar'}}}
    """
    attribute_partitioned = attribute.partition('=')
    attribute_name = attribute_partitioned[0]
    attribute_value = attribute_partitioned[2]
    attribute_name_partitioned = attribute_name.split('.')

    a = json_result
    for i in range(len(attribute_name_partitioned)):
        if a.has_key(attribute_name_partitioned[i]):
            if i < (len(attribute_name_partitioned) - 1):
                a = a[attribute_name_partitioned[i]]
            else:
                try:
                    a[attribute_name_partitioned[i]] = json.loads(attribute_value)
                except Exception:
                    a[attribute_name_partitioned[i]] = attribute_value

        else:
            if i < (len(attribute_name_partitioned) - 1):
                a[attribute_name_partitioned[i]] = {}
                a = a[attribute_name_partitioned[i]]
                json_result.update(a)
            else:
                try:
                    a[attribute_name_partitioned[i]] = json.loads(attribute_value)
                except Exception:
                    a[attribute_name_partitioned[i]] = attribute_value

    return json_result


def action_or_link(item):
    if item.count('=') > 2:
        return False
    return True


def get_entity_members_from_body(data):
    kind = None
    mixins = list()
    actions = list()
    links = list()
    entity_list = my_split(data, ["Category", "X-OCCI-Attribute", "Link"])

    for item in entity_list:
        if kind is None:
            kind = extract_kind_from_http_entity(item)

        mixin = extract_mixin_from_http_entity(item)
        if mixin is not None:
            mixins.append(mixin)

        is_action = action_or_link(item)
        if is_action is True:
            action = extract_action_from_http_entity(item)
            if action is not None:
                actions.append(action)
        else:
            link = extract_link_from_http_entity(item)
            if link is not None:
                links.append(link)

    attributes = extract_attributes_from_http_entity(entity_list)

    return kind, mixins, attributes, actions, links


def get_entity_members_from_headers(headers):
    kind = None
    mixins = list()
    actions = list()
    links = list()
    entity_list = list()
    if headers.__contains__('Category'):
        categories = headers['Category']
        entity_list.extend(categories.split(','))

    if headers.__contains__('Link'):
        link_headers = headers['Link']
        entity_list.extend(link_headers.split(','))

    if headers.__contains__('X-OCCI-Attribute'):
        att_h = headers['X-OCCI-Attribute']
        entity_list.extend(att_h.split(','))

    for item in entity_list:
        if kind is None:
            kind = extract_kind_from_http_entity(item)

        mixin = extract_mixin_from_http_entity(item)
        if mixin is not None:
            mixins.append(mixin)

        is_action = action_or_link(item)
        if is_action is True:
            action = extract_action_from_http_entity(item)
            if action is not None:
                actions.append(action)
        else:
            link = extract_link_from_http_entity(item)
            if link is not None:
                links.append(link)

    attributes = extract_attributes_from_http_entity(entity_list)

    return kind, mixins, attributes, actions, links

#=======================================================================================================================
#                                                           Independant functions Zone
#=======================================================================================================================
def my_split(s, seps):
    res = [s]
    for sep in seps:
        s, res = res, []
        for seq in s:
            res += seq.split(sep)
    return res

if __name__ == "__main__":
    cat = "Category : my_stuff;"\
          "scheme=\"http://example.com/occi/my_stuff#\";"\
          "# class=\"mixin\";"\
          "rel=\"http:/example.com/occi/something_else#mixin\";"\
          "title=\"Storage Resource\";"\
          "location=\"/my_stuff/\";"\
          "attributes=\"occi.storage.size{required} occi.storage.state{immutable}\";"\
          "actions=\"http://schemas.ogf.org/occi/infrastructure/storage/action#resize ...\";"\
          "Category : my_stuff;"\
          "scheme=\"http://example.com/occi/my_stuff#\";"\
          "# class=\"mixin\";"\
          "rel=\"http:/example.com/occi/something_else#mixin\";"\
          "title=\"Storage Resource\";"\
          "location=\"/my_stuff/\";"\
          "attributes=\"occi.storage.size{required} occi.storage.state{immutable}\";"\
          "actions=\"http://schemas.ogf.org/occi/infrastructure/storage/action#resize ...\";"\
          "Category : my_stuff;"\
          "scheme=\"http://example.com/occi/my_stuff#\";"\
          "# class=\"mixin\";"\
          "rel=\"http:/example.com/occi/something_else#mixin\";"\
          "title=\"Storage Resource\";"\
          "location=\"/my_stuff/\";"\
          "attributes=\"occi.storage.size{required} occi.storage.state{immutable}\";"\
          "actions=\"http://schemas.ogf.org/occi/infrastructure/storage/action#resize ...\";"

    cat = "</network/123>;"\
          "rel=\"http://schemas.ogf.org/occi/infrastructure#network\";"\
          "self=\"/link/networkinterface/456\";"\
          "category=\"http://schemas.ogf.org/occi/infrastructure#networkinterface\";"\
          "occi.networkinterface.interface=\"eth0\";"\
          "occi.networkinterface.mac=\"00:11:22:33:44:55\";"\
          "occi.networkinterface.state=\"active\";"


    #    to_del = cat.find(':')
    #    print to_del
    #    if to_del != -1:
    #        print ".." + cat[:to_del] + "--" + cat[to_del+1:] + "**"
    #        term = cat[:to_del-1] + cat[to_del+1:]
    #    else:
    #        term = None
    from webob import Request, Response

    req = Response()
    req.headers.add('Category',
        "my_stuff;scheme=\"http://example.com/occi/my_stuff#\";class=\"mixin\",my_stuff;scheme=\"http://example.com/occi/my_stuff#\";class=\"mixin\",my_stuff;scheme=\"http://example.com/occi/my_stuff#\";class=\"mixin\"")
    res = req.headers
    print res['Category']


    #    to_del = res.find("\"")
    #    if to_del != -1:
    #        res = res[:to_del] + res[to_del+1:]
    #        to_del = res.find("\"")
    #        if to_del != -1:
    #            res = res[:to_del] + res[to_del+1:]
    print res

