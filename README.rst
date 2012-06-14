pyocni README
=============

Copyright (C) Houssem Medhioub <houssem.medhioub@it-sudparis.eu>
Copyright (C) Bilel Msekni >bilel.msekni@telecom-sudparis.eu>
Redistribution of this software is permitted under the terms of the LGPL License

Table of Contents
=================

0. What is it?
1. The Latest Version
2. API Documentation
3. Installation
3.1. Requirements
3.2. Install
3.3. Configuration
3.4. Server running
4. HowTo use (examples)
5. For developers
6. Licensing
7. Contacts
8. Acknowledgment
9. Todo
10. json files to execute the HowTo use examples


0. What is it?
==============

PyOCNI (Python Open Cloud Networking Interface): A Python implementation of an extended OCCI with a JSON serialization and a cloud networking extension


1. The Latest Version
=====================

version 0.2
11 Jan 2012
status: Still an ongoing work

-----------------------------------------------------------------------------
2. API Documentation
-----------------------------------------------------------------------------
the api documentation are available through this html file:
 PyOCNI/pyocni/doc/index.html

-----------------------------------------------------------------------------
3. Installation
-----------------------------------------------------------------------------

3.1. Requirements
-----------------
This software needs this packages to run:
* python == 2.7
* python-all-dev (for eventlet/greenlet install/make)
* python-setuptools (to execute the setup.py file)
* couchdbkit

3.2. Install
------------
sudo python setup.py install

3.3. Configuration
------------------
Logger configuration:  OCCILogging.conf
Server configuration:  occi_server.conf
CouchDB configuration: couchdb_server.conf

3.4. Server running
-------------------
python start.py

-----------------------------------------------------------------------------
4. HowTo use (examples. The json files are at the end of this README)
-----------------------------------------------------------------------------

In order to use PyOCNI, you must respect certain rules :

1- All data must follow the JSON format declared by OCCI [occi+json], any detected conflict will cancel the request.
2- Kinds, Mixins and Actions can be created, read, updated or deleted (CRUD) on the fly.
3- Kinds, Mixins and Actions can be read and created by anyone but updated and deleted by only their creator
4- Resources and Links can be created, read, updated or deleted(CRUD) on the fly.
5- Resources and Links can be read and created by anyone but updated and deleted by only their creator
6- Kinds, Mixins, Actions, Resources and Links have their own distinct storage format (see below)
7- The new data provided in an update request must be sent in consistency with the raw format
8- An update request is done through the update of the fields mentioned in the DocumentSkeleton (see below)

These are some commands that you can use with PyOCNI
__________________________________________________________________________________________________________________

Retrieval of all registered Kinds, Mixins and Actions:

curl -X GET -H 'accept: application/json:occi' -v http://localhost:8090/-/
__________________________________________________________________________________________________________________

Create a Kind
curl -X POST -d@post_kind.json -H 'content-type: application/occi+json' --user user_1:pass -v 'http://localhost:8090/-/kind/'

Get a kind
curl -X GET -H 'content-type: application/occi+json' -v http://localhost:8090/-/kind/{user-id}/{kind-id}

Update a Kind
curl -X PUT -d@up_kind.json -H 'content-type: application/occi+json' --user user_1:pass -v http://localhost:8090/-/kind/{user-id}/{kind-id}

Delete a Kind
curl -X DELETE -H 'content-type: application/occi+json' -v http://localhost:8090/-/kind/{user-id}/{kind-id}

__________________________________________________________________________________________________________________

__________________________________________________________________________________________________________________

Create a Mixin
curl -X POST -d@post_mixin.json -H 'content-type: application/occi+json' --user user_1:pass -v http://localhost:8090/-/mixin/

Get a Mixin
curl -X GET -H 'content-type: application/occi+json' -v http://localhost:8090/-/mixin/{user-id}/{mixin-id}

Update a mixin
curl -X PUT -d@up_mixin.json -H 'content-type: application/occi+json' --user user_1:pass -v http://localhost:8090/-/mixin/{user-id}/{mixin-id}

Delete a mixin
curl -X DELETE -H 'content-type: application/occi+json' -v http://localhost:8090/-/mixin/{user-id}/{mixin-id}

__________________________________________________________________________________________________________________

__________________________________________________________________________________________________________________

