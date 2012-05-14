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

import pyocni.pyocni_tools as tools
import pyocni.pyocni_tools.config as config
import re

import pyocni.pyocni_tools.mixin as mixin_tools

import cStringIO

try:
    import simplejson as json
except ImportError:
    import json

import jsonpickle

from collections import OrderedDict

from  pyocni.specification.occi_core import Category, Kind, Mixin, Action, Entity, Resource, Link

from pyocni.registry.registry import location_registry, category_registry

# getting the Logger
logger = config.logger

# getting IP and Port of the OCCI server
OCNI_IP = config.OCNI_IP
OCNI_PORT = config.OCNI_PORT


################################### For testing ############################################################
# category = {'id': 'resourceID', 'title': "CloNe resource number 1"}
#kind = {'kind': {'term': 'CloNeNode', 'scheme': 'http://schemas.ogf.org/occi/ocni', 'class': 'kind',
#                 'title': 'Cloud networking Node'}}
#mixin1 = {'term': 'my_stuff1', 'scheme': 'http://example.com/occi/ocni/my_stuff1', 'class': 'mixin',
#          'title': 'my_stuff1 mixin'}
#mixin2 = {'term': 'my_stuff2', 'scheme': 'http://example.com/occi/ocni/my_stuff2', 'class': 'mixin',
#          'title': 'my_stuff2 mixin'}
#mixins = {'mixins': [mixin1, mixin2]}
#result_json = OrderedDict(category.items() + kind.items() + mixins.items())
#result_dump = cStringIO.StringIO()
#json.dump(result_json, result_dump, indent=4 * ' ')
#print 'json-serialization=', result_dump.getvalue()
#############################################################################################################


# ======================================================================================
# OCCI Category serialization
# Rendering of the OCCI Category, Kind and Mixin types
# ======================================================================================
class category_serializer(object):
    """

    This class is used for the serialization of OCCI category (Kind, Mixin, action) in JSON

    """

    def to_json(self, obj):
        """

        method to convert an object (OCCI object) to a JSON format

        """
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

        category_dict = {'term': _category.term, 'scheme': _category.scheme, 'class': _classe, 'title': _category.title}

        self.category_rel_dict = OrderedDict({'rel': []})
        if _category.related.__len__() > 0:
            category_rel_values = list()
            for rel in _category.related:
                category_rel_values.append(rel.__repr__())
            self.category_rel_dict = {'rel': category_rel_values}

        self._location_registry = location_registry()
        _location = self._location_registry.get_location(_category)
        self.category_location_dict = OrderedDict({'location': _location})

        self.category_attributes_dict = OrderedDict({'attributes': []})
        if _classe == 'kind' or _classe == 'mixin':
            category_attributes_values = list()
            for __attribute in _category.attributes:
                category_attributes_values.append(__attribute.name)
            self.category_attributes_dict = {'attributes': category_attributes_values}

        self.category_actions_dict = OrderedDict({'actions': []})
        if _classe == 'kind' or _classe == 'mixin':
            category_actions_values = list()
            for __action in _category.actions:
                category_actions_values.append(__action.__repr__())
            self.category_actions_dict = {'actions': category_actions_values}

        result_json = OrderedDict(
            category_dict.items() + self.category_rel_dict.items() + self.category_location_dict.items() + self.category_attributes_dict.items() + self.category_actions_dict.items())
        result_dump = cStringIO.StringIO()
        json.dump(result_json, result_dump, indent=4 * ' ')
        logger.debug('category_serializer_to_json-serialization=' + result_dump.getvalue())
        return result_dump.getvalue()

    def from_json(self, json_doc):
        """

        method to convert from JSON to an object (OCCI object)

        """
        pass


# ======================================================================================
# OCCI Entity attributes serialization
# Rendering of OCCI Entity attributes
# ======================================================================================
class entity_serializer(object):
    """

    This class is used for the serialization of OCCI entity in JSON
    (Not needed until now ;-) )

    """

    def to_json(self, obj):
        """

        method to convert an object (OCCI object) to a JSON format

        """

    def from_json(self, json_doc):
        """

        method to convert from JSON to an object (OCCI object)

        """
        pass


