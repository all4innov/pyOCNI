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
Created on Feb 25, 2011

@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@version: 0.3
@license: LGPL - Lesser General Public License
"""
#====================================================================
# OCCI Core version 1.1
#====================================================================

import persistent

class Attribute(object):
    """

    The attribute type used for the attributes list of category

    """

    def __init__(self, name, type='', required=False, multiplicity='', mutable=False, description=''):
        # the attribute name
        self.name = name

        # type of the attribute (string, URI, IPv4 or another complexType
        self.type = type

        # True if the attribute is required else False
        self.required = required

        # The multiplicity of this attributes (1, *, 0..1, 0..*, 1..*)
        self.multiplicity = multiplicity

        # True if the attribute is mutable else False
        self.mutable = mutable

        # A small description of the attribute
        self.description = description


class Category(persistent.Persistent):
    """

    The Category type is the basis of the type identification mechanism used by the OCCI classification system.

    """

    def __init__(self, term, scheme, title='', attributes=()):
        # Unique identifier of the category instance within the categorisation scheme
        # @AttributeType string
        # @AttributeMultiplicity 1
        # @AttributeMutability immutable
        self.term = term

        # The categorisation scheme
        # @AttributeType URI
        # @AttributeMultiplicity 1
        # @AttributeMutability immutable
        self.scheme = scheme

        # The display name of an instance
        # @AttributeType string
        # @AttributeMultiplicity 0..1
        # @AttributeMutability immutable
        self.title = title

        # The set of resource attribute names defined by the category instance
        # @AttributeType string
        # @AttributeMultiplicity 0..*
        # @AttributeMutability immutable
        self.attributes = attributes

    def __repr__(self):
        return  self.scheme + "#" + self.term


class Kind(Category):
    """

    The kind type, together with the Mixin type, defines the classification system of the OCCI Core Model.
    The Kind type represents the type identification mechanism for all Entity types present in the model.

    """

    def __init__(self, term, scheme, entity_type, title='', attributes=(), actions=(), related=(), entities=()):
        super(Kind, self).__init__(term=term,
                                   scheme=scheme,
                                   title=title,
                                   attributes=attributes)
        # set of actions defined by the Kind instance
        # @AttributeType Action
        # @AttributeMultiplicity 0..*
        # @AttributeMutability immutable
        self.actions = actions

        # set of related Kind instances
        # @AttributeType Kind
        # @AttributeMultiplicity 0..*
        # @AttributeMutability immutable
        self.related = related

        # Entity type uniquely identified by the Kind instance
        # @AttributeType Entity
        # @AttributeMultiplicity 1
        # @AttributeMutability immutable
        self.entity_type = entity_type

        # set of resource instances, i.e. Entity sub-type instances.
        # Resources instantiated from the Entity sub-type which is uniquely identified by this Kind instance.
        # @AttributeType Entity
        # @AttributeMultiplicity 0..*
        # @AttributeMutability immutable
        self.entities = entities


class Mixin(Category):
    """

    The Mixin type complements the Kind type in defining the OCCI Core Model type classification system.
    The Mixin type represent an extension mechanism, which allows new resource capabilities to be added
        to resource instances both at creation-time and/or run-time.
    A Mixin instance can be associated with any existing resource instance and thereby add new resource
        capabilities, i.e. attributes and Actions, to the resource instance. However, a Mixin can never
        be applied to a type.

    """

    def __init__(self, term, scheme, title='', attributes=(), actions=(), related=(), entities=[]):
        super(Mixin, self).__init__(term=term,
                                    scheme=scheme,
                                    title=title,
                                    attributes=attributes)
        # set of actions defined by the Mixin instance
        # @AttributeType Action
        # @AttributeMultiplicity 0..*
        # @AttributeMutability immutable
        self.actions = actions or []

        # set of related Mixin instances
        # @AttributeType Mixin
        # @AttributeMultiplicity 0..*
        # @AttributeMutability immutable
        self.related = related or []

        # set of resource instances, i.e. Entity sub-type instances, associated with the Mixin instance.
        # @AttributeType Entity
        # @AttributeMultiplicity 0..*
        # @AttributeMutability mutable
        self.entities = entities or []


class Action(persistent.Persistent):
    """

    The Action type is an abstract type. Each sub-type of Action defines an invocable
        operation applicable to an Entity sub-type instance or a collection thereof.

    """

    # The category instance assigned to the action type
    __category_instance = Category(term='action',
                                   scheme='http://schemas.ogf.org/occi/core',
                                   title='Action',
                                   attributes=())

    def __init__(self, category=__category_instance):
        # The identifying Category of the Action
        # @AttributeType Category
        # @AttributeMultiplicity 1
        # @AttributeMutability immutable
        self.category = category

    # __repr__ is also the unique id of Category
    def __repr__(self):
        return  self.category.scheme + '#' + self.category.term


class Entity(persistent.Persistent):
    """

    The Entity type is an abstract type of the Resource type and the Link type.

    """

    # The kind instance assigned to the entity type
    _kind = Kind(term='entity',
                 scheme='http://schemas.ogf.org/occi/core',
                 entity_type='',
                 title='Entity type',
                 attributes=(Attribute(name='occi.core.id', type='URI', required=True),
                             Attribute(name='occi.core.title', mutable=True)),
                 actions=(),
                 related=(),
                 entities=())

    def __init__(self, occi_core_id, kind=_kind, occi_core_title='', mixins=[]):
        # A unique identifier (within the service provider's name-space) of the Entity sub-type instance.
        # occi.core.id
        # @AttributeType URI
        # @AttributeMultiplicity 1
        # @AttributeMutability immutable
        self.occi_core_id = occi_core_id

        # The display name of the instance.
        # occi.core.title
        # @AttributeType string
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.occi_core_title = occi_core_title

        # The Kind instance uniquely identifying the Entity sub-type of the resource instance.
        # @AttributeType Kind
        # @AttributeMultiplicity 1
        # @AttributeMutability immutable
        self.kind = kind

        # The Mixin instances associated to this resource instance.
        # Consumers can expect the attributes and Actions of the associated Mixins to be exposed byt the instance.
        # @AttributeType Kind
        # @AttributeMultiplicity 0..*
        # @AttributeMutability mutable
        self.mixins = mixins

    # __repr__ is also the unique id of Entity
    def __repr__(self):
        return self.occi_core_id


class Resource(Entity):
    """

    The resource type inherits Entity and describes a concrete resource that can be inspired and manipulated.
    A resource is suitable to represent real world resources, e.g. virtual machines, networks, services , etc.
        through specialisation

    """

    # The kind instance assigned to the resource type
    _kind = Kind(term='resource',
                 scheme='http://schemas.ogf.org/occi/core',
                 entity_type='',
                 title='Resource',
                 attributes=(Attribute(name='occi.core.summary', mutable=True), ),
                 actions=(),
                 related=(Entity._kind, ),
                 entities=())

    def __init__(self, occi_core_id, kind=_kind, occi_core_title='', mixins=[], occi_core_summary='', links=[]):
        super(Resource, self).__init__(occi_core_id=occi_core_id,
                                       kind=kind,
                                       occi_core_title=occi_core_title,
                                       mixins=mixins)
        # A summarising description of the Resource instance
        # occi.core.summary
        # @AttributeType string
        # @AttributeMultiplicity 0..1
        # @AttributeMutability mutable
        self.occi_core_summary = occi_core_summary or ''

        # A set of Link compositions.
        # @AttributeType Link
        # @AttributeMultiplicity 0..*
        # @AttributeMutability mutable
        self.links = links or []


class Link(Entity):
    """

    An instance of the Link type defines a base association between two Resource instances.
    A Link instance indicates that one Resource instance is connected to another.

    """

    # The kind instance assigned to the link type
    _kind = Kind(term='link',
                 scheme='http://schemas.ogf.org/occi/core',
                 entity_type='',
                 title='Link',
                 attributes=(Attribute(name='occi.core.source', required=True, mutable=True),
                             Attribute(name='occi.core.target', required=True, mutable=True)),
                 actions=(),
                 related=(Entity._kind, ),
                 entities=())

    def __init__(self, occi_core_id, occi_core_source, occi_core_target, kind=_kind, occi_core_title='', mixins=[]):
        super(Link, self).__init__(occi_core_id=occi_core_id,
                                   kind=kind,
                                   occi_core_title=occi_core_title,
                                   mixins=mixins)
        # The Resource instances the Link instance originates from.
        # occi.core.source
        # @AttributeType Resource
        # @AttributeMultiplicity 1
        # @AttributeMutability mutable
        self.occi_core_source = occi_core_source

        # The Resource instances the Link instance points to.
        # occi.core.target
        # @AttributeType Resource
        # @AttributeMultiplicity 1
        # @AttributeMutability mutable
        self.occi_core_target = occi_core_target


if __name__ == '__main__':
    pass