Create an Action
curl -X POST -d@post_action.json -H 'content-type: application/occi+json' --user user_1:pass -v http://localhost:8090/-/action/

Get an Action
curl -X GET -H 'content-type: application/occi+json' -v http://localhost:8090/-/action/{user-id}/{action-id}

Update an Action
curl -X PUT -d@up_action.json -H 'content-type: application/occi+json' --user user_1:pass -v http://localhost:8090/-/action/{user-id}/{action-id}

Delete an Action
curl -X DELETE -H 'content-type: application/occi+json' -v http://localhost:8090/-/action/{user-id}/{action-id}

__________________________________________________________________________________________________________________

__________________________________________________________________________________________________________________

Create a Resource
curl -X POST -d@post_resource.json -H 'content-type: application/occi+json' --user user_1:pass -v http://localhost:8090/-/resource/

Get a Resource
curl -X GET -H 'content-type: application/occi+json' -v http://localhost:8090/-/resource/{user-id}/{resource-id}

Update a Resource
curl -X PUT -d@up_resource.json -H 'content-type: application/occi+json' --user user_1:pass -v http://localhost:8090/-/resource/{user-id}/{resource-id}

Delete a Resource
curl -X DELETE -H 'content-type: application/occi+json' -v http://localhost:8090/-/resource/{user-id}/{resource-id}

__________________________________________________________________________________________________________________

__________________________________________________________________________________________________________________

Create a Link
curl -X POST -d@post_link.json -H 'content-type: application/occi+json' --user user_1:pass -v http://localhost:8090/-/link/

Get a Link
curl -X GET -H 'content-type: application/occi+json' -v http://localhost:8090/-/link/{user-id}/{link-id}

Update a Link
curl -X PUT -d@up_link.json -H 'content-type: application/occi+json' --user user_1:pass -v http://localhost:8090/-/link/{user-id}/{link-id}

Delete a link
curl -X DELETE -H 'content-type: application/occi+json' -v http://localhost:8090/-/link/{user-id}/{link-id}

-----------------------------------------------------------------------------
5. For developers
-----------------------------------------------------------------------------

If you want export the use of your service through OCCI, two parts should be developped:
(1) the definition of the mixin with the list of attributes
(2) implementation of the specific service backend (CRUD operations)

-----------------------------------------------------------------------------
6. Licensing
-----------------------------------------------------------------------------

Copyright (C) 2011 Houssem Medhioub - Institut Telecom

This library is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this library.  If not, see <http://www.gnu.org/licenses/>.

-----------------------------------------------------------------------------
7. Contacts
-----------------------------------------------------------------------------

Houssem Medhioub:
houssem.medhioub@it-sudparis.eu

