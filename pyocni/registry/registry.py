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

import pyocni.pyocni_tools.ocni_exceptions as ocni_exceptions
import pyocni.pyocni_tools.config as config

from pyocni.specification.occi_core import Category, Kind, Mixin, Action, Entity, Resource, Link

from ZODB.FileStorage import FileStorage
from ZODB.DB import DB
import transaction

# getting the Logger
logger = config.logger

# ======================================================================================
# Location registry
# ======================================================================================
class location_registry(object):
    """

    A registry containing all the locations and objects

    """

    # ======== locations[object_id] = location =============
    storage_locations = FileStorage('locations.fs')
    db_locations = DB(storage_locations)
    connection_locations = db_locations.open()
    locations = connection_locations.root()


    # ======== objects[location] = object ==================
    storage_objects = FileStorage('objects.fs')
    db_objects = DB(storage_objects)
    connection_objects = db_objects.open()
    objects = connection_objects.root()

    def __init__(self):
        pass

    def register_location(self, location, object):
        if  object.__repr__() in location_registry.locations:
            logger.warning('the location \'' + str(location) + '\' is already registered')
            try:
                raise ocni_exceptions.AlreadyRegistered('the location \'' + str(location) + '\' is already registered')
            except Exception:
                pass
                #raise ocni_exceptions.AlreadyRegistered('the location \'' + str(location) + '\' is already registered')
            else:
                pass

        elif location in location_registry.objects:
            logger.warning('the object \'' + str(object) + '\' is already registered')
            try:
                raise ocni_exceptions.AlreadyRegistered('the object \'' + str(object) + '\' is already registered')
            except Exception:
                pass
                #raise ocni_exceptions.AlreadyRegistered('the object \'' + str(object) + '\' is already registered')
            else :
                pass

        else:
            logger.debug("Registering the location \'" + location + "\' to the object \'" + object.__repr__() + "\'")
            location_registry.locations[object.__repr__()] = location
            location_registry.objects[location] = object
            transaction.commit()

    def unregister_location(self, location):
        if location in location_registry.objects:
            logger.debug("Un-registering the location \'" + str(location) + "\'")
            del location_registry.locations[location_registry.objects[location].__repr__()]
            del location_registry.objects[location]
            transaction.commit()
        else:
            logger.warning("The location \'" + str(location) + "\'" + " is not registered")

    def get_location(self, object):
        try:
            return location_registry.locations.get(object.__repr__())
        except Exception:
            return None

    def get_object(self, location):
        try:
            return location_registry.objects.get(location)
        except Exception:
            return None

    def get_object_under_location(self, location_path):
        _objects = []
        try:
            for _location in location_registry().objects:
                if _location.startswith(location_path):
                    _objects.append(location_registry.objects[_location])
            return _objects
        except Exception:
            return None

    def get_locations_under_path(self, path):
        _locations = []
        try:
            for _location in location_registry().locations.values():
                if _location.startswith(path):
                    _locations.append(_location)
            return _locations
        except Exception:
            return None
        pass

    def purge_locations_db(self):
        location_registry.locations.clear()
        transaction.commit()

    def purge_objects_db(self):
        location_registry.objects.clear()
        transaction.commit()

    def close_locations_db(self):
        self.connection_locations.close()
        self.db_locations.close()
        self.storage_locations.close()

    def close_objects_db(self):
        self.connection_objects.close()
        self.db_objects.close()
        self.storage_objects.close()


# ======================================================================================
# Location registry (old) with no persistent storage through ZODB (deprecated)
# ======================================================================================
class location_registry_old(object):
    """

    A registry containing all the locations and objects

    """

    # locations[object_id] = location
    locations = {}

    # objects[location] = object
    objects = {}

    def __init__(self):
        pass

    def register_location(self, location, object):
        if  object.__repr__() in location_registry.locations:
            logger.warning('the location \'' + location + '\' is already registered')
            raise ocni_exceptions.AlreadyRegistered('the location \'' + location + '\' is already registered')
        elif location in location_registry.objects:
            logger.warning('the object \'' + object + '\' is already registered')
            raise ocni_exceptions.AlreadyRegistered('the object \'' + object + '\' is already registered')
        else:
            logger.debug("Registering the location \'" + location + "\' to the object \'" + object.__repr__() + "\'")
            location_registry.locations[object.__repr__()] = location
            location_registry.objects[location] = object

    def unregister_location(self, location):
        if location in location_registry.objects:
            logger.debug("Un-registering the location \'" + location + "\'")
            del location_registry.locations[location_registry.objects[location].__repr__()]
            del location_registry.objects[location]
        else:
            logger.warning("The location \'" + location + "\'" + " is not registered")

    def get_location(self, object):
        try:
            return location_registry.locations.get(object.__repr__())
        except Exception:
            return None

    def get_object(self, location):
        try:
            return location_registry.objects.get(location)
        except Exception:
            return None

    def get_object_under_location(self, location_path):
        _objects = []
        try:
            for _location in location_registry().objects:
                if _location.startswith(location_path):
                    _objects.append(location_registry.objects[_location])
            return _objects
        except Exception:
            return None

    def get_locations_under_path(self, path):
        _locations = []
        try:
            for _location in location_registry().locations.values():
                if _location.startswith(path):
                    _locations.append(_location)
            return _locations
        except Exception:
            return None
        pass


