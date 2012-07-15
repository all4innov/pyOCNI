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
import pyocni.pyocni_tools.uuid_Generator as uuid

post_resources= """{
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
                        "cores": 2
                    }
                },
                "org": {
                    "other": {
                        "occi": {
                            "my_mixin": {
                                "my_attribute": "my_value"
                            }
                        }
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
            "id": "996ad860-2a9a-504f-8861-aeafd0b2ae30",
            "title": "Compute resource",
            "summary": "This is a compute resource"
        }
    ]
}
"""
associate_mixin = """
{"Resource_Locations":["http://127.0.0.1:8090/user_1/compute/996ad860-2a9a-504f-8861-aeafd0b2ae29","http://127.0.0.1:8090/user_1/compute/996ad860-2a9a-504f-8861-aeafd0b2ae30"]}
"""
put_on_mixin_path = """
{"Resource_Locations":["http://127.0.0.1:8090/user_1/compute/996ad860-2a9a-504f-8861-aeafd0b2ae29","http://127.0.0.1:8090/user_1/compute/996ad860-2a9a-504f-8861-aeafd0b2ae30"],
"Mixin_Locations":[]}
"""

links ="""
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


part_links = """{
    "links": [
            {
            "id": " try to change it",
            "title": "My partial update test !",
            "target": "http://127.0.0.1:8090/bilel/compute/vm1",
            "source": "http://127.0.0.1:8090/bilel/compute2/vm2"
        }
    ]
}
"""
part_resource ="""
{
    "resources": [{

            "id": "996ad860-2a9a-504f-8861-aeafd0b2ae29",
            "title": "Compute resource ????",
            "summary": "This is a compute resource"
        }
    ]
}
"""

post_resources_link= """{
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
                        "cores": 2
                    }
                },
                "org": {
                    "other": {
                        "occi": {
                            "my_mixin": {
                                "my_attribute": "my_value"
                            }
                        }
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
            "links":{},
            "id": "996ad860-2a9a-504f-8861-aeafd0b2ae30",
            "title": "Compute resource",
            "summary": "This is a compute resource"
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


trig_action = """
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

entity_http = "Category:compute; scheme=\"http://schemas.ogf.org/occi/infrastructure#\"; class=\"kind\";"\
      "Category: my_stuff; scheme=\"http://example.com/occi/my_stuff#\"; class=\"mixin\";"\
      "X-OCCI-Attribute: occi.compute.cores=2"\
      "X-OCCI-Attribute: occi.compute.hostname=\"foobar\""\
      "Link: </users/foo/compute/b9ff813e-fee5-4a9d-b839-673f39746096?action=start>;"\
      "rel=\"http://schemas.ogf.org/occi/infrastructure/compute/action#start\""