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
from unittest import TestLoader,TextTestRunner,TestCase
from pyocni.TDD.fake_Data.server_Mock import ocni_server
import pycurl
import time
import StringIO
from pyocni.TDD.fake_Data.initialize_fakeDB import init_fakeDB
from pyocni.TDD.fake_Data import entities, categories
import pyocni.pyocni_tools.config as config

def start_server():
    ocni_server_instance = ocni_server()
    ocni_server_instance.run_server()

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
        #init_fakeDB()
        time.sleep(0.5)

    def tearDown(self):

        #config.purge_PyOCNI_db()
        self.p.terminate()

    def test_post_entities(self):
        """
        register resources & links
        """
        storage = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL,'http://127.0.0.1:8090/compute/this_is_bilel?action=start')
        c.setopt(c.HTTPHEADER, ['Accept: application/occi+json','Content-Type: text/plain'])
        c.setopt(c.CUSTOMREQUEST, 'POST')
        c.setopt(c.VERBOSE, True)
        c.setopt(c.POSTFIELDS,entities.action_att_http)
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
        #init_fakeDB()
        time.sleep(0.5)

    def tearDown(self):

        self.p.terminate()
        #config.purge_PyOCNI_db()

    def test_get_entity(self):
        """
        get resources & links
        """

        storage = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL,"http://127.0.0.1:8090/compute/9930")
        c.setopt(c.HTTPHEADER, ['Accept:application/occi+json'])
        c.setopt(c.VERBOSE, True)
        c.setopt(c.CUSTOMREQUEST, 'GET')
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

    def test_delete_entity(self):
        """
        delete resources & links
        """

        storage = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL,"http://127.0.0.1:8090/compute/this_is_bilel")
        c.setopt(c.HTTPHEADER, ['Content-Type: application/occi+json', 'Accept: application/occi+json'])
        c.setopt(c.CUSTOMREQUEST, 'DELETE')
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
        #init_fakeDB()
        time.sleep(0.5)

    def tearDown(self):
        self.p.terminate()

    def test_create_custom_resource(self):
        """
        """
        storage = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL,'http://127.0.0.1:8090/bilel/home/vm02')

        c.setopt(c.HTTPHEADER, ['Accept: application/occi+json','Content-Type: text/plain'])
        c.setopt(c.CUSTOMREQUEST, 'PUT')
        c.setopt(c.POSTFIELDS,entities.entity_http)
        c.setopt(c.VERBOSE, True)

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
    put_suite = loader.loadTestsFromTestCase(test_put)
    post_suite = loader.loadTestsFromTestCase(test_post)
    #Run tests

    runner.run(put_suite)