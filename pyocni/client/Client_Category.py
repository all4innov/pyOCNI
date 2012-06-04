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

if __name__ == '__main__':

    # ====== Adding a new Kind ======
    print ('======================================== Adding a new kind ========================================')
    body='''
        '{
         "kinds":[
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
                            "pattern": "(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\\-]*[a-zA-Z0-9])\\.)*",
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
                "http://schemas.ogf.org/occi/infrastructure/compute/action#restart",
                "http://schemas.ogf.org/occi/infrastructure/compute/action#suspend"
            ],
            "location": "/compute/"
        }
    ]
    }
    '''
    c = pycurl.Curl()
    c.setopt(pycurl.URL, 'http://127.0.0.1:8090/-/kind/')
    c.setopt(pycurl.HTTPHEADER, ['Accept: text/plain'])
    c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/occi+json'])
    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.USERPWD, 'user1:password')
    c.setopt(pycurl.POSTFIELDS,body)
    c.perform()
