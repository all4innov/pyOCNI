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
Created on Jun 19, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@license: Apache License, Version 2.0
"""

import pyocni.TDD.fake_Data.categories as f_categories
import pyocni.TDD.fake_Data.entities as f_entities
import pycurl

def init_fakeDB():
    """
    Fill the database with Fake DB
    """
    add_fake_action()
    add_fake_kind()
    add_fake_mixin()


def add_fake_kind():
    c = pycurl.Curl()
    c.setopt(c.URL, 'http://127.0.0.1:8090/-/')
    c.setopt(c.HTTPHEADER, ['Content-Type: application/occi+json', 'Accept: application/occi+json'])
    c.setopt(c.POSTFIELDS, f_categories.kind)
    c.setopt(c.CUSTOMREQUEST, 'POST')
    c.perform()


def add_fake_mixin():
    c = pycurl.Curl()
    c.setopt(c.URL, 'http://127.0.0.1:8090/-/')
    c.setopt(c.HTTPHEADER, ['Content-Type: application/occi+json', 'Accept: application/occi+json'])
    c.setopt(c.POSTFIELDS, f_categories.mixin)
    c.setopt(c.CUSTOMREQUEST, 'POST')
    c.perform()


def add_fake_action():
    c = pycurl.Curl()
    c.setopt(c.URL, 'http://127.0.0.1:8090/-/')
    c.setopt(c.HTTPHEADER, ['Content-Type: application/occi+json', 'Accept: application/occi+json'])
    c.setopt(c.POSTFIELDS, f_categories.action)
    c.setopt(c.CUSTOMREQUEST, 'POST')
    c.perform()


def add_fake_resource():
    c = pycurl.Curl()
    c.setopt(c.URL, 'http://127.0.0.1:8090/compute/')
    c.setopt(c.HTTPHEADER, ['Content-Type: application/occi+json', 'Accept: application/occi+json'])
    c.setopt(c.POSTFIELDS, f_entities.resource)
    c.setopt(c.CUSTOMREQUEST, 'POST')
    c.perform()