# ======================================================================================
# OCCI Resource instance serialization
# Rendering of OCCI resource instance references
# ======================================================================================
class resource_serializer(object):
    """

    This class is used for the serialization of OCCI resource in JSON

    """

    def to_json(self, obj):
        """

        method to convert an object (OCCI object) to a JSON format

        """

        self.entity_dict = OrderedDict({'occi.core.id': obj.occi_core_id, 'occi.core.title': obj.occi_core_title})
        self.kind_dict = OrderedDict(
                {'kind': {'term': obj.kind.term, 'scheme': obj.kind.scheme, 'class': 'kind', 'title': obj.kind.title}})

        self.mixins_dict = OrderedDict({'mixins': []})
        mixins_values = list()
        for __mixin in obj.mixins:
            __mixin_class = category_registry().get_mixin(__mixin['scheme'] + "#" + __mixin['term'])
            mixins_values.append({'term': __mixin_class.term, 'scheme': __mixin_class.scheme, 'class': 'mixin',
                                  'title': __mixin_class.title})
        self.mixins_dict = {'mixins': mixins_values}

        self.resource_dict = OrderedDict({'occi.core.summary': obj.occi_core_summary})

        self.links_dict = OrderedDict({'links': []})
        links_values = list()
        for __link in obj.links:
            links_values.append(__link.__repr__())
        self.links_dict = {'links': links_values}

        self.attributes_dict = OrderedDict({'attributes': ''})
        attributes_values = OrderedDict()

        # to extract attributes defined directly by the Kind
        for __attribute in obj.kind.attributes:
            _a = obj.__getattribute__(re.sub('\.', '_', __attribute.name))
            _b = jsonpickle.encode(_a, unpicklable=False)
            attributes_values[str(__attribute.name)] = jsonpickle.decode(_b)

        # to extract attributes defined by the related Kinds
        for __kind_related in obj.kind.related:
            # to do (not urgent): attributes of the related kind of the related kind (recursively)
            # we use this if because tha main attributes of Resource and Link should be outside of Attributes bloc
            if __kind_related.__repr__() != Resource._kind.__repr__() and __kind_related.__repr__() != Link._kind.__repr__():
                for __attribute in  category_registry().get_kind(str(__kind_related)).attributes:
                    _a = obj.__getattribute__(re.sub('\.', '_', __attribute.name))
                    _b = jsonpickle.encode(_a, unpicklable=False)
                    attributes_values[str(__attribute.name)] = jsonpickle.decode(_b)

        # to extract attributes defined by the mixins and related mixins of each mixin
        for __mixin in obj.mixins:
            # for __attribute in __mixin.attributes:
            __mixin_class = category_registry().get_mixin(__mixin['scheme'] + "#" + __mixin['term'])
            for __attribute in __mixin_class.attributes:
                _cc = obj.__getattribute__(re.sub('\.', '_', __attribute.name))
                _d = jsonpickle.encode(_cc, unpicklable=False)
                attributes_values[str(__attribute.name)] = jsonpickle.decode(_d)
            for __mixin_related in __mixin_class.related:
                # to do (not urgent): attributes of the related mixin of the related mixin (recursively)
                for __attribute in category_registry().get_kind(str(__mixin_related)).attributes:
                    _e = obj.__getattribute__(re.sub('\.', '_', __attribute.name))
                    _f = jsonpickle.encode(_e, unpicklable=False)
                    attributes_values[str(__attribute.name)] = jsonpickle.decode(_f)

        self.attributes_dict = {'attributes': attributes_values}

        self.location_dict = OrderedDict({'location': location_registry().get_location(obj)})

        result_json = OrderedDict(
            self.entity_dict.items() + self.kind_dict.items() + self.mixins_dict.items() + self.resource_dict.items() + self.links_dict.items() + self.attributes_dict.items() + self.location_dict.items())
        result_dump = cStringIO.StringIO()
        json.dump(result_json, result_dump, indent=4 * ' ')

        logger.debug('resource_serialization_to_json=' + result_dump.getvalue())
        return result_dump.getvalue()

    def from_json(self, json_doc):
        """

        method to convert from JSON to an object (OCCI object)

        """

        result_obj = jsonpickle.decode(json_doc)

        _kind_term = result_obj['kind']['term']
        _kind_scheme = result_obj['kind']['scheme']
        _kind_class = result_obj['kind']['class']

        _occi_core_id = result_obj['occi.core.id']
        _occi_core_title = result_obj['occi.core.title']
        _occi_core_summary = result_obj['occi.core.summary']
        _mixins = result_obj['mixins']
        _links = result_obj['links']
        _attributes = result_obj['attributes']

        _kind = category_registry().get_kind(_kind_scheme + '#' + _kind_term)
        if  _kind is not None:
            _resource = Resource(occi_core_id=_occi_core_id, kind=_kind, occi_core_title=_occi_core_title,
                                 mixins=_mixins, occi_core_summary=_occi_core_summary, links=_links)

            # P.S. if the attribute value extracted from the json is a list type than use a boucle

            #  = 1 = pour tout les attributes du kind (ex attributs du kind compute), il faut ajouter les valeurs des attributs à resource
            for _attribute in _kind.attributes:
                _attribute_name = _attribute.name.replace('.', '_')
                # condition on the type of the attribute if it is based on a specific new class ('' means a standard type)
                if _attribute.type is '':
                    _resource.__dict__[_attribute_name] = _attributes[_attribute.name] or ''
                else:
                    # many elements
                    if str(_attribute.multiplicity).endswith('*'):
                        result_attribute = []
                        for a in _attributes[_attribute.name]:
                            # JUST EXAMPLE: fun = 'specification.ocni/specification.ocni.Availability(' + 'ocni_availability_start="' + str(t1) + '", ocni_availability_end="' + str(t2) + '")'
                            best_func = tools.classPath2modulePath(_attribute.type) + '/' + _attribute.type + '('
                            i = 0
                            for cle in a:
                                best_func += re.sub('\.', '_', str(cle)) + '="' + a[cle] + '"'
                                if i < len(a) - 1:
                                    best_func += ','
                                i += 1
                            best_func += ')'

                            obj = jsonpickle.unpickler.loadrepr(best_func)
                            result_attribute.append(obj)

                        _resource.__dict__[_attribute_name] = result_attribute
                        # just one element
                    else:
                        a = _attributes[_attribute.name]
                        best_func = tools.classPath2modulePath(_attribute.type) + '/' + _attribute.type + '('
                        i = 0
                        for cle in a:
                            best_func += re.sub('\.', '_', str(cle)) + '="' + a[cle] + '"'
                            if i < len(a) - 1:
                                best_func += ','
                            i += 1
                        best_func += ')'

                        obj = jsonpickle.unpickler.loadrepr(best_func)

                        _resource.__dict__[_attribute_name] = obj
                        pass
                    pass

                #_resource.__dict__.update(attribute_name)
                #_resource.attribute_name = lambda: None
                #setattr(_resource, attribute_name, 'attribute_name_value')
                #print getattr(_resource, attribute_name)

                logger.debug('the attribute to add:' + str(getattr(_resource, _attribute_name)))

            # = 2 = pour tout les mixins, et pour chaque mixin il faut: appliquer le mixin sur l'objet resource puis il faut ajouter les avaleurs des attributs du mixin à l'objet resource

            for _mixin in _mixins:
                _mixin_obj = category_registry().get_mixin(_mixin['scheme'] + '#' + _mixin['term'])
                if _mixin_obj is not None:
                    for _element in _mixin_obj.attributes:
                        _attribute_name = _element.name.replace('.', '_')
                        # condition on the type of the attribute if it is based on a specific new class ('' means a standard type)
                        if _element.type is '':
                            _resource.__dict__[_attribute_name] = _attributes[_element.name] or ''
                        else:
                            # many elements
                            if str(_element.multiplicity).endswith('*'):
                                result_element = []
                                for a in _attributes[_element.name]:
                                    # JUST EXAMPLE: fun = 'specification.ocni/specification.ocni.Availability(' + 'ocni_availability_start="' + str(t1) + '", ocni_availability_end="' + str(t2) + '")'
                                    best_func = tools.classPath2modulePath(_element.type) + '/' + _element.type + '('
                                    i = 0
                                    for cle in a:
                                        best_func += re.sub('\.', '_', str(cle)) + '="' + a[cle] + '"'
                                        if i < len(a) - 1:
                                            best_func += ','
                                        i += 1
                                    best_func += ')'

                                    obj = jsonpickle.unpickler.loadrepr(best_func)
                                    result_element.append(obj)

                                _resource.__dict__[_attribute_name] = result_element
                                # just one element
                            else:
                                a = _attributes[_element.name]
                                best_func = tools.classPath2modulePath(_element.type) + '/' + _element.type + '('
                                i = 0
                                for cle in a:
                                    best_func += re.sub('\.', '_', str(cle)) + '="' + a[cle] + '"'
                                    if i < len(a) - 1:
                                        best_func += ','
                                    i += 1
                                best_func += ')'

                                obj = jsonpickle.unpickler.loadrepr(best_func)

                                _resource.__dict__[_attribute_name] = obj
                                pass
                            pass
                            ## just as backup in case of a problem by replacing this block
                            #if _element.type is '':
                            #    _resource.__dict__[_attribute_name] = _attributes[_element.name] or ''
                            #else:
                            #    pass
                else:
                    logger.warning('trying to use an unregistered mixin')
                    return 'FAILED to add this resource because you want to use an unregistered mixin'
                pass

            return _resource

        else:
            logger.warning('trying to create a resource of an unregistered kind')
            return 'FAILED to add this resource'


# ======================================================================================
# OCCI Link instance serialization
# Rendering of OCCI Link instance references
# ======================================================================================
class link_serializer(object):
    """

    This class is used for the serialization of OCCI Link

    """

    def to_json(self, obj):
        """

        method to convert an object (OCCI object) to a JSON format

        """
        self.entity_dict = OrderedDict({'occi.core.id': obj.occi_core_id, 'occi.core.title': obj.occi_core_title})
        self.kind_dict = OrderedDict(
                {'kind': {'term': obj.kind.term, 'scheme': obj.kind.scheme, 'class': 'kind', 'title': obj.kind.title}})

        self.mixins_dict = OrderedDict({'mixins': []})
        mixins_values = list()
        for __mixin in obj.mixins:
            mixins_values.append(
                    {'term': __mixin.term, 'scheme': __mixin.scheme, 'class': 'mixin', 'title': __mixin.title})
        self.mixins_dict = {'mixins': mixins_values}

        self.attributes_dict = OrderedDict({'attributes': ''})
        attributes_values = OrderedDict()

        # to extract attributes defined directly by the Kind
        for __attribute in obj.kind.attributes:
            _a = obj.__getattribute__(re.sub('\.', '_', __attribute.name))
            _b = jsonpickle.encode(_a, unpicklable=False)
            attributes_values[str(__attribute.name)] = jsonpickle.decode(_b)

        # to extract attributes defined by the related Kinds
        for __kind_related in obj.kind.related:
            # to do (not urgent): attributes of the related kind of the related kind (recursively)
            # we use this if because tha main attributes of Resource and Link should be outside of Attributes bloc
            if __kind_related.__repr__() != Resource._kind.__repr__() and __kind_related.__repr__() != Link._kind.__repr__():
                for __attribute in  category_registry().get_kind(str(__kind_related)).attributes:
                    _a = obj.__getattribute__(re.sub('\.', '_', __attribute.name))
                    _b = jsonpickle.encode(_a, unpicklable=False)
                    attributes_values[str(__attribute.name)] = jsonpickle.decode(_b)

        # to extract attributes defined by the mixins and related mixins of each mixin
        for __mixin in obj.mixins:
            for __attribute in __mixin.attributes:
                _cc = obj.__getattribute__(re.sub('\.', '_', __attribute.name))
                _d = jsonpickle.encode(_cc, unpicklable=False)
                attributes_values[str(__attribute.name)] = jsonpickle.decode(_d)
            for __mixin_related in __mixin.related:
                # to do (not urgent): attributes of the related mixin of the related mixin (recursively)
                for __attribute in category_registry().get_kind(str(__mixin_related)).attributes:
                    _e = obj.__getattribute__(re.sub('\.', '_', __attribute.name))
                    _f = jsonpickle.encode(_e, unpicklable=False)
                    attributes_values[str(__attribute.name)] = jsonpickle.decode(_f)

        self.attributes_dict = {'attributes': attributes_values}

        self.link_dict = OrderedDict(
                {'occi.core.source': obj.occi_core_source, 'occi.core.target': obj.occi_core_target})

        self.location_dict = OrderedDict({'location': location_registry().get_location(obj)})

        result_json = OrderedDict(
            self.entity_dict.items() + self.kind_dict.items() + self.mixins_dict.items() + self.attributes_dict.items() + self.link_dict.items() + self.location_dict.items())
        result_dump = cStringIO.StringIO()
        json.dump(result_json, result_dump, indent=4 * ' ')

        logger.debug('link_serialization_to_json=' + result_dump.getvalue())
        return result_dump.getvalue()

    def from_json(self, json_doc):
        """

        method to convert from JSON to an object (OCCI object)

        """
        pass


