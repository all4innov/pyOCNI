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

resource = """{
    "resources": [
            {
            "kind": "http://schemas.ogf.org/occi/infrastructure#compute",
            "mixins": [
                "http://example.com/template/resource#medium"
            ],
            "attributes": {
                "occi": {
                    "compute": {
                        "speed": 2,
                        "memory": 4,
                        "cores": 12
                    }
                }
            },
            "actions": [
                    {
                    "title": "Start My Server",
                    "href": "/compute/996ad860-2a9a-504f-8861-aeafd0b2ae29?action=start",
                    "category": "http://schemas.ogf.org/occi/infrastructure/compute/action#start"
                }
            ],
            "id": "9930",
            "title": "Compute resource",
            "summary": "This is a compute resource"
        }
    ]
}
"""
#=======================================================================================================================

link = """
{
    "links": [
        {
            "kind": "http://schemas.ogf.org/occi/infrastructure#compute",
            "mixins": [
                "http://example.com/template/resource#medium"
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
            "id": "22fe83ae-a20f-54fc-b436-cec85c94c5e8",
            "title": "Mynetworkinterface",
            "target": "http://127.0.0.1:8090/bilel/vms/v2",
            "source": "http://127.0.0.1:8090/bilel/vms/v1"
        }
    ]
}
"""
#=======================================================================================================================

j_occi_att = """
{
    "resources": [
        {
            "attributes": {
                "occi": {
                    "compute": {
                        "speed": 2,
                        "memory": 4,
                        "cores": 12
                    }
                }
            }
        }
    ]
}
"""


#=======================================================================================================================
#                                                           HTTP format
#=======================================================================================================================



entity_http = "Category: compute; scheme=\"http://schemas.ogf.org/occi/infrastructure#\"; class=\"kind\";"\
              "Category: my_stuff; scheme=\"http://example.com/template/resource#\"; class=\"medium\";"\
              "X-OCCI-Attribute: occi.compute.cores=2"\
              "Link: </users/foo/compute/b9ff813e-fee5-4a9d-b839-673f39746096?action=start>;"\
              "rel=\"http://schemas.ogf.org/occi/infrastructure/compute/action#start\""

#=======================================================================================================================


x_occi_att = "X-OCCI-Attribute: occi.compute.cores=20:2"