# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

# Copyright (C) 2012 Bilel Msekni - Institut Mines-Telecom
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
Created on Jun 20, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@version: 0.3
@license: LGPL - Lesser General Public License

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
