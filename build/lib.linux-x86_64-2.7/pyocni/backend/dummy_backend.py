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
Created on 10 Nov, 2011

@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Telecom - Telecom SudParis
@version: 0.1
@license: LGPL - Lesser General Public License
"""

#import pyocni.backend.backend as backend
from pyocni.backend.backend import backend
import pyocni.pyocni_tools.config as config
# getting the Logger
logger = config.logger

class dummy_backend(backend):
    def create(self, entity):
        '''

        Create an entity (Resource or Link)

        '''
        logger.debug('The create operation of the dummy_backend')
        logger.debug('bilel')

    def read(self, entity):
        '''

        Get the Entity's information

        '''
        logger.debug('The read operation of the dummy_backend')

    def update(self, old_entity, new_entity):
        '''

        Update an Entity's information

        '''
        logger.debug('The update operation of the dummy_backend')

    def delete(self, entity):
        '''

        Delete an Entity

        '''
        logger.debug('The delete operation of the dummy_backend')

    def action(self, entity, action):
        '''

        Perform an action on an Entity

        '''
        logger.debug('The Entity\'s action operation of the dummy_backend')
