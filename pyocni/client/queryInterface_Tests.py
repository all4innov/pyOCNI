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
Created on Jun 19, 2012

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

actions ="""
{
    "actions": [
        {
            "term": "restart",
            "scheme": "http://schemas.ogf.org/occi/infrastructure/compute/action#",
            "title": "Stop Compute instance",
            "attributes": {
                "method": {
                    "mutable": true,
                    "required": false,
                    "type": "string",
                    "pattern": "graceful|acpioff|poweroff",
                    "default": "poweroff"
                }
            }
        },
        {
            "term": "stop",
            "scheme": "http://schemas.ogf.org/occi/infrastructure/compute/action#",
            "title": "Stop Compute instance",
            "attributes": {
                "method": {
                    "mutable": true,
                    "required": false,
                    "type": "string",
                    "pattern": "graceful|acpioff|poweroff",
                    "default": "poweroff"
                }
            }
        },
        {
            "term": "start",
            "scheme": "http://schemas.ogf.org/occi/infrastructure/compute/action#",
            "title": "Stop Compute instance",
            "attributes": {
                "method": {
                    "mutable": true,
                    "required": false,
                    "type": "string",
                    "pattern": "graceful|acpioff|poweroff",
                    "default": "poweroff"
                }
            }
        }
    ]
}
"""
kinds_indep="""
{"kinds": [
        {
            "term": "resource",
            "scheme": "http://schemas.ogf.org/occi/core#",
            "title": "Compute Bilel",
            "attributes": {
                "occi": {
                    "compute": {
                        "hostname": {
                            "mutable": true,
                            "required": false,
                            "type": "string",
                            "pattern": "(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\\\\-]*[a-zA-Z0-9])\\\\.)*",
                            "minimum": "1",
                            "maximum": "2550"
                        },
                        "state": {
                            "mutable": false,
                            "required": false,
                            "type": "string",
                            "pattern": "inactive|active|suspended|failed",
                            "default": "inactive"
                        }
                    }
                }
            },
            "location": "/resource/"
        }
    ]
    }
"""
kinds_dep = """
{
    "kinds": [
        {
            "term": "storage",
            "scheme": "http://schemas.ogf.org/occi/infrastructure#resource",
            "title": "Compute Resource",
            "related": [
                "http://schemas.ogf.org/occi/core#resource"
            ],
            "attributes": {
                "occi": {
                    "compute": {
                        "hostname": {
                            "mutable": true,
                            "required": false,
                            "type": "string",
                            "pattern": "(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\\\\-]*[a-zA-Z0-9])\\\\.)*",
                            "minimum": "1",
                            "maximum": "255"
                        },
                        "state": {
                            "mutable": false,
                            "required": false,
                            "type": "string",
                            "pattern": "inactive|active|suspended|failed",
                            "default": "inactive"
                        }
                    }
                }
            },
            "actions": [
                "http://schemas.ogf.org/occi/infrastructure/compute/action#start",
                "http://schemas.ogf.org/occi/infrastructure/compute/action#stop",
                "http://schemas.ogf.org/occi/infrastructure/compute/action#restart"
            ],
            "location": "/storage/"
        }
    ]
}"""
mixins = """
{"mixins": [
        {
            "term": "resource_tpl",
            "scheme": "http://schemas.ogf.org/occi/infrastructure#",
            "title": "Big Bad VM",
            "related": [],
            "attributes": {
                "occi": {
                    "compute": {
                        "speed": {
                            "type": "number",
                            "default": 2.8
                        }
                    }
                }
            },
            "location": "/template/resource/resource_tpl/"
        }
    ]
}
"""
mixins_dep = """
{
    "mixins": [
        {
            "term": "medium",
            "scheme": "http://example.com/template/resource#",
            "title": "Medium VM",
            "related": [
                "http://schemas.ogf.org/occi/infrastructure#resource_tpl"
            ],
            "attributes": {
                "occi": {
                    "compute": {
                        "speed": {
                            "type": "number",
                            "default": 2.8
                        }
                    }
                }
            },
            "location": "/template/resource/medium2/"
        },
        {
            "term": "mixin",
            "scheme": "http://schemas.ogf.org/occi/infrastructure#",
            "title": "Compute Resource",
            "related": [
                "http://schemas.ogf.org/occi/infrastructure#resource_tpl"
            ],
            "attributes": {
                "occi": {
                    "compute": {
                        "hostname": {
                            "mutable": true,
                            "required": false,
                            "type": "string",
                            "pattern": "(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\\\\-]*[a-zA-Z0-9])\\\\.)*",
                            "minimum": "1",
                            "maximum": "255"
                        },
                        "state": {
                            "mutable": false,
                            "required": false,
                            "type": "string",
                            "pattern": "inactive|active|suspended|failed",
                            "default": "inactive"
                        }
                    }
                }
            },
            "actions": [
                "http://schemas.ogf.org/occi/infrastructure/compute/action#start",
                "http://schemas.ogf.org/occi/infrastructure/compute/action#stop",
                "http://schemas.ogf.org/occi/infrastructure/compute/action#restart"
            ],
            "location": "/mixin/"
        }
    ]
}
        """
