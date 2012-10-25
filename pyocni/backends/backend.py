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
Created on Feb 25, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@license: Apache License, Version 2.0
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
