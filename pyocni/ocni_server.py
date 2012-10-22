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
Created on Jun 01, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@version: 1.0
@license: LGPL - Lesser General Public License
"""
from pyocni.dispachers.single_entityDispatcher import SingleEntityDispatcher
from pyocni.dispachers.multi_entityDispatcher import MultiEntityDispatcher
from pyocni.dispachers.queryDispatcher import QueryDispatcher
import pyocni.pyocni_tools.config as config
import pyocni.pyocni_tools.DoItYourselfWebOb as url_mapper
import eventlet
from eventlet import wsgi
from pyocni.pyocni_tools import ask_user_details as shell_ask



# getting the Logger
logger = config.logger

# getting IP and Port of the OCCI server
OCNI_IP = config.OCNI_IP
OCNI_PORT = config.OCNI_PORT

# ======================================================================================================================
#                                                     The OCNI Server
# ======================================================================================================================


class ocni_server(object):
    """

    The main OCNI REST server

    """


    operationQuery = url_mapper.rest_controller(QueryDispatcher)
    operationSingleEntity = url_mapper.rest_controller(SingleEntityDispatcher)
    operationMultiEntity = url_mapper.rest_controller(MultiEntityDispatcher)
    app = url_mapper.Router()

    app.add_route('/-/',controller=operationQuery)

    app.add_route('/{location}/',controller=operationMultiEntity)
    app.add_route('/{location}/{idontknow}/',controller=operationMultiEntity)
    app.add_route('/{location}/{idontknow}/{idontcare}/',controller=operationMultiEntity)

    app.add_route('/{location}/{idontknow}',controller=operationSingleEntity)
    app.add_route('/{location}/{idontknow}/{idontcare}',controller=operationSingleEntity)


    def run_server(self):
        """

        to run the server

        """
        result = shell_ask.query_yes_no_quit(" \n_______________________________________________________________\n"
                                                     "   Do you want to purge all databases (DB  reinitialization)?", "no")
        if result == 'yes':
            config.purge_PyOCNI_db()

        print ("\n______________________________________________________________________________________\n"
               "The OCNI server is running at: " + config.OCNI_IP + ":"+config.OCNI_PORT)
        wsgi.server(eventlet.listen((config.OCNI_IP, int(config.OCNI_PORT))), self.app)
        print ("\n______________________________________________________________________________________\n"
               "Closing correctly PyOCNI server ")



if __name__ == '__main__':

    ocni_server_instance = ocni_server()
    ocni_server_instance.run_server()