# ======================================================================================
# OCCI action instance serialization
# Rendering of references to OCCI Action instances
# ======================================================================================
class action_serializer(object):
    """

    This class is used for the serialization of OCCI action

    """

    def to_json(self, obj):
        """

        method to convert an object (OCCI object) to a JSON format

        """

    def from_json(self, json_doc):
        """

        method to convert from JSON to an object (OCCI object)

        """
        pass


# ======================================================================================
# OCCI Location-URIs serialization
# Rendering of Location-URIs
# ======================================================================================
class location_uri_serializer(object):
    """

    This class is used for the serialization of OCCI Location-URIs

    """

    def to_json(self, obj):
        """

        method to convert an object (OCCI object) to a JSON format

        """
        pass


# ======================================================================================
# # OCCI main serialization
# ======================================================================================
class main_serializer(object):
    pass


class test1(object):
    def __init__(self, start='start', end='end'):
        # start = datetime(year=2010, month=11, day=1, hour=14, minute=40, second=0)
        self.start = start
        self.end = end

    pass


class test2(object):
    def __init__(self, a=None, b=None):
        # start = datetime(year=2010, month=11, day=1, hour=14, minute=40, second=0)
        self.a = a or test1()
        #self.b = b or (test1(),)

    pass


# ======================================================================================
# main
# ======================================================================================
if __name__ == '__main__':
    # ======================================================================================
    # Needed import for registration of entities to the registries
    # ======================================================================================
    from specification.occi_infrastructure import Compute, Network, Storage, NetworkInterface, StorageLink, IPNetworking, IPNetworkInterface

    # ======================================================================================
    # the category registry
    # ======================================================================================

    # register OCCI Core kinds
    category_registry().register_kind(Entity._kind)
    category_registry().register_kind(Resource._kind)
    category_registry().register_kind(Link._kind)

    # register OCCI Infrastructure kinds
    category_registry().register_kind(Compute._kind)
    category_registry().register_kind(Network._kind)
    category_registry().register_kind(Storage._kind)
    category_registry().register_kind(NetworkInterface._kind)
    category_registry().register_kind(StorageLink._kind)

    # register OCCI Infrastructure mixins
    category_registry().register_mixin(IPNetworking())
    category_registry().register_mixin(IPNetworkInterface())

    # ======================================================================================
    # the location registry
    # ======================================================================================

    # register OCCI Core kind locations
    location_registry().register_location("/resource/", Resource._kind)
    location_registry().register_location("/link/", Link._kind)

    # register OCCI Infrastructure kind locations
    location_registry().register_location("/compute/", Compute._kind)
    location_registry().register_location("/network/", Network._kind)
    location_registry().register_location("/storage/", Storage._kind)
    location_registry().register_location("/networkinterface/", NetworkInterface._kind)
    location_registry().register_location("/storagelink/", StorageLink._kind)

    # register OCCI Infrastructure mixin locations
    location_registry().register_location("/ipnetworking/", IPNetworking())
    location_registry().register_location("/ipnetworkinterface/", IPNetworkInterface())

    #################### To test category_serializer to_json function #################################################
    #ser = category_serializer()

    #ser.to_json(Compute._kind)

    #b = IPNetworkInterface()
    #ser.to_json(b)
    ###################################################################################################################

    #################### To test resource_serializer to_json function #################################################
    network_instance = Network('/network/123', 'active', occi_core_summary='the summary of the network instance')
    location_registry().register_location("/network/123", network_instance)

    category_registry().register_mixin(IPNetworking())
    network_instance.mixins.append(IPNetworking())
    #network_instance.mixins.append(IPNetworking())
    mixin_tools.mixIn(network_instance, IPNetworking())

    network_interface_instance = NetworkInterface('NIC1', network_instance.__repr__(), network_instance.__repr__(),
                                                  'networkInterface',
                                                  'mac@', 'active')
    location_registry().register_location("/networkinterface/456", network_interface_instance)
    network_instance.links.append(network_interface_instance.__repr__())
    #network_instance.links.append(network_interface_instance.__repr__())

    print network_instance.__dict__

    resource_serializer_instance = resource_serializer()
    resource_serializer_instance.to_json(network_instance)

    from pyocni.specification.ocni import CloNeNode

    CloNeNode_instance = CloNeNode('CloNeNodeID', 'active')
    location_registry().register_location("/CloNeNode/CloNeNodeID", CloNeNode_instance)

    resource_serializer_instance.to_json(CloNeNode_instance)
    ###################################################################################################################

    #################### To test link_serializer to_json function #####################################################
    link_serializer_instance = link_serializer()
    link_serializer_instance.to_json(network_interface_instance)
    ###################################################################################################################

    pass

    print 'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz begin zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz'

    #aa = str('{"availability":[{ "start":"08:00", "end":"12:00"  },  { "start":"14:00", "end":"18:00" } ]}')
    aa = str('[{ "start":"08:00", "end":"12:00"  },  { "start":"14:00", "end":"18:00" } ]')

    cla = jsonpickle.unpickler.loadclass('specification.ocni.Availability')
    start = "'08:00'"
    end = '"12:00"'
    jsonobj = jsonpickle.encode('{"ocni.availability.start":"08:00", "ocni.availability.end":"12:00" } ')
    print jsonobj
    #obj = jsonpickle.unpickler.loadrepr('specification.ocni/specification.ocni.AvailabilityInterval(' + start + ',' + end +')')
    print cla.__module__
    print cla.__name__
    print cla.__dict__

    ob = cla('dateTime1', 'dateTime2')
    print type(ob)
    print ob
    print ob.__dict__

    obj = jsonpickle.unpickler.loadrepr(
        'specification.ocni/specification.ocni.Availability(' + start + ',' + end + ')')
    print type(obj)
    print str(obj.ocni_availability_start)
    print str(obj.ocni_availability_end)
    unpickled = jsonpickle.decode(aa)
    print type(unpickled)
    print str(unpickled)

    print 'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz end zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz'

    oaa = test2()

    c = jsonpickle.unpickler.loadclass('serialization.serializer_json.Availability')
    jsonobj = jsonpickle.decode('{"a": {"start":"s", "end":"e"} }')
    print type(jsonobj)
    print jsonobj

    res = json.loads('{"a": {"start":"s", "end":"e"} }')
    print type(res)
    print res

# To Do =
# Raise error if object is not the same of the serialization object
#if  isinstance(obj, Resource):
#            logger.warning("Object bad type: Only a kind, mixin or an action can be rendered as a category")
#            raise Exception("Object bad type: Only a kind, mixin or an action can be rendered as a category")
