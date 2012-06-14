# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

# Copyright (C) 2011 Houssem Medhioub - Institut Telecom
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
@organization: Institut Telecom - Telecom SudParis
@version: 0.2
@license: LGPL - Lesser General Public License
"""
from multiprocessing import Process
from couchdbkit import *
import pyocni.pyocni_tools.config as config
from unittest import TestLoader,TextTestRunner,TestCase
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
        db = server.get_or_create_db(config.Kind_DB)
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
        try:
            self.id = get_me_an_id()
        except Exception as e:
            print e.message
        time.sleep(0.5)

    def tearDown(self):
        self.p.terminate()

    def test_get_all_kinds(self):
        """
        Get all kinds
        """
        storage = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/kind/')
        c.setopt(pycurl.HTTPHEADER, ['Accept: application/occi+json'])
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
        c.setopt(pycurl.CUSTOMREQUEST, 'GET')
        c.setopt(pycurl.USERPWD, 'user_1:password')
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        content = storage.getvalue()
        print " ===== Body content =====\n " + content + " ==========\n"
        self.assertEqual(c.getinfo(pycurl.HTTP_CODE),return_code['OK'])

    def test_get_kind_by_id(self):
        """
        get the kind specific to the id

        """

        storage = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/kind/user_1/'+self.id)
        c.setopt(pycurl.HTTPHEADER, ['Accept: application/occi+json'])
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
        c.setopt(pycurl.CUSTOMREQUEST, 'GET')
        c.setopt(pycurl.USERPWD, 'user_1:password')
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        content = storage.getvalue()
        print " ===== Body content =====\n " + content + " ==========\n"
        self.assertEqual(c.getinfo(pycurl.HTTP_CODE),return_code['OK'])

    def test_get_kind_with_wrong_id(self):
        """
        get a kind using a bad id

        """
        id = "41005914"
        storage = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/kind/'+id)
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
        self.body='''
{
    "kinds": [
        {
            "term": "compute",
            "scheme": "http://schemas.ogf.org/occi/infrastructure#",
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
            "location": "/compute/"
        }
    ]
}
'''
        self.p = Process(target = start_server)
        self.p.start()
        time.sleep(0.5)

    def tearDown(self):
        self.p.terminate()

    def test_add_kind(self):

        storage = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL, 'http://127.0.0.1:8090/-/kind/')
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
        time.sleep(0.5)
        self.updated_data = '''
{

   "OCCI_Description": {
       "kinds": [
           {
               "term": "hhh, it was updated"
           }
       ]
   }
}
'''



    def tearDown(self):
        self.p.terminate()

    def test_update_kind_normal(self):

        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/kind/user_1/'+self.id)
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

    def test_update_kind_unauthorized(self):

        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/kind/userm/'+self.id)
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

    def test_update_kind_notfound(self):

        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/kind/user_1/47b2-ab50-0e340bce9cc2')
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


    def test_delete_kind_unauthorized(self):

        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/kind/userm/'+self.id)
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

    def test_delete_kind_notfound(self):

        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/kind/user_1/bbe47489-001')
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

    def test_delete_kind_normal(self):

        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/kind/user_1/'+self.id)
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