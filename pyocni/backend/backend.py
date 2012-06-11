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
import commands

# getting the Logger
logger = config.logger



class backend(object):
    '''

    A simple and empty backend

    '''

    local_identifier = 'a'

    def create(self, entity):
        '''

        Create an entity (Resource or Link)

        '''
        logger.debug('The create operation is not implemented yet')

    def read(self, entity):
        '''

        Get the Entity's information

        '''
        logger.debug('The read operation is not implemented yet')

    def update(self, old_entity, new_entity):
        '''

        Update an Entity's information

        '''
        logger.debug('The update operation is not implemented yet')

    def delete(self, entity):
        '''

        Delete an Entity

        '''
        logger.debug('The delete operation is not implemented yet')

    def action(self, entity, action):
        '''

        Perform an action on an Entity

        '''
        logger.debug('The Entity\'s action operation is not implemented yet')


if __name__ == '__main__':
    pass
