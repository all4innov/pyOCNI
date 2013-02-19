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
Created on Jun 27, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@license: Apache License, Version 2.0
"""
from multiprocessing import Process
from unittest import TestLoader, TextTestRunner, TestCase
from pyocni.TDD.fake_Data.server_Mock import ocni_server
import pycurl
import time
import StringIO
from pyocni.TDD.fake_Data.initialize_fakeDB import init_fakeDB
import pyocni.TDD.fake_Data.categories as f_categories
import pyocni.pyocni_tools.config as config

def start_server():

    ocni_server_instance = ocni_server()
    ocni_server_instance.run_server()


class test_get(TestCase):
    """
    Tests GET request scenarios
    """

    def setUp(self):
        """
        Set up the test environment
        """
        self.p = Process(target=start_server)
        self.p.start()
        time.sleep(0.5)
        #init_fakeDB()
        time.sleep(0.5)

    def tearDown(self):

        #config.purge_PyOCNI_db()
        self.p.terminate()

    def test_get_categories(self):
        """
        Get all kinds,mixins and actions
        """

        storage = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, 'http://127.0.0.1:8090/-/')
        c.setopt(c.HTTPHEADER, ['Accept:application/occi+json','content-type:application/occi+json'])
        c.setopt(c.VERBOSE, True)
        c.setopt(c.POSTFIELDS,f_categories.kind)
        c.setopt(c.CUSTOMREQUEST, 'GET')
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        content = storage.getvalue()
        print " ========== Body content ==========\n " + content + " \n ==========\n"


class test_delete(TestCase):
    """
    Tests DELETE request scenarios
    """

    def setUp(self):
        """
        Set up the test environment
        """
        self.p = Process(target=start_server)
        self.p.start()
        time.sleep(0.5)
        init_fakeDB()
        time.sleep(0.5)

    def tearDown(self):
        #config.purge_PyOCNI_db()
        self.p.terminate()


    def test_delete_categories(self):
        """
        delete a mixin
        """
        storage = StringIO.StringIO()
        c = pycurl.Curl()

        c.setopt(c.CUSTOMREQUEST, 'DELETE')
        c.setopt(c.URL, 'http://127.0.0.1:8090/-/')
        c.setopt(c.HTTPHEADER, ['Accept: application/occi+json', 'Content-Type: application/occi+json'])
        c.setopt(c.POSTFIELDS, f_categories.kind)
        c.setopt(c.VERBOSE, True)
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
        self.p = Process(target=start_server)
        self.p.start()
        time.sleep(0.5)
        #init_fakeDB()
        time.sleep(0.5)

    def tearDown(self):

        self.p.terminate()
        #config.purge_PyOCNI_db()

    def test_register_categories(self):
        """
        register kind, mixins or actions
        """

        c = pycurl.Curl()
        storage = StringIO.StringIO()

        c.setopt(c.URL, 'http://127.0.0.1:8090/-/')
        c.setopt(c.HTTPHEADER, ['Content-Type: application/occi+json', 'Accept: application/occi+json'])

        c.setopt(c.POSTFIELDS, f_categories.kind)
        c.setopt(c.CUSTOMREQUEST, 'POST')
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
        self.p = Process(target=start_server)
        self.p.start()
        time.sleep(0.5)
        #init_fakeDB()
        time.sleep(0.5)

    def tearDown(self):
        self.p.terminate()
        #config.purge_PyOCNI_db()

    def test_update_categories(self):
        """
        register kind, mixins or actions
        """
        storage = StringIO.StringIO()
        c = pycurl.Curl()

        c.setopt(c.URL, 'http://127.0.0.1:8090/-/')
        c.setopt(c.HTTPHEADER, ['Content-Type: application/occi+json', 'Accept: application/occi+json'])
        c.setopt(c.CUSTOMREQUEST, 'PUT')
        c.setopt(c.POSTFIELDS, f_categories.put_provider)
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

    runner.run(delete_suite)
