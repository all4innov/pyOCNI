
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

kind =\
    "{"\
    "\"kinds\": ["\
            "{"\
            "\"term\": \"compute\","\
            """
            "scheme": "http://schemas.ogf.org/occi/infrastructure#",
            "title": "Compute Resource",
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
                "http://schemas.ogf.org/occi/infrastructure/compute/action#start"
            ],
            """ \
            "\"location\": \"/compute/\""\
        "}"\
    "]"\
"}"


#=======================================================================================================================


mixin = """
{
"mixins": [
    {
        "term": "medium",
        "scheme": "http://example.com/template/resource#",
        "title": "Medium VM",
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

"""


#=======================================================================================================================


action =\
"""
            {
                "actions": [
        {
            "term": "start",
            "scheme": "http://schemas.ogf.org/occi/infrastructure/compute/action#",
            "title": "Start Compute instance",
            "attributes": {
                "method": {
                    "mutable": true,
                    "required": false,
                    "type": "string",
                    "pattern": "graceful|acpion|poweron",
                    "default": "poweron"
                }
            }
        }
    ]
}
"""


#=======================================================================================================================

put_provider ="""
    {
    "providers": [
            {
            "Provider": {
                "local": [
                    "dummy"
                ],
                "remote": [
                    "Bilel"
                ]
            },
            "OCCI_ID": "http://schemas.ogf.org/occi/infrastructure#compute"
        }
    ]
}
"""

provider_up = """
{
    "Providers": {
        "remote": [],
        "local": [
            "dummy"
        ]
    }
}"""

#======================================================================================================================

post_http_categories = "Category : my_stuff;\"" \
                    "scheme=\"http://example.com/occi/my_stuff#\";"\
                   "class=\"mixin\";"\
                   "title=\"Storage Resource\";"\
                   "location=\"/my_stuff/\";"\
                   "attributes=\"occi.storage.size{required} occi.storage.state{immutable}\";"\
