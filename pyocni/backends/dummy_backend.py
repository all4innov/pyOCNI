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
Created on Nov 10, 2011

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@license: Apache License, Version 2.0
"""

#import pyocni.backend.backend as backend
from pyocni.backends.backend import backend_interface
import pyocni.pyocni_tools.config as config
# getting the Logger
logger = config.logger

class backend(backend_interface):

    def create(self, entity):
        '''

        Create an entity (Resource or Link)

        '''

        logger.debug('***The create operation of the dummy_backend***')

    def read(self, entity):
        '''

        Get the Entity's information

        '''
        logger.debug('***The read operation of the dummy_backend***')

    def update(self, old_entity, new_entity):
        '''

        Update an Entity's information

        '''
        logger.debug('***The update operation of the dummy_backend***')

    def delete(self, entity):
        '''

        Delete an Entity

        '''
        logger.debug('***The delete operation of the dummy_backend***')

    def action(self, entity, action, attributes):
        '''

        Perform an action on an Entity

        '''
        logger.debug('***The Entity\'s action operation of the dummy_backend***')
