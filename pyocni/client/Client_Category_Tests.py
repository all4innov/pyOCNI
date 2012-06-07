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
Created on Jun 4, 2012

@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@organization: Institut Telecom - Telecom SudParis
@version: 0.1
@license: LGPL - Lesser General Public License
"""
import pycurl
import pprint




body='''
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
updated_data = '''
{"actions": ["http://schemas.ogf.org/occi/infrastructure/compute/action#start",
                "http://schemas.ogf.org/occi/infrastructure/compute/action#stop",
                "http://schemas.ogf.org/occi/infrastructure/compute/action#restart"
                ]}
'''
# ====== Adding a new Kind ======
def test_add_kind():
    print ('======================================== Adding a new kind ========================================')
    c = pycurl.Curl()
    c.setopt(pycurl.URL, 'http://127.0.0.1:8090/-/kind/')
    c.setopt(pycurl.HTTPHEADER, ['Accept: text/plain'])
    c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.USERPWD, 'user_1:password')
    c.setopt(pycurl.POSTFIELDS,body)
    c.perform()
    c.close()
    print ('\n==================================================================================================')

# ====== Deleting a Kind ======
def test_delete_kind():

    print ('======================================== Deleting a kind ========================================')
    c = pycurl.Curl()
    c.setopt(pycurl.URL, 'http://127.0.0.1:8090/-/kind/user_1/2ee')
    c.setopt(pycurl.HTTPHEADER, ['Accept: text/plain'])
    c.setopt(pycurl.HTTPHEADER, ['Content-Type: text/plain'])
    c.setopt(pycurl.CUSTOMREQUEST, 'DELETE')
    c.setopt(pycurl.USERPWD, 'user_1:password')
    c.perform()
    c.close()
    print ('\n==================================================================================================')

# ====== Getting all kinds ======
def test_get_all_kinds():

    print ('==========================================================================================')
    Test = 'Getting all kinds'
    Res = 'OK'
    try:
        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/kind/')
        c.setopt(pycurl.HTTPHEADER, ['Accept: application/occi+json'])
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
        c.setopt(pycurl.CUSTOMREQUEST, 'GET')
        c.setopt(pycurl.USERPWD, 'user_1:password')
        c.perform()
        c.close()
    except Exception:
        Res = 'Failed'
    print ("\n" + Test + " = " + Res)
    print ('\n==========================================================================================')

    # ====== Update kind ======
def test_update_kind():

    print ('==========================================================================================')
    Test = 'Getting all kinds'
    Res = 'OK'
    try:
        c = pycurl.Curl()
        c.setopt(pycurl.URL,'http://127.0.0.1:8090/-/kind/user_1/8b2d9f37-2ca8-41c6-ae6d-d93c7ba2cacb')
        c.setopt(pycurl.HTTPHEADER, ['Accept: text/plain'])
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
        c.setopt(pycurl.CUSTOMREQUEST, 'PUT')
        c.setopt(pycurl.USERPWD, 'user_1:password')
        c.setopt(pycurl.POSTFIELDS,updated_data)
        c.perform()
        c.close()
    except Exception:
        Res = 'Failed'
    print ("\n" + Test + " = " + Res)
    print ('\n==========================================================================================')


if __name__ == '__main__':

    #test_add_kind()
    #test_delete_kind()
    #test_get_all_kinds()
    test_update_kind()