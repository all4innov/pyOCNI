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
Created on Jun 20, 2011

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@license: Apache License, Version 2.0
"""

import pyocni.pyocni_tools.config as config
# getting the Logger
logger = config.logger

def update_kind_provider(old_provider,new_provider):
    """
    Update only a part of the provider description
    Args:
        @param old_provider: The old provider description
        @param new_provider: The new provider description
        @return : Updated data and a boolean (false if all fields are updated, true if there were some un-updated fields)
    """

    #Try to get the keys from occi description dictionary
    oldData_keys = old_provider.keys()
    newData_keys = new_provider.keys()
    for key in newData_keys:
        try:
            oldData_keys.index(key)
            old_provider[key] = new_provider[key]
        except Exception:
            #Keep the record of the keys(=parts) that couldn't be updated
            logger.debug("update description : " + key + " could not be found")
            return None,True

    return old_provider,False
