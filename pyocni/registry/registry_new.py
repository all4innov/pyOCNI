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
Created on May 29, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@version: 0.1
@license: LGPL - Lesser General Public License
"""

import pyocni.pyocni_tools.ocni_exceptions as ocni_exceptions
import pyocni.pyocni_tools.config as config

from pyocni.specification.occi_core import Category, Kind, Mixin, Action, Entity, Resource, Link


import transaction
import os
import couchdb
# getting the Logger
logger = config.logger
import simplejson as json

#<<<<<CategoryRegistry>>>>>

class Category_registry(object):
    """

    A registry containing default Kinds, Mixins, actions and more.

    """

    def __init__(self):
        """
        Initialize db for the upcoming inputs
        """
        server=couchdb.Server()
        server.delete('category')
        self.category_db=server.create('category')


    def load_defaults(self):

       """
       Load default kinds and mixins from the default folder

       """
       #try :
       for file in os.listdir("../default"):
           print "../default/"+ file
           default_file=open("../default/"+ file,"r")
           contenu=default_file.read()
           contenu = json.loads(contenu)
           doc_id,doc_rev=self.category_db.save(contenu)
       #except:
           #print("Default files missing, please contact administrator")


if __name__=='__main__':
    Cat_Reg=Category_registry()
    Cat_Reg.load_defaults()





