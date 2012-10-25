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
    c.setopt(c.URL,'http://127.0.0.1:8090/-/')
    c.setopt(c.HTTPHEADER, ['Content-Type: application/occi+json','Accept: application/occi+json'])
    c.setopt(c.POSTFIELDS,f_categories.kind)
    c.setopt(c.CUSTOMREQUEST, 'POST')
    c.perform()

def add_fake_mixin():
    c = pycurl.Curl()
    c.setopt(c.URL,'http://127.0.0.1:8090/-/')
    c.setopt(c.HTTPHEADER, ['Content-Type: application/occi+json','Accept: application/occi+json'])
    c.setopt(c.POSTFIELDS,f_categories.mixin)
    c.setopt(c.CUSTOMREQUEST, 'POST')
    c.perform()

def add_fake_action():
    c = pycurl.Curl()
    c.setopt(c.URL,'http://127.0.0.1:8090/-/')
    c.setopt(c.HTTPHEADER, ['Content-Type: application/occi+json','Accept: application/occi+json'])
    c.setopt(c.POSTFIELDS,f_categories.action)
    c.setopt(c.CUSTOMREQUEST, 'POST')
    c.perform()

def add_fake_resource():
    c = pycurl.Curl()
    c.setopt(c.URL,'http://127.0.0.1:8090/compute/')
    c.setopt(c.HTTPHEADER, ['Content-Type: application/occi+json','Accept: application/occi+json'])
    c.setopt(c.POSTFIELDS,f_entities.resource)
    c.setopt(c.CUSTOMREQUEST, 'POST')
    c.perform()