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
Created on Jun 11, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@version: 0.3
@license: LGPL - Lesser General Public License
"""

from multiprocessing import Process
from unittest import TestLoader,TextTestRunner,TestCase
from couchdbkit import *
import pyocni.pyocni_tools.config as config
import pyocni.client.server_Mock as server
import pycurl
import time
import StringIO

# ======================================================================================
# HTTP Return Codes
# ======================================================================================
return_code = {'OK': 200,
               'Accepted': 202,
               'Bad Request': 400,
               'Unauthorized': 401,
               'Forbidden': 403,
               'Resource not found': 404,
               'Method Not Allowed': 405,
               'Conflict': 409,
               'Gone': 410,
               'Unsupported Media Type': 415,
               'Internal Server Error': 500,
               'Not Implemented': 501,
               'Service Unavailable': 503}

def start_server():
    ocni_server_instance = server.ocni_server()
    ocni_server_instance.run_server()
def get_me_an_id():
    try:
        DB_server_IP = config.DB_IP
        DB_server_PORT = config.DB_PORT
        server = Server('http://' + str(DB_server_IP) + ':' + str(DB_server_PORT))
        db = server.get_or_create_db(config.Mixin_DB)
    except Exception:
        raise Exception("Database is unreachable")
    res = db.all_docs()
    if res is None:
        raise Exception('Database is empty')
    else:
        for re in res:
            if re['id'][0] != "_":
                return re['id']

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
        try:
            self.id = get_me_an_id()
        except Exception as e:
            print e.message

    def tearDown(self):
        self.p.terminate()

    def test_get_all_mixins(self):
        """
        Get all mixins
        """
        storage = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/mixin/')
        c.setopt(pycurl.HTTPHEADER, ['Accept: application/occi+json'])
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
        c.setopt(pycurl.CUSTOMREQUEST, 'GET')
        c.setopt(pycurl.USERPWD, 'user_1:password')
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        content = storage.getvalue()
        print " ===== Body content =====\n " + content + " ==========\n"
        self.assertEqual(c.getinfo(pycurl.HTTP_CODE),return_code['OK'])

    def test_get_mixin_by_id(self):
        """
        get the mixin specific to the id

        """

        storage = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/mixin/user_1/' + self.id)
        c.setopt(pycurl.HTTPHEADER, ['Accept: application/occi+json'])
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
        c.setopt(pycurl.CUSTOMREQUEST, 'GET')
        c.setopt(pycurl.USERPWD, 'user_1:password')
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        content = storage.getvalue()
        print " ===== Body content =====\n " + content + " ==========\n"
        self.assertEqual(c.getinfo(pycurl.HTTP_CODE),return_code['OK'])

    def test_get_mixin_with_wrong_id(self):
        """
        get a mixin using a bad id

        """
        id = "41005914"
        storage = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/mixin/'+id)
        c.setopt(pycurl.HTTPHEADER, ['Accept: application/occi+json'])
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
        c.setopt(pycurl.CUSTOMREQUEST, 'GET')
        c.setopt(pycurl.USERPWD, 'user_1:password')
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        content = storage.getvalue()
        print " ===== Body content =====\n " + content + " ==========\n"
        self.assertEqual(c.getinfo(pycurl.HTTP_CODE),return_code['Resource not found'])

class test_post(TestCase):
    """
    Tests the post request scenarios
    """
    def setUp(self):

        """
        Set up the test environment
        """
        self.body ='''
{
            "mixins": [
                    {
                    "term": "medium100",
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
                    "location": "/template/resource/medium/"
                }
            ]
}
'''
        self.repbody ='''
{
            "mixins": [
                    {
                    "term": "medium100",
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
                    "location": "/template/resource/medium/"
                }
            ]
}
'''
        self.p = Process(target = start_server)
        self.p.start()
        time.sleep(0.5)

    def tearDown(self):
        self.p.terminate()

    def test_add_mixin(self):

        storage = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL, 'http://127.0.0.1:8090/-/mixin/')
        c.setopt(pycurl.HTTPHEADER, ['Accept: text/plain'])
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
        c.setopt(pycurl.POST, 1)
        c.setopt(pycurl.USERPWD, 'user_1:password')
        c.setopt(pycurl.POSTFIELDS,self.body)
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        content = storage.getvalue()
        print " ===== Body content =====\n " + content + " ==========\n"
        self.assertEqual(c.getinfo(pycurl.HTTP_CODE),return_code['OK'])

    def test_add_replicated_mixin(self):

        storage = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL, 'http://127.0.0.1:8090/-/mixin/')
        c.setopt(pycurl.HTTPHEADER, ['Accept: text/plain'])
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
        c.setopt(pycurl.POST, 1)
        c.setopt(pycurl.USERPWD, 'user_1:password')
        c.setopt(pycurl.POSTFIELDS,self.repbody)
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        content = storage.getvalue()
        print " ===== Body content =====\n " + content + " ==========\n"
        self.assertEqual(c.getinfo(pycurl.HTTP_CODE),return_code['Conflict'])

class test_put(TestCase):
    """
    Tests the put request scenarios
    """
    def setUp(self):
        self.p = Process(target=start_server)
        self.p.start()
        try:
            self.id = get_me_an_id()
        except Exception as e:
            print e.message
        self.updated_data ='''
{

        "mixins": [
            {
                "term": "medium",
                "scheme": "http://example.com/template/resource#",
                "title": "Large VM",
                "related": [
                    "http://schemas.ogf.org/occi/infrastructure#resource_tpl"
                ],
                "attributes": {
                    "occi": {
                        "compute": {
                            "speed": {
                                "type": "number",
                                "default": 3
                            }
                        }
                    }
                },
                "location": "/template/resource/medium/"
            }
        ]

}
'''
        self.updated_provider ='''
{
        "Provider": {
            "remote": ["holo"
            ],
            "local": ["molo"
            ]
}       }
'''
        time.sleep(0.5)


    def tearDown(self):
        self.p.terminate()

    def test_update_mixin_normal(self):

        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/mixin/user_1/'+self.id)
        c.setopt(pycurl.HTTPHEADER, ['Accept: text/plain'])
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
        c.setopt(pycurl.CUSTOMREQUEST, 'PUT')
        c.setopt(pycurl.USERPWD, 'user_1:password')
        c.setopt(pycurl.POSTFIELDS,self.updated_data)
        storage = StringIO.StringIO()
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        content = storage.getvalue()
        print " ===== Body content =====\n " + content + " ==========\n"
        self.assertEqual(c.getinfo(pycurl.HTTP_CODE),return_code['OK'])

    def test_update_mixin_unauthorized(self):

        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/mixin/userm/'+self.id)
        c.setopt(pycurl.HTTPHEADER, ['Accept: text/plain'])
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
        c.setopt(pycurl.CUSTOMREQUEST, 'PUT')
        c.setopt(pycurl.USERPWD, 'user_1:password')
        c.setopt(pycurl.POSTFIELDS,self.updated_data)
        storage = StringIO.StringIO()
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        content = storage.getvalue()
        print " ===== Body content =====\n " + content + " ==========\n"
        self.assertEqual(c.getinfo(pycurl.HTTP_CODE),return_code['Unauthorized'])

    def test_update_mixin_notfound(self):

        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/mixin/user_1/fb1cff2a-641c-47b2-ab50-cc2')
        c.setopt(pycurl.HTTPHEADER, ['Accept: text/plain'])
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
        c.setopt(pycurl.CUSTOMREQUEST, 'PUT')
        c.setopt(pycurl.USERPWD, 'user_1:password')
        c.setopt(pycurl.POSTFIELDS,self.updated_data)
        storage = StringIO.StringIO()
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        content = storage.getvalue()
        print " ===== Body content =====\n " + content + " ==========\n"
        self.assertEqual(c.getinfo(pycurl.HTTP_CODE),return_code['Resource not found'])

    def test_update_mixin_Provider_normal(self):

        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/mixin/user_1/'+self.id)
        c.setopt(pycurl.HTTPHEADER, ['Accept: text/plain'])
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
        c.setopt(pycurl.CUSTOMREQUEST, 'PUT')
        c.setopt(pycurl.USERPWD, 'user_1:password')
        c.setopt(pycurl.POSTFIELDS,self.updated_provider)
        storage = StringIO.StringIO()
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        content = storage.getvalue()
        print " ===== Body content =====\n " + content + " ==========\n"
        self.assertEqual(c.getinfo(pycurl.HTTP_CODE),return_code['OK'])

    def test_update_mixin_Provider_unauthorized(self):

        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/mixin/userm/'+self.id)
        c.setopt(pycurl.HTTPHEADER, ['Accept: text/plain'])
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
        c.setopt(pycurl.CUSTOMREQUEST, 'PUT')
        c.setopt(pycurl.USERPWD, 'user_1:password')
        c.setopt(pycurl.POSTFIELDS,self.updated_provider)
        storage = StringIO.StringIO()
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        content = storage.getvalue()
        print " ===== Body content =====\n " + content + " ==========\n"
        self.assertEqual(c.getinfo(pycurl.HTTP_CODE),return_code['Unauthorized'])

    def test_update_mixin_Provider_notfound(self):

        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/mixin/user_1/47b2-ab50-0e340bce9cc2')
        c.setopt(pycurl.HTTPHEADER, ['Accept: text/plain'])
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
        c.setopt(pycurl.CUSTOMREQUEST, 'PUT')
        c.setopt(pycurl.USERPWD, 'user_1:password')
        c.setopt(pycurl.POSTFIELDS,self.updated_provider)
        storage = StringIO.StringIO()
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        content = storage.getvalue()
        print " ===== Body content =====\n " + content + " ==========\n"
        self.assertEqual(c.getinfo(pycurl.HTTP_CODE),return_code['Resource not found'])


class test_delete(TestCase):
    """
    Tests the put request scenarios
    """
    def setUp(self):
        self.p = Process(target=start_server)
        self.p.start()
        try:
            self.id = get_me_an_id()
        except Exception as e:
            print e.message
        time.sleep(0.5)


    def tearDown(self):
        self.p.terminate()

    def test_delete_mixin_unauthorized(self):

        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/mixin/userm/'+self.id)
        c.setopt(pycurl.HTTPHEADER, ['Accept: text/plain'])
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
        c.setopt(pycurl.CUSTOMREQUEST, 'DELETE')
        c.setopt(pycurl.USERPWD, 'user_1:password')
        storage = StringIO.StringIO()
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        content = storage.getvalue()
        print " ===== Body content =====\n " + content + " ==========\n"
        self.assertEqual(c.getinfo(pycurl.HTTP_CODE),return_code['Unauthorized'])

    def test_delete_mixin_notfound(self):

        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/mixin/user_1/fb1cff2a-641c-47b2-ab50-0')
        c.setopt(pycurl.HTTPHEADER, ['Accept: text/plain'])
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
        c.setopt(pycurl.CUSTOMREQUEST, 'DELETE')
        c.setopt(pycurl.USERPWD, 'user_1:password')
        storage = StringIO.StringIO()
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        content = storage.getvalue()
        print " ===== Body content =====\n " + content + " ==========\n"
        self.assertEqual(c.getinfo(pycurl.HTTP_CODE),return_code['Resource not found'])

    def test_delete_mixin_normal(self):

        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/mixin/user_1/'+self.id)
        c.setopt(pycurl.HTTPHEADER, ['Accept: text/plain'])
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
        c.setopt(pycurl.CUSTOMREQUEST, 'DELETE')
        c.setopt(pycurl.USERPWD, 'user_1:password')
        storage = StringIO.StringIO()
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        content = storage.getvalue()
        print " ===== Body content =====\n " + content + " ==========\n"
        self.assertEqual(c.getinfo(pycurl.HTTP_CODE),return_code['OK'])

if __name__ == '__main__':

    #Create the testing tools
    loader = TestLoader()
    runner = TextTestRunner(verbosity=2)

    #Create the testing suites
    get_suite = loader.loadTestsFromTestCase(test_get)
    post_suite = loader.loadTestsFromTestCase(test_post)
    put_suite = loader.loadTestsFromTestCase(test_put)
    delete_suite = loader.loadTestsFromTestCase(test_delete)

    #Run tests
    runner.run(get_suite)
    runner.run(post_suite)
    runner.run(put_suite)
    runner.run(delete_suite)
