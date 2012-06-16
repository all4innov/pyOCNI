

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
Created on Jun 12, 2012

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
        db = server.get_or_create_db(config.Link_DB)
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

    def test_get_all_links(self):
        """
        Get all links
        """
        storage = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/link/')
        c.setopt(pycurl.HTTPHEADER, ['Accept: application/occi+json'])
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
        c.setopt(pycurl.CUSTOMREQUEST, 'GET')
        c.setopt(pycurl.USERPWD, 'user_1:password')
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        content = storage.getvalue()
        print " ===== Body content =====\n " + content + " ==========\n"
        self.assertEqual(c.getinfo(pycurl.HTTP_CODE),return_code['OK'])

    def test_get_link_by_id(self):
        """
        Get the link specific to the id

        """
        storage = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/link/user_1/'+self.id)
        c.setopt(pycurl.HTTPHEADER, ['Accept: application/occi+json'])
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
        c.setopt(pycurl.CUSTOMREQUEST, 'GET')
        c.setopt(pycurl.USERPWD, 'user_1:password')
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        content = storage.getvalue()
        print " ===== Body content =====\n " + content + " ==========\n"
        self.assertEqual(c.getinfo(pycurl.HTTP_CODE),return_code['OK'])

    def test_get_link_with_wrong_id(self):
        """
        Get a link using a bad id

        """
        id = "41005914"
        storage = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/link/'+id)
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
            "links": [
                    {
                    "kind": "http://schemas.ogf.org/occi/infrastructure#networkinterface",
                    "mixins": [
                        "http://schemas.ogf.org/occi/infrastructure/networkinterface#ipnetworkinterface"
                    ],
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
                            "category": "http: //schemas.ogf.org/occi/infrastructure/networkinterface/action#"
                        }
                    ],
                    "id": "22fe83ae-a20f-54fc-b436-cec85c94c5e8",
                    "title": "Mynetworkinterface",
                    "target": "http: //myservice.tld/network/b7d55bf4-7057-5113-85c8-141871bf7635",
                    "source": "http: //myservice.tld/compute/996ad860-2a9a-504f-8861-aeafd0b2ae29"
                }
            ]
        }
'''

        self.p = Process(target = start_server)
        self.p.start()
        time.sleep(0.5)

    def tearDown(self):
        self.p.terminate()

    def test_add_link(self):

        storage = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL, 'http://127.0.0.1:8090/-/link/')
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
        self.updated_data = '''
{
   "_id": "fb1cff2a-641c-47b2-ab50-0e340bce9cc2",
   "_rev": "2-8d02bacda9bcb93c8f03848191fd64f0"

}
'''
        time.sleep(0.5)


    def tearDown(self):
        self.p.terminate()

    def test_update_link_normal(self):

        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/link/user_1/'+self.id)
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

    def test_update_link_unauthorized(self):

        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/link/userm/'+self.id)
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

    def test_update_link_notfound(self):

        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/link/user_1/fb1cff2a-')
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

    def test_delete_link_normal(self):

        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/link/user_1/'+self.id)
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

    def test_delete_link_unauthorized(self):

        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/link/userm/'+self.id)
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

    def test_delete_link_notfound(self):

        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/link/user_1/bbe47489-001')
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