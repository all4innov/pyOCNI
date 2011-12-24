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
Created on Feb 25, 2011

@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Telecom - Telecom SudParis
@version: 0.1
@license: LGPL - Lesser General Public License
"""

import pyocni.pyocni_tools.config as config
import re

from pyocni.specification.occi_core import Category, Kind, Mixin, Action, Entity, Resource, Link
from pyocni.registry.registry import location_registry

# getting the Logger
logger = config.logger

# getting IP and Port of the OCCI server
OCNI_IP = config.OCNI_IP
OCNI_PORT = config.OCNI_PORT


# ======================================================================================
# headers
# ======================================================================================
header_category = "Category"
header_link = "Link"
header_attribute = "X-OCCI-Attribute"
header_location = "X-OCCI-Location"


# ======================================================================================
# OCCI Category rendering
# Rendering of the OCCI Category, Kind and Mixin types
# ======================================================================================
class category_renderer(object):
    def renderer(self, obj):
        header = {}
        category_value = ''
        category_param = ''

        if isinstance(obj, Kind):
            _category = obj
            _classe = 'kind'
        elif isinstance(obj, Mixin):
            _category = obj
            _classe = 'mixin'
        elif isinstance(obj, Action):
            _category = obj.category
            _classe = 'action'
        else:
            logger.warning("Object bad type: Only a kind, mixin or an action can be rendered as a category")
            raise ("Object bad type: Only a kind, mixin or an action can be rendered as a category")

        category_value += _category.term + ';\nscheme="' + _category.scheme + '";\nclass="' + _classe + '";\n'

        if _category.title != '':
            category_param += 'title="' + _category.title + '";\n'

        if _category.related.__len__() > 0:
            __related_objects = ''
            for rel in _category.related:
                __related_objects += rel.__repr__() + " "
            category_param += 'rel="' + __related_objects + '";\n'

        _location_registry = location_registry()
        _location = _location_registry.get_location(_category)
        category_param += 'location=' + _location + ';\n'

        if _classe == 'kind' or _classe == 'mixin':
            __attributes = ''
            for __attribute in _category.attributes:
                __attributes += __attribute.name + ' '
            category_param += 'attributes="' + __attributes + '";\n'

        if _classe == 'kind' or _classe == 'mixin':
            __actions = ''
            for __action in _category.actions:
                __actions += __action.__repr__() + ' '
            category_param += 'actions="' + __actions + '";'

        header[header_category] = category_value + category_param

        return header


# ======================================================================================
# OCCI Link instance rendering
# Rendering of OCCI Link instance references
# ======================================================================================
class link_renderer(object):
    def renderer(self, obj):
        header = {}
        link_value = ''
        link_param = ''

        if isinstance(obj, Link):
            _location_registry = location_registry()
            _location_of_obj = _location_registry.get_location(obj)

            _source = obj.occi_core_source
            _target_location = obj.occi_core_target

            _target_object = _location_registry.get_object(_target_location)

            logger.debug('the Target location of this link is: ' + _target_location)
            logger.debug('the Target object of this link is: ' + _target_object.__repr__())

            link_value += '<' + _target_location + '>;\nrel="' + _target_object.kind.__repr__() + '";\nself="' + _location_of_obj + '";\n'

            link_param += 'category="' + obj.kind.__repr__() + '";'

            for attribute in obj.kind.attributes:
                link_param += '\n' + attribute.name + '="' + obj.__getattribute__(
                    re.sub('\.', '_', attribute.name)) + '";'

        else:
            logger.warning("Object bad type: Only a Link can be rendered")
            raise ("Object bad type: Only a Link can be rendered")

        header[header_link] = link_value + link_param

        return header


# ======================================================================================
# OCCI action instance rendering
# Rendering of references to OCCI Action instances
# ======================================================================================
class action_renderer(object):
    def renderer(self, obj, action):
        header = {}
        link_value = ''

        if isinstance(obj, Resource):
            _location_registry = location_registry()
            _location_of_obj = _location_registry.get_location(obj)

            _location_of_action = _location_of_obj + '?action=' + action.category.term

            link_value += '<' + _location_of_action + '>;\nrel="' + action.__repr__() + '"'
        else:
            logger.warning("Object bad type: Only a Resource can be rendered")
            raise ("Object bad type: Only a Resource can be rendered")

        header[header_link] = link_value

        return header


# ======================================================================================
# OCCI Entity attributes rendering
# Rendering of OCCI Entity attributes
# ======================================================================================
class attributes_renderer(object):
    def renderer(self, obj):
        header = {}
        attribute_value = []

        if isinstance(obj, Entity):
            for attribute in obj._kind.attributes:
                attribute_value.append(
                    attribute.name + '="' + str(obj.__getattribute__(re.sub('\.', '_', attribute.name))) + '"')

        else:
            logger.warning("Object bad type: Only an Entity can be rendered")
            raise ("Object bad type: Only an Entity can be rendered")

        header[header_attribute] = attribute_value

        return header


# ======================================================================================
# OCCI Location-URIs rendering
# Rendering of Location-URIs
# ======================================================================================
class location_renderer(object):
    def renderer(self, locations):
        header = {}
        location_values = []

        for location in locations:
            authority = OCNI_IP + ':' + OCNI_PORT
            location_values.append(authority + location)

        header[header_location] = location_values

        return header


# ======================================================================================
# OCCI Content-type text/plain rendering
# ======================================================================================
class text_plain_renderer(object):
    pass


# ======================================================================================
# OCCI Content-type text/occi rendering
# ======================================================================================
class text_occi_renderer(object):
    pass


# ======================================================================================
# OCCI Content-type text/uri-list rendering
# ======================================================================================
class text_urilist_renderer(object):
    pass


# ======================================================================================
# OCCI main rendering
# ======================================================================================
class main_renderer(object):
    pass


# ======================================================================================
# main
# ======================================================================================
if __name__ == '__main__':
    print 'test'
    print OCNI_IP + ':' + OCNI_PORT
    pass
