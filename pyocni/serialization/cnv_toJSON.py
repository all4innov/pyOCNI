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

    return term,scheme,ht_class,title,rel,location,attributes,actions

def extract_term_from_category(http_item):

    term = None
    if http_item.find('=') == -1:
        to_del = http_item.find(':')
        if to_del != -1:
            term = http_item[:to_del] + http_item[to_del+1:]
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

    return my_split(rel,[',',' '])



def create_JSON_format_attributes(attributes):

    att_list = my_split(attributes,[',',' '])
    atts = list()
    for item in att_list:
        atts.extend(item.split('.'))
    return atts


def create_JSON_format_actions(actions):
    return my_split(actions,[',',' '])

def clean_quotes(string):

    to_del = string.find("\"")
    if to_del != -1:
        string = string[:to_del] + string[to_del+1:]
        to_del = string.find("\"")
        if to_del != -1:
            string = string[:to_del] + string[to_del+1:]

    return string

def my_split(s, seps):
    res = [s]
    for sep in seps:
        s, res = res, []
        for seq in s:
            res += seq.split(sep)
    return res

if __name__ == "__main__":

    cat = "Category : my_stuff;" \
          "scheme=\"http://example.com/occi/my_stuff#\";" \
          "# class=\"mixin\";" \
          "rel=\"http:/example.com/occi/something_else#mixin\";"\
          "title=\"Storage Resource\";" \
          "location=\"/my_stuff/\";" \
          "attributes=\"occi.storage.size{required} occi.storage.state{immutable}\";" \
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

    cat = "occi.storage.size{required} occi.storage.state{immutable}"

#    to_del = cat.find(':')
#    print to_del
#    if to_del != -1:
#        print ".." + cat[:to_del] + "--" + cat[to_del+1:] + "**"
#        term = cat[:to_del-1] + cat[to_del+1:]
#    else:
#        term = None

    res = create_JSON_format_attributes(cat)


#    to_del = res.find("\"")
#    if to_del != -1:
#        res = res[:to_del] + res[to_del+1:]
#        to_del = res.find("\"")
#        if to_del != -1:
#            res = res[:to_del] + res[to_del+1:]
    print res

