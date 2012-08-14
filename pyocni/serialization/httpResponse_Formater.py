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
import pyocni.serialization.cnv_toHTTP as extractor
from webob import Response

class To_HTTP_Text_Plain():
    """
    formats JSON object to HTTP text/plain descriptions
    """

    def format_to_text_plain_categories(self, var):
        """
        Format JSON categories into HTTP text/plain categories
        Args:
            @param var: JSON categories
        """
        resp=""
        if var.has_key('kinds'):
            items = var['kinds']
            for item in items:
                resp += "Category :" + cnv_JSON_category(item,"kind") + "\n"

        if var.has_key('mixins'):
            items = var['mixins']
            for item in items:
                resp += "Category :" + cnv_JSON_category(item,"mixin") + "\n"

        if var.has_key('actions'):
            items = var['actions']
            for item in items:
                resp += "Category :" + cnv_JSON_category(item,"action") + "\n"

        return resp

    def format_to_text_plain_entities(self, var):
        """
        Convert a JSON resource description into a text/plain resource description
         Args:
            @param var: JSON resource description
        """

        response = ""
        if var.has_key('resources'):
            items = var['resources']
            for item in items:
                cat,link,att = cnv_JSON_Resource(item)

                for c in cat:
                    response += "Category: " + c + "\n"

                for l in link:
                    response += "Link: " + l + "\n"

                for a in att:
                    response += "X-OCCI-Attribute: " + a + "\n"

                response = response[:-1] + ",\n"
            response = response[:-2]

        if var.has_key('links'):

            items = var['links']
            response += ",\n"
            for item in items:
                cat,link,att = cnv_JSON_Resource(item)

                for c in cat:
                    response += "Category: " + c + "\n"

                for l in link:
                    response += "Link: " + l + "\n"

                for a in att:
                    response += "X-OCCI-Attribute: " + a + "\n"

                response = response[:-1] + ",\n"
            response = response[:-2]
        return response

    def format_to_text_plain_locations(self, var):
        """
        Converts JSON locations into HTTP locations
        Args:
            var: JSON locations
        """
        locs = ""
        for item in var:
            locs += "X-OCCI-Location: " + item + "\n"
        return locs


class To_HTTP_Text_OCCI():
    """
    formats JSON object to HTTP text/plain descriptions
    """
    def format_to_text_occi_categories(self, var):
        """
        Format JSON categories into HTTP text/plain categories
        Args:
            @param var: JSON categories
        """
        resp= Response()
        resp.headers.clear()
        value =""
        if var.has_key('kinds'):
            items = var['kinds']
            for item in items:
                value = cnv_JSON_category(item,"kind") +",\n"
                resp.headers.add('Category',value[:-2])

        if var.has_key('mixins'):
            items = var['mixins']

            for item in items:
                value = cnv_JSON_category(item,"mixin") + ",\n"
                resp.headers.add('Category',value[:-2])

        if var.has_key('actions'):
            items = var['actions']
            for item in items:
                value = cnv_JSON_category(item,"action") + ",\n"
                resp.headers.add('Category',value[:-2])

        return resp.headers

    def format_to_text_occi_entities(self, var):
        """
        Convert a JSON resource description into a text/occi resource description
         Args:
            @param var: JSON resource description
        """
        response = Response()
        response.headers.clear()
        if var.has_key('resources'):
            items = var['resources']
            for item in items:
                cat,link,att = cnv_JSON_Resource(item)

                for c in cat:
                    response.headers.add("Category" ,c)

                for l in link:
                    response.headers.add("Link",l)

                for a in att:
                    response.headers.add("X-OCCI-Attribute",a)


        if var.has_key('links'):

            items = var['links']
            for item in items:
                cat,link,att = cnv_JSON_Resource(item)

                for c in cat:
                    response.headers.add("Category" ,c)

                for l in link:
                    response.headers.add("Link",l)

                for a in att:
                    response.headers.add("X-OCCI-Attribute",a)

        return response.headers

    def format_to_text_occi_locations(self, var):
        """
        Converts JSON locations into HTTP locations
        Args:
            var: JSON locations
        """
        locs = ""
        resp = Response()
        resp.headers.clear()
        for item in var:
            locs += item + ","
        resp.headers.add("X-OCCI-Location",locs[:-1])
        return resp.headers



class To_HTTP_Text_URI_List():
    """
    formats JSON object to HTTP text/plain descriptions
    """
    def __init__(self):
        pass

    def check_for_uri_locations(self, var):
        """
        Checks for the existence of path URIs in a JSON location object
        Args:
            @param var: JSON location object
        """
        resp = ""
        is_text_uri = False
        for item in var:
            resp += item + "\n"
            if item.endswith("/"):
                is_text_uri = True

        return resp,is_text_uri


def cnv_JSON_category(category,type):
    """
    Converts a json category into a HTTP category
    Args:
        @param category: JSON category
        @param type: Category type = (kind || mixin || action)
    """
    http_cat = extractor.extract_term_from_category(category) +';'
    http_cat +="scheme=\"" + extractor.extract_scheme_from_category(category) + "\";"
    http_cat +="class=\"" + type + "\";"

    title = extractor.extract_title_from_category(category)
    if title is not None:
        http_cat +="title=\"" + title + "\";"

    rel = extractor.extract_related_from_category(category)
    if rel is not None:
        http_cat +="rel=\"" + rel + "\";"

    attributes = extractor.extract_attributes_from_category(category)
    if attributes is not None:
        http_cat +="attributes=\"" + attributes + "\";"

    actions = extractor.extract_actions_from_category(category)
    if actions is not None:
        http_cat +="actions=\"" + actions + "\";"

    location = extractor.extract_location_from_category(category)
    if location is not None:
        http_cat +="location=\"" + location + "\";"

    return http_cat


def cnv_JSON_Resource(json_object):
    """
    Converts a JSON Resource into a HTTP Resource
    """
    res_cat = list()
    res_links = list()
    res_cat.append(extractor.extract_kind_from_entity(json_object))

    items = extractor.extract_mixin_from_entity(json_object)
    if items is not None:
        res_cat.extend(items)

    var= extractor.extract_attributes_from_entity(json_object)
    if var is not None:
        res_att = var
    else:
        res_att = list()

    items = extractor.extract_internal_link_from_entity(json_object)
    if items is not None:
        res_links.extend(items)

    items = extractor.extract_actions_from_entity(json_object)
    if items is not None:
        res_links.extend(items)

    return res_cat,res_links,res_att


