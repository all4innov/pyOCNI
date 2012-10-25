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
from unittest import TestLoader,TextTestRunner,TestCase
import pyocni.client.server_Mock as server
import pycurl
import time
import StringIO
import pyocni.client.entities as fake_data
res_filter = """
{
    "resources": [
        {
            "kind": "http://schemas.ogf.org/occi/core#resource",
            "title": "Compute resource",
            "id": "996ad860-2a9a-504f-8861-aeafd0b2ae29"
        }
    ]
}
            """
def start_server():
    ocni_server_instance = server.ocni_server()
    ocni_server_instance.run_server()

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

    def test_get_on_path(self):
        """
        get resources & links
        """

        storage = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL,"http://127.0.0.1:8090/template/resource/")
        c.setopt(pycurl.HTTPHEADER, ['Accept: application/occi+json'])
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
        c.setopt(pycurl.CUSTOMREQUEST, 'GET')
        c.setopt(pycurl.USERPWD, 'user_1:password')
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        content = storage.getvalue()
        print " ===== Body content =====\n " + content + " ==========\n"

    def test_get_with_filter_on_path(self):
        """
        get resources & links
        """

        storage = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL,"http://127.0.0.1:8090/user_1/compute/")
        c.setopt(pycurl.HTTPHEADER, ['Accept: application/occi+json'])
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
        c.setopt(pycurl.CUSTOMREQUEST, 'GET')
        c.setopt(pycurl.USERPWD, 'user_1:password')
        c.setopt(pycurl.POSTFIELDS,fake_data.links)
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

    def test_delete_on_path(self):
        """
        get resources & links
        """

        storage = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL,"http://127.0.0.1:8090/user_1/compute/")
        c.setopt(pycurl.HTTPHEADER, ['Accept: application/occi+json'])
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
        c.setopt(pycurl.CUSTOMREQUEST, 'DELETE')
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
    #    delete_suite = loader.loadTestsFromTestCase(test_delete)
#    put_suite = loader.loadTestsFromTestCase(test_put)
#    post_suite = loader.loadTestsFromTestCase(test_post)
    #Run tests
    runner.run(get_suite)
    #    runner.run(delete_suite)
#    runner.run(put_suite)
#    runner.run(post_suite)