# ======================================================================================
# category registry
# ======================================================================================
class category_registry(object):
    """

    A registry containing all the Kinds, Mixins and actions

    """

    # A dictionary of all kinds
    kinds = {}
    # A dictionary of all mixins
    mixins = {}
    # A dictionary of all actions
    actions = {}

    def __init__(self):
        #       self.register_kind(Entity._kind)
        #        self.register_kind(Resource._resource_kind)
        #        self.register_kind(Link._kind)
        #
        #        self.register_kind(Compute._kind)
        #        self.register_kind(Network._kind)
        #        self.register_kind(Storage._kind)
        #        self.register_kind(Network_interface._kind)
        #        self.register_kind(Storage_link._kind)
        #
        #        self.register_mixin(ip_networking())
        #        self.register_mixin(ip_network_interface())
        pass

    def register_kind(self, _kind):
        logger.debug("Registering the kind: " + _kind.__repr__())
        if isinstance(_kind, Kind):
            category_registry.kinds[_kind.__repr__()] = _kind
            for _action in _kind.actions:
                self.register_action(_action)
        else:
            logger.warning("Cannot register the category: bad type")

    def register_mixin(self, _mixin):
        logger.debug("Registering the mixin: " + _mixin.__repr__())
        if isinstance(_mixin, Mixin):
            category_registry.mixins[_mixin.__repr__()] = _mixin
            for _action in _mixin.actions:
                self.register_action(_action)
        else:
            logger.warning("Cannot register the category: bad type")

    def register_action(self, _action):
        logger.debug("Registering the action: " + _action.__repr__())
        category_registry.actions[_action.category.__repr__()] = _action

    def unregister_kind(self, _kind):
        logger.debug("Un-registering the kind: " + _kind.__repr__())
        del category_registry.kinds[_kind.__repr__()]

    def unregister_mixin(self, _mixin):
        logger.debug("Un-registering the mixin: " + _mixin.__repr__())
        del category_registry.mixins[_mixin.__repr__()]

    def unregister_action(self, _action):
        logger.debug("Un-registering the action: " + _action.__repr__())
        del category_registry.actions[_action.__repr__()]

    def get_kind(self, kind_id):
        try:
            return category_registry.kinds[kind_id]
        except Exception:
            return None

    def get_mixin(self, mixin_id):
        try:
            return category_registry.mixins[mixin_id]
        except Exception:
            return None

    def get_action(self, action_id):
        try:
            return category_registry.actions[action_id]
        except Exception:
            return None

    def get_category(self, category_id):
        try:
            return category_registry.kinds.get(category_id) or category_registry.mixins.get(category_id)
        except Exception:
            return None

    def get_kinds(self):
        try:
            return category_registry.kinds
        except Exception:
            return None

    def get_mixins(self):
        try:
            return category_registry.mixins
        except Exception:
            return None

    def get_actions(self):
        try:
            return category_registry.actions
        except Exception:
            return None

            # only items !!!
            #def get_categories(self):
            #    try:
            #       return dict(category_registry.kinds.items() + category_registry.mixins.items())
            #   except:
            #        return None


# ======================================================================================
# backend registry                     (To do)
# ======================================================================================
class backend_registry():
    """

    A registry containing all the backends

    """
    backends = {}

    def register_backend(self, _backend):
        if  _backend.__repr__() in backend_registry.backends:
            logger.warning('the backend: \'' + _backend.__repr__() + '\' is already registered')
            raise ('the backend \'' + _backend.__repr__() + '\' is already registered')
        else:
            logger.debug("Registering the backend: " + _backend.__repr__())
            backend_registry.backends[_backend.__repr__()] = _backend

    def unregister_backend(self):
        pass

    def get_backend(self):
        pass

    def get_backends(self):
        try:
            return backend_registry().backends
        except Exception:
            return None


# ======================================================================================
# rendering registry                     (To do)
# ======================================================================================
class serialization_registry():
    """

    A registry containing all the serializers

    """
    serializers = {}

    def register_serializer(self):
        pass

    def unregister_serializer(self):
        pass

    def get_serializer(self):
        pass

# ======================================================================================
# main
# ======================================================================================

if __name__ == '__main__':
    #ca = category_registry()
    #print ca.kinds
    #print ca.mixins
    #print ca.actions
    #print ca.get_categories()
    path = "/-/"
    loc = path.lstrip('/')
    print loc
    print not loc
    pass
