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
Created on Jun 01, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@license: Apache License - Version 2.0
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


class occi_server(object):
    """

    The main OCNI REST server

    """

    operationQuery = url_mapper.rest_controller(QueryDispatcher)
    operationSingleEntity = url_mapper.rest_controller(SingleEntityDispatcher)
    operationMultiEntity = url_mapper.rest_controller(MultiEntityDispatcher)
    app = url_mapper.Router()

    app.add_route('/-/', controller=operationQuery)

    app.add_route('/{location}/', controller=operationMultiEntity)
    app.add_route('/{location}/{idontknow}/', controller=operationMultiEntity)
    app.add_route('/{location}/{idontknow}/{idontcare}/', controller=operationMultiEntity)

    app.add_route('/{location}/{idontknow}', controller=operationSingleEntity)
    app.add_route('/{location}/{idontknow}/{idontcare}', controller=operationSingleEntity)


    def run_server(self):
        """

        to run the server

        """

        db_status = config.check_db()
        if db_status == 1:
            result = shell_ask.query_yes_no_quit(" \n_______________________________________________________________\n"
                                                 "   Do you want to purge all databases (DB  reinitialization)?", "no")
            if result == 'yes':
                config.purge_PyOCNI_db()

            print ("\n______________________________________________________________________________________\n"
                   "The OCNI server is running at: " + config.OCNI_IP + ":" + config.OCNI_PORT)
            wsgi.server(eventlet.listen((config.OCNI_IP, int(config.OCNI_PORT))), self.app)
            print ("\n______________________________________________________________________________________\n"
                   "Closing correctly PyOCNI server ")
        else:
            print ("\n______________________________________________________________________________________\n"
                   "The Database is OFF. Please start it before running pyOCNI.")


if __name__ == '__main__':
    occi_server_instance = occi_server()
    occi_server_instance.run_server()
