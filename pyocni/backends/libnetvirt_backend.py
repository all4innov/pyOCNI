# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

# Copyright (C) 2011 Daniel Turull - KTH Royal Institute of Technology
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
Created on 10 Nov, 2011

@author: Daniel Turull
@contact: danieltt@kth.se
@organization: KTH Royal Institute of Technology
@version: 0.1
@license: LGPL - Lesser General Public License
"""

#import pyocni.backend.backend as backend
from pyocni.backends.backend import backend
import pyocni.pyocni_tools.config as config
# getting the Logger
logger = config.logger
try:
    import pyocni.backends.libnetvirt
except ImportError:
    logger.error("Libnetvirt not present. Add libnetvirt library to enable this backend")

class libnetvirt_backend(backend):
    def ep_check(self, ep):
        '''
        
        Check that the endpoint has the correct data format and fix it if necessary
        
        '''
        if ep.ocni_libnetvirt_endpoint_vlan == '':
            ep.ocni_libnetvirt_endpoint_vlan = 0xffff
        if ep.ocni_libnetvirt_endpoint_mpls == '':
            ep.ocni_libnetvirt_endpoint_mpls = 0
        if ep.ocni_libnetvirt_endpoint_port == '':
            ep.ocni_libnetvirt_endpoint_port = 0
        if ep.ocni_libnetvirt_endpoint_swid == '':
            ep.ocni_libnetvirt_endpoint_swid = 0

        return ep

    def diff(self, endpoints_old, endpoints_new):
        '''
        
        Return the list of nodes to add and remove
        
        '''
        e1 = set(endpoints_old)
        e2 = set(endpoints_new)
        inter = e1.intersection(e2)
        add = e2.difference(inter)
        rem = e1.difference(inter)

        return add, rem

    def create(self, entity):
        '''

        Create an entity (Resource or Link)

        '''
        logger.debug('The create operation of the libnetvirt_backend')

        # Check if the mixin is libnetvirt
        if str(entity.mixins[0]['term']) != 'libnetvirt':
            return

        # Initialize and connect libnetvirt
        info = libnetvirt.libnetvirt_init(libnetvirt.DRIVER_OF_NOX)
        con = libnetvirt.libnetvirt_connect(info,
            entity.ocni_libnetvirt_of_controller,
            int(entity.ocni_libnetvirt_of_controller_port))

        if con < 0:
            logger.error('Error while connecting to libnetvirt driver')
            return

        # Create FNS
        fns = libnetvirt.create_local_fns(int(entity.ocni_libnetvirt_uuid),
            len(entity.ocni_libnetvirt_endpoint),
            entity.occi_core_id)
        # Loop with all the endpoints
        index = 0
        for ep in entity.ocni_libnetvirt_endpoint:
            ep = self.ep_check(ep)

            libnetvirt.add_local_epoint(fns, index,
                long(ep.ocni_libnetvirt_endpoint_uuid),
                int(ep.ocni_libnetvirt_endpoint_swid),
                int(ep.ocni_libnetvirt_endpoint_port),
                int(ep.ocni_libnetvirt_endpoint_vlan),
                int(ep.ocni_libnetvirt_endpoint_mpls))
            index = index + 1

        # Send command
        libnetvirt.libnetvirt_create_fns(info, fns)

        # Stop communication        
        libnetvirt.libnetvirt_stop(info)


    def read(self, entity):
        '''

        Get the Entity's information

        '''
        logger.debug('The read operation of the libnetvirt_backend')

    def update(self, old_entity, new_entity):
        '''

        Update an Entity's information

        '''
        logger.debug('The update operation of the libnetvirt_backend')

        if old_entity == None:
            self.create(new_entity)
            return

        # Find the difference
        ep_add, ep_rem = self.diff(old_entity.ocni_libnetvirt_endpoint,
            new_entity.ocni_libnetvirt_endpoint)

        #ep_rem = self.diff(new_entity.ocni_libnetvirt_endpoint,
        #             old_entity.ocni_libnetvirt_endpoint)


        # Nothing to be change
        if len(ep_add) == 0 and len(ep_rem) == 0:
            return

        # Initialize and connect libnetvirt
        info = libnetvirt.libnetvirt_init(libnetvirt.DRIVER_OF_NOX)
        con = libnetvirt.libnetvirt_connect(info,
            new_entity.ocni_libnetvirt_of_controller,
            int(new_entity.ocni_libnetvirt_of_controller_port))

        if con < 0:
            logger.error('Error while connecting to libnetvirt driver')
            return

        if len(ep_add) > 0:
            # Modify add
            logger.debug('Adding endpoint to FNS')
            logger.debug(ep_add)
            fns = libnetvirt.create_local_fns(int(new_entity.ocni_libnetvirt_uuid),
                len(ep_add),
                new_entity.occi_core_id)
            # Loop with all the endpoints
            index = 0
            for ep in ep_add:
                ep = self.ep_check(ep)

                libnetvirt.add_local_epoint(fns, index,
                    long(ep.ocni_libnetvirt_endpoint_uuid),
                    int(ep.ocni_libnetvirt_endpoint_swid),
                    int(ep.ocni_libnetvirt_endpoint_port),
                    int(ep.ocni_libnetvirt_endpoint_vlan),
                    int(ep.ocni_libnetvirt_endpoint_mpls))
                index = index + 1

            libnetvirt.libnetvirt_modify_fns_add(info, fns);

        if len(ep_rem) > 0:
            # Modify remove
            logger.debug('Removing endpoints to FNS')
            logger.debug(ep_rem)
            fns = libnetvirt.create_local_fns(int(new_entity.ocni_libnetvirt_uuid),
                len(ep_rem),
                new_entity.occi_core_id)
            # Loop with all the endpoints
            index = 0
            for ep in ep_rem:
                ep = self.ep_check(ep)

                libnetvirt.add_local_epoint(fns, index,
                    long(ep.ocni_libnetvirt_endpoint_uuid),
                    int(ep.ocni_libnetvirt_endpoint_swid),
                    int(ep.ocni_libnetvirt_endpoint_port),
                    int(ep.ocni_libnetvirt_endpoint_vlan),
                    int(ep.ocni_libnetvirt_endpoint_mpls))
                index = index + 1

            libnetvirt.libnetvirt_modify_fns_del(info, fns);


        # Stop communication        
        libnetvirt.libnetvirt_stop(info)

    def delete(self, entity):
        '''

        Delete an Entity

        '''
        logger.debug('The delete operation of the libnetvirt_backend')
        # Check if the mixin is libnetvirt
        if entity == None:
            logger.error('Error. Entity is none')
            return
        if str(entity.mixins[0]['term']) != 'libnetvirt':
            logger.error('Entity is not libnetvirt mixin')
            return

        # Initialize and connect libnetvirt
        info = libnetvirt.libnetvirt_init(libnetvirt.DRIVER_OF_NOX)
        con = libnetvirt.libnetvirt_connect(info,
            entity.ocni_libnetvirt_of_controller,
            int(entity.ocni_libnetvirt_of_controller_port))

        if con < 0:
            logger.error('Error while connecting to libnetvirt driver')
            return

        fns = libnetvirt.create_local_fns(int(entity.ocni_libnetvirt_uuid),
            0,
            entity.occi_core_id)

        # Send command
        libnetvirt.libnetvirt_remove_fns(info, fns);
        logger.debug('Removing fns sent')
        # Stop communication        
        libnetvirt.libnetvirt_stop(info)


    def action(self, entity, action):
        '''

        Perform an action on an Entity

        '''
        logger.debug('The Entity\'s action operation of the libnetvirt_backend')
