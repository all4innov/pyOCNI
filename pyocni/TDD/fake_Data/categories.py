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

#=======================================================================================================================
#                                                           JSON format
#=======================================================================================================================

kind =\
    "{"\
    "\"kinds\": ["\
            "{"\
            "\"term\": \"compute\","\
            """
            "scheme": "http://schemas.ogf.org/occi/infrastructure#",
            "title": "Compute Resource no2",
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
                        "default": 3.0
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
            "title": "Start Compute instance now",
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





#=======================================================================================================================
#                                                           HTTP format
#=======================================================================================================================

kind_occci_id="""Category: compute;
 scheme="http://schemas.ogf.org/occi/infrastructure#";
 class=kind;
"""
#=======================================================================================================================

mixin_occci_id="""Category: medium;
 scheme="http://example.com/template/resource#";
 class=mixin;
"""
#=======================================================================================================================

action_occci_id="""Category: start;
 scheme="http://schemas.ogf.org/occi/infrastructure/compute/action#";
 class=action;
"""
#=======================================================================================================================

mixin_http = "Category : my_stuff;\""\
             "scheme=\"http://example.com/occi/my_stuff#\";"\
             "class=\"mixin\";"\
             "title=\"Storage Resource\";"\
             "location=\"/my_stuff/\";"\
             "attributes=\"occi.storage.size{required} occi.storage.state{immutable}\";"\

#=======================================================================================================================

kind_http = "Category: compute;"\
            "scheme=\"http://schemas.ogf.org/occi/infrastructure#\";"\
            "class=\"kind\";"\
            "title=\"Compute Resource type\";"\
            "rel=\"http://schemas.ogf.org/occi/core#resource\";"\
            "attributes=\"occi.compute.cores occi.compute.state{immutable}\";"\
            "actions=\"http://schemas.ogf.org/occi/infrastructure/compute/action#stop\";"\
            "location=\"http://example.com/compute/\""