providers ="""
{"providers": [
        {
        "Provider": {
            "local": ["Houssem"],
            "remote": ["Bilel"]
        },
        "OCCI_ID": "http://schemas.ogf.org/occi/infrastructure#resourcestorage"
    }
]
}"""


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

    def test_get_all_categories(self):
        """
        Get all kinds
        """
        storage = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/')
        c.setopt(pycurl.HTTPHEADER, ['Accept: application/occi+json'])
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
        c.setopt(pycurl.CUSTOMREQUEST, 'GET')
        c.setopt(pycurl.USERPWD, 'user_1:password')
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        content = storage.getvalue()
        print " ===== Body content =====\n " + content + " ==========\n"


    def test_get_filter_categories_ok(self):
        """
        get all categories matching the terms contained in the request
        """
        storage = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/')
        c.setopt(pycurl.HTTPHEADER, ['Accept: application/occi+json'])
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
        c.setopt(pycurl.CUSTOMREQUEST, 'GET')
        c.setopt(pycurl.POSTFIELDS,mixins)
        c.setopt(pycurl.USERPWD, 'user_1:password')
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        content = storage.getvalue()
        print " ===== Body content =====\n " + content + " ==========\n"


class test_delete(TestCase):
    """
    Tests DELETE request scenarios
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

    def test_delete_categories(self):
        """
        delete a mixin
        """
        storage = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/')
        c.setopt(pycurl.HTTPHEADER, ['Accept: application/occi+json'])
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
        c.setopt(pycurl.CUSTOMREQUEST, 'DELETE')
        c.setopt(pycurl.POSTFIELDS,mixins)
        c.setopt(pycurl.USERPWD, 'user_1:password')
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        content = storage.getvalue()
        print " ===== Body content =====\n " + content + " ==========\n"




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

    def test_register_categories(self):
        """
        register kind, mixins or actions
        """
        storage = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/')
        c.setopt(pycurl.HTTPHEADER, ['Accept: application/occi+json'])
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
        c.setopt(pycurl.CUSTOMREQUEST, 'POST')
        c.setopt(pycurl.POSTFIELDS,kinds_indep)
        c.setopt(pycurl.USERPWD, 'user_1:password')
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        content = storage.getvalue()
        print " ===== Body content =====\n " + content + " ==========\n"


class test_put(TestCase):
    """
    Tests PUT request scenarios
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

    def test_update_categories(self):
        """
        register kind, mixins or actions
        """
        storage = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/')
        c.setopt(pycurl.HTTPHEADER, ['Accept: application/occi+json'])
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
        c.setopt(pycurl.CUSTOMREQUEST, 'PUT')
        c.setopt(pycurl.POSTFIELDS,kinds_indep)
        c.setopt(pycurl.USERPWD, 'user_1:password')
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
    delete_suite = loader.loadTestsFromTestCase(test_delete)
    post_suite = loader.loadTestsFromTestCase(test_post)
    put_suite = loader.loadTestsFromTestCase(test_put)
    #Run tests
    runner.run(get_suite)
    runner.run(post_suite)
    runner.run(delete_suite)
    runner.run(put_suite)