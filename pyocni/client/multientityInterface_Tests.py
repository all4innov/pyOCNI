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
Created on Jun 27, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@version: 0.3
@license: LGPL - Lesser General Public License
"""
from multiprocessing import Process
from pyocni.pyocni_tools.config import return_code
from unittest import TestLoader,TextTestRunner,TestCase
import pyocni.client.server_Mock as server
import pycurl
import time
import StringIO


def start_server():
    ocni_server_instance = server.ocni_server()
    ocni_server_instance.run_server()
resources ="""
{
    "resources": [
            {
            "kind": "http://schemas.ogf.org/occi/core#resource",
            "mixins": [
                "http://example.com/template/resource#medium",
                "http://schemas.ogf.org/occi/infrastructure#mixin"
            ],
            "attributes": {
                "occi": {
                    "compute": {
                        "speed": 2,
                        "memory": 4,
                        "cores": 2
                    }
                },
                "org": {
                    "other": {
                        "occi": {
                            "my_mixin": {
                                "my_attribute": "my_value"
                            }
                        }
                    }
                }
            },
            "actions": [
                    {
                    "title": "Start My Server",
                    "href": "/compute/996ad860-2a9a-504f-8861-aeafd0b2ae29?action=start",
                    "category": "http://schemas.ogf.org/occi/infrastructure/compute/action#start"
                }
            ],
            "id": "996ad860-2a9a-504f-8861-aeafd0b2ae29",
            "title": "Compute resource",
            "summary": "This is a compute resource"
        }
    ]
}
"""
resources_link ="""
{
    "resources": [
        {
            "kind": "http://schemas.ogf.org/occi/core#resource",
            "mixins": [
                "http://example.com/template/resource#medium",
                "http://schemas.ogf.org/occi/infrastructure#mixin"
            ],
            "attributes": {
                "occi": {
                    "compute": {
                        "speed": 2,
                        "memory": 4,
                        "cores": 2
                    }
                },
                "org": {
                    "other": {
                        "occi": {
                            "my_mixin": {
                                "my_attribute": "my_value"
                            }
                        }
                    }
                }
            },
            "actions": [
                {
                    "title": "Start My Server",
                    "href": "/compute/996ad860-2a9a-504f-8861-aeafd0b2ae29?action=start",
                    "category": "http://schemas.ogf.org/occi/infrastructure/compute/action#start"
                }
            ],
            "id": "996ad860-2a9a-504f-8861-aeafd0b2ae30",
            "title": "Compute resource",
            "summary": "This is a compute resource",
            "links": [
                {
                    "target": "http://127.0.0.1:8090/user_1/resource/996ad860-2a9a-504f-8861-aeafd0b2ae29",
                    "kind": "http://schemas.ogf.org/occi/infrastructure#resourcestorage",
                    "attributes": {
                        "occi": {
                            "storagelink": {
                                "deviceid": "ide: 0: 1"
                            }
                        }
                    },
                    "id": "391ada15-580c-5baa-b16f-eeb35d9b1122",
                    "title": "Mydisk"
                }
            ]
        }
    ]
}
"""
links = """{
    "links": [
            {
            "kind": "http://schemas.ogf.org/occi/core#resource",
            "attributes": {
                "occi": {
                    "infrastructure": {
                        "networkinterface": {
                            "interface": "eth0",
                            "mac": "00:80:41:ae:fd:7e",
                            "address": "192.168.0.100",
                            "gateway": "192.168.0.1",
                            "allocation": "dynamic"
                        }
                    }
                }
            },
            "actions": [
                    {
                    "title": "Disable networkinterface",
                    "href": "/networkinterface/22fe83ae-a20f-54fc-b436-cec85c94c5e8?action=up",
                    "category": "http://schemas.ogf.org/occi/infrastructure/compute/action#start"
                }
            ],
            "id": "for my test2",
            "title": "Mynetworkinterface",
            "target": "http://127.0.0.1:8090/user_1/resource/996ad860-2a9a-504f-8861-aeafd0b2ae29",
            "source": "http://127.0.0.1:8090/user_1/resource/996ad860-2a9a-504f-8861-aeafd0b2ae30"
        }
    ]
}
"""
occi_ids = """
{"OCCI_Locations":["http://127.0.0.1:8090/user_1/resource/for my test"]}
"""
class test_post(TestCase):
    """
    Tests POST request scenarios
    """
    def setUp(self):

        """
        Set up the test environment
        """
        self.p = Process(target = start_server)
        self.p.start()
        time.sleep(0.5)

    def tearDown(self):
        self.p.terminate()

    def test_register_entities(self):
        """
        register resources & links
        """
        storage = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/resource/')
        c.setopt(pycurl.HTTPHEADER, ['Accept: application/occi+json'])
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
        c.setopt(pycurl.CUSTOMREQUEST, 'POST')
        c.setopt(pycurl.POSTFIELDS,links)
        c.setopt(pycurl.USERPWD, 'user_1:password')
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        content = storage.getvalue()
        print " ===== Body content =====\n " + content + " ==========\n"

    def test_associate_mixin(self):
        """
        register resources & links
        """
        storage = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/mixin/')
        c.setopt(pycurl.HTTPHEADER, ['Accept: application/occi+json'])
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
        c.setopt(pycurl.CUSTOMREQUEST, 'POST')
        c.setopt(pycurl.POSTFIELDS,occi_ids)
        c.setopt(pycurl.USERPWD, 'user_1:password')
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        content = storage.getvalue()
        print " ===== Body content =====\n " + content + " ==========\n"
class test_get(TestCase):
    """
    Tests GET request scenarios
    """
    def setUp(self):

        """
        Set up the test environment
        """
        self.p = Process(target = start_server)
        self.p.start()
        time.sleep(0.5)

    def tearDown(self):
        self.p.terminate()

    def test_get_all_entities(self):
        """
        get resources & links
        """

        storage = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL,"http://127.0.0.1:8090/template/resource/medium2/")
        c.setopt(pycurl.HTTPHEADER, ['Accept: application/occi+json'])
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
        c.setopt(pycurl.CUSTOMREQUEST, 'GET')
        c.setopt(pycurl.USERPWD, 'user_1:password')
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        content = storage.getvalue()
        print " ===== Body content =====\n " + content + " ==========\n"

    def test_get_filtred_entities(self):
        """
        get filtred resources & links
        """

        storage = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL,"http://127.0.0.1:8090/template/resource/medium2/")
        c.setopt(pycurl.HTTPHEADER, ['Accept: application/occi+json'])
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
        c.setopt(pycurl.CUSTOMREQUEST, 'GET')
        c.setopt(pycurl.USERPWD, 'user_1:password')
        c.setopt(pycurl.POSTFIELDS,resources)
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        content = storage.getvalue()
        print " ===== Body content =====\n " + content + " ==========\n"

if __name__ == '__main__':

    #Create the testing tools
    loader = TestLoader()
    runner = TextTestRunner(verbosity=2)

    #Create the testing suites
    get_suite = loader.loadTestsFromTestCase(test_get)
    #    delete_suite = loader.loadTestsFromTestCase(test_delete)
    #    put_suite = loader.loadTestsFromTestCase(test_put)
    post_suite = loader.loadTestsFromTestCase(test_post)
    #Run tests
    runner.run(get_suite)
    #    runner.run(delete_suite)
    #    runner.run(put_suite)
    runner.run(post_suite)