-----------------------------------------------------------------------------
8. Acknowledgment
-----------------------------------------------------------------------------
This work has been supported by:
     SAIL project (IST 7th Framework Programme Integrated Project) [http://sail-project.eu/]
     CompatibleOne Project (French FUI project) [http://compatibleone.org/]



-----------------------------------------------------------------------------
9. Todo
-----------------------------------------------------------------------------
This release of pyocni is experimental.

Some of pyocni's needs might be:

  - 

-----------------------------------------------------------------------------
10. json files to execute the HowTo use examples
-----------------------------------------------------------------------------

post_kind.json
-----------------

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

up_kind.json
-----------------
{

   "Description": {
       "kinds": [
           {
               "term": "compute",
               "title": "Compute Resource",
               "related": [
                   "http://schemas.ogf.org/occi/core#resource"
               ],
               "actions": [

               ],
               "attributes": {
                   "occi": {
                       "compute": {
                           "state": {
                               "default": "inactive",
                               "mutable": false,
                               "required": false,
                               "type": "string",
                               "pattern": "inactive|active|suspended|failed"
                           },
                           "hostname": {
                               "pattern": "(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\\\\-]*[a-zA-Z0-9])\\\\.)*",
                               "required": false,
                               "maximum": "255",
                               "minimum": "1",
                               "mutable": true,
                               "type": "string"
                           }
                       }
                   }
               },
               "scheme": "http://schemas.ogf.org/occi/infrastructure#",
               "location": "/compute/"
           }
       ]
   },
   "Creator": "user_2",
}

post_mixin.json
-----------------
{
            "mixins": [
                    {
                    "term": "medium",
                    "scheme": "http://example.com/template/resource#",
                    "title": "Medium VM",
                    "related": [
                        "http://schemas.ogf.org/occi/infrastructure#resource_tpl"
                    ],
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

up_mixin.json
-----------------
{
    "Description": {
        "mixins": [
            {
                "term": "medium",
                "scheme": "http://example.com/template/resource#",
                "title": "Large VM",
                "related": [
                    "http://schemas.ogf.org/occi/infrastructure#resource_tpl"
                ],
                "attributes": {
                    "occi": {
                        "compute": {
                            "speed": {
                                "type": "number",
                                "default": 3
                            }
                        }
                    }
                },
                "location": "/template/resource/medium/"
            }
        ]
    }
}
post_action.json
-----------------
{
            "actions": [
                    {
                    "term": "stop",
                    "scheme": "http://schemas.ogf.org/occi/infrastructure/compute/action#",
                    "title": "Stop Compute instance",
                    "attributes": {
                        "method": {
                            "mutable": true,
                            "required": false,
                            "type": "string",
                            "pattern": "graceful|acpioff|poweroff",
                            "default": "poweroff"
                        }
                    }
                }
            ]
}

up_action.json
-----------------
{
    "Description": {
        "actions": [
            {
                "attributes": {
                    "method": {
                        "default": "poweroff",
                        "mutable": true,
                        "required": false,
                        "type": "string",
                        "pattern": "graceful|acpioff|poweroff"
                    }
                },
                "term": "start",
                "scheme": "http://schemas.ogf.org/occi/infrastructure/compute/action#",
                "title": "start Compute instance"
            }
        ]
    }
}

post_resource.json
-----------------
{
        "resources": [
            {
                "kind": "http: //schemas.ogf.org/occi/infrastructure#compute",
                "mixins": [
                    "http: //schemas.opennebula.org/occi/infrastructure#my_mixin",
                    "http: //schemas.other.org/occi#my_mixin"
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
                "id": "996ad860-2a9a-504f-8861-aeafd0b2ae29",
                "title": "Compute resource",
                "summary": "This is a compute resource",
                "links": [
                    {
                        "target": "http://myservice.tld/storage/59e06cf8-f390-5093-af2e-3685be593",
                        "kind": "http: //schemas.ogf.org/occi/infrastructure#storagelink",
                        "attributes": {
                            "occi": {
                                "storagelink": {
                                    "deviceid": "ide: 0: 1"
                                }
                            }
                        },
                        "id": "391ada15-580c-5baa-b16f-eeb35d9b1122",
                        "title": "Mydisk"
                    }
                ]
            }
        ]
}
up_resource.json
-----------------
{
   "_id": "fb1cff2a-641c-47b2-ab50-0e340bce9cc2",
   "_rev": "2-8d02bacda9bcb93c8f03848191fd64f0",

}

post_link.json
-----------------
{
            "links": [
                    {
                    "kind": "http://schemas.ogf.org/occi/infrastructure#networkinterface",
                    "mixins": [
                        "http://schemas.ogf.org/occi/infrastructure/networkinterface#ipnetworkinterface"
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
                    "actions": [
                            {
                            "title": "Disable networkinterface",
                            "href": "/networkinterface/22fe83ae-a20f-54fc-b436-cec85c94c5e8?action=up",
                            "category": "http: //schemas.ogf.org/occi/infrastructure/networkinterface/action#"
                        }
                    ],
                    "id": "22fe83ae-a20f-54fc-b436-cec85c94c5e8",
                    "title": "Mynetworkinterface",
                    "target": "http: //myservice.tld/network/b7d55bf4-7057-5113-85c8-141871bf7635",
                    "source": "http: //myservice.tld/compute/996ad860-2a9a-504f-8861-aeafd0b2ae29"
                }
            ]
        }
up_link.json
-----------------
{
   "_id": "fb1cff2a-641c-47b2-ab50-0e340bce9cc2",
   "_rev": "2-8d02bacda9bcb93c8f03848191fd64f0",

}

DocumentSkeleton
-------------------

{
    "_id": "id value",
    "_rev": "rev value",
    "LastUpdate": "datetime",
    "CreationDate": "datetime",
    "OCCI_Description": {occi+json},
    "Creator": "creator login",
    "Location": "path to the document",
    "Provider": {
        "remote": [],
        "local": []
    },
    "Type": "Type of the OCCI description"
}