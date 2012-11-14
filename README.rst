==========================================================
 pyOCNI - Python Open Cloud Networking Interface
==========================================================

:Version: 0.9
:Source: https://github.com/jordan-developer/pyOCNI
:Keywords: OCCI, OCNI, REST, Interface, HTTP, JSON, CouchDB, Eventlet, Webob, Cloud Computing, Cloud Networking

Developers
==========

Copyright (C) Houssem Medhioub <houssem.medhioub@it-sudparis.eu>

Copyright (C) Bilel Msekni <bilel.msekni@telecom-sudparis.eu>

Redistribution of this software is permitted under the terms of the Apache License, Version 2.0

Table of Contents
=================
::

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

pyOCNI (Python Open Cloud Networking Interface): A Python implementation of an extended OCCI server with a JSON/HTTP serialization and a Category Manager.

1. The Latest Version
=====================

version 0.9

2. API Documentation
====================
the api documentation are available through this html file: pyOCNI/pyocni/doc/index.html

3. Installation
===============

3.1. Requirements
-----------------
This software needs this packages to run:

* python <= 2.7
* python-all-dev (for eventlet/greenlet install/make)
* python-setuptools (to execute the setup.py file)
* couchdb >= 1.2.0:
Example of installing couchdb using build-couchdb on Ubuntu (more details on: https://github.com/iriscouch/build-couchdb)
::

    sudo apt-get install help2man make gcc zlib1g-dev libssl-dev rake help2man
    git clone git://github.com/iriscouch/build-couchdb
    cd build-couchdb
    git submodule init
    git submodule update
    rake
    build/bin/couchdb

To test CouchDB:       http://127.0.0.1:5984

To test CouchDB GUI:   http://127.0.0.1:5984/_utils/

3.2. Install
------------
::

   sudo python setup.py install

3.3. Configuration
------------------

* Logger configuration:  OCCILogging.conf
* Server configuration:  occi_server.conf
* CouchDB configuration: couchdb_server.conf

3.4. Server running
-------------------
::

   sudo python start.py


4. HowTo use
=====================================================================
In order to use pyOCNI, you must respect certain rules :

#. All requests/responses must follow the OCCI standard, any detected conflict will cancel the request.
#. Kinds, Mixins and Actions can be created, retrieved, updated or deleted (CRUD) on the fly.
#. Scheme + Term = OCCI_ID : unique identifier of the OCCI (Kind/Mixin/Action) description
#. PyOCNI_Server_Address + location = OCCI_Location of (Kind/Mixin/Action) description
#. location word refers to a kind or mixin location.

PyOCNI offers two OCCI rendering formats : **HTTP and JSON**. The following commands are JSON specific. If you want to see HTTP command please check here.

**Note:** To simplify the output, contents of the requests are available in section **json files to execute the HowTo**.


4.1. Category management
----------------------

1.Retrieval of all registered Categories (Kinds, Mixins and Actions)::

    curl -X GET -H 'content-type: application/occi+json' -H 'accept: application/occi+json' -v http://localhost:8090/-/

* Response::

   {
           "actions": [
               {
                   "term": "start",
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
           ],
           "kinds": [
               {
                   "term": "storage",
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
                   "location": "/storage/"
               }
           ],
           "mixins": [
               {
                   "term": "resource_tpl",
                   "scheme": "http://schemas.ogf.org/occi/infrastructure#",
                   "title": "Medium VM",
                   "related": [],
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
                   "location": "/template/resource/resource_tpl/"
               }
           ]
       }

2.Retrieval of specific Kinds, Mixins and Actions using filtering::

   curl -X GET -d@filter_categories.json -H 'content-type: application/occi+json' -H 'accept: application/occi+json' -v http://localhost:8090/-/

* Response::

   {
    "actions": [
        {
            "term": "start",
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
   
3.Update of Categories (Kinds and/or Mixins and/or Actions)::

   curl -X PUT -d@put_categories.json -H 'content-type: application/occi+json' -H 'accept: application/occi+json' -v http://localhost:8090/-/

* Response::

   N/A

4.Deletion of Categories (Kinds and/or Mixins and/or Actions)::

   curl -X DELETE -d@delete_categories.json -H 'content-type: application/occi+json' -H 'accept: application/occi+json' -v http://localhost:8090/-/

* Response::

   N/A


4.2. Path management
----------------------

1.Get Resources,Links and URLs below a path ::

   curl -X GET -H 'content-type: application/occi+json' -H 'accept: application/occi+json' -v http://localhost:8090/{path}

* Response::

   [
    "http://localhost:8090/{path}/vm3",
    "http://localhost:8090/{path}/fooVM",
    "http://localhost:8090/{path}/user/"
   ]

2.Get Resources and Links below a path::

   curl -X GET -H 'content-type: application/occi+json' -H 'accept: application/occi+json' -v http://localhost:8090/{primary}/{secondary}

* Response::

   {
    "X-OCCI-Location": [
       " http://localhost:8090/{primary}/{secondary}/vm1",
        "http://localhost:8090/{primary}/{secondary}/vm2",
        "http://localhost:8090/{primary}/{secondary}/vm3"
    ]
   }

3.Delete all Resources and Links below a path::

   curl -X DELETE -H 'content-type: application/occi+json' -H 'accept: application/occi+json' -v http://localhost:8090/{primary}/{secondary}

* Response::

   N/A

4.3. Multiple resource management
----------------------

1.Get multiple resources of a kind/mixin::
 
   curl -X GET -H 'content-type: application/occi+json' -H 'accept: application/occi+json' -v http://localhost:8090/{location}/

* Response::

       {
    "X-OCCI-Location": [
        http://localhost:8090/{location}/vm1",
        http://localhost:8090/{location}/vm2",
        http://localhost:8090/{location}/vm3"
    ]
   }

2.Get specific resources of a kind/mixin using filtering::

   curl -X GET -d@get_resources.json -H 'content-type: application/occi+json' -H 'accept: application/occi+json' -v http://localhost:8090/{location}/

* Response::

    {
    "X-OCCI-Location": [
        "http://localhost:8090/{location}/vm1",
        "http://localhost:8090/{location}/vm2"
    ]
   }

3.Create multiple resources of a kind::

   curl -X POST -d@post_resources.json -H 'content-type: application/occi+json' -H 'accept: application/occi+json' -v http://localhost:8090/{kind_location}/

* Response::

   {
    "Location": [
        "http://localhost:8090/{kind_location}/resource1_id",
        "http://localhost:8090/{kind_location}/resource2_id",
        "http://localhost:8090/{kind_location}/resource3_id"
    ]
   }

4.Trigger an action on multiple resources of a kind/mixin::

   curl -X POST -d@trigger_action.json -H 'content-type: application/occi+json' -H 'accept: application/occi+json' -v http://localhost:8090/{location}/?action={action_name}

* Response::

   N/A   

3.Associate a mixin to multiple resources::

   curl -X POST -d@associate_mixins.json -H 'content-type: application/occi+json' -H 'accept: application/occi+json' -v http://localhost:8090/{mixin_location}/

* Response::

   N/A

5.Full update of the mixin collection of multiple resources::

   curl -X PUT -d@update_mixins.json -H 'content-type: application/occi+json' -H 'accept: application/occi+json' -v http://localhost:8090/{mixin_location}/

* Response::

   N/A

6.Dissociate resource from mixins::

   curl -X DELETE -d@dissociate_mixin.json -H 'content-type: application/occi+json' -H 'accept: application/occi+json' -v http://localhost:8090/{mixin_location}/

* Response::
   
   N/A

4.4. Single resource management
----------------------

1.Create a Resource with a custom URL path::

   curl -X PUT -d@post_custom_resource.json -H 'content-type: application/occi+json' -H 'accept: application/occi+json' -v http://localhost:8090/{location}/{my_custom_resource_id}

* Response::

   N/A

2.Get a Resource::

   curl -X GET -H 'content-type: application/occi+json' -H 'accept: application/occi+json' -v http://localhost:8090/{location}/{resource-id}

* Response::

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

3.Full Update of a Resource::

   curl -X PUT -d@full_update_resource.json -H 'content-type: application/occi+json' -H 'accept: application/occi+json' -v http://localhost:8090/{location}/{resource-id}

* Response::

   {
    "X-OCCI-Location": [
        "http://localhost:8090/{kind}/resource1_id"
    ]
   }

4.Partial Update of a Resource::

   curl -X POST -d@partial_update_resource.json -H 'content-type: application/occi+json' -H 'accept: application/occi+json' -v http://localhost:8090/{location}/{resource-id}

   * Response::

   {
    "X-OCCI-Location": [
        "http://localhost:8090/{kind}/resource1_id"
    ]
   }

5.Trigger an action on a resource::

   curl -X POST -d@action_on_resource.json -H 'content-type: application/occi+json' -H 'accept: application/occi+json' -v http://localhost:8090/{location}/{resource-id}?action={action_name}

* Response::

   N/A

6.Delete a Resource::

   curl -X DELETE -H 'content-type: application/occi+json' -H 'accept: application/occi+json' -v http://localhost:8090/{location}/{resource-id}

* Response::

   N/A

5. For developers
=================

If you want export the use of your service through OCCI, two parts should be developped:

#. the definition of the kind, action, and mixin with the list of attributes
#. implementation of the specific service backend (CRUD operations)


6. Licensing
============

::

  Copyright 2010-2012 Institut Mines-Telecom

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.


7. Contacts
===========

Houssem Medhioub: houssem.medhioub@it-sudparis.eu

Bilel Msekni: bilel.msekni@telecom-sudparis.eu

Djamal Zeghlache: djamal.zeghlache@it-sudparis.eu

8. Acknowledgment
=================
This work has been supported by:

* SAIL project (IST 7th Framework Programme Integrated Project) [http://sail-project.eu/]
* CompatibleOne Project (French FUI project) [http://compatibleone.org/]


9. Todo
=======
This release of pyocni is experimental.

Some of pyocni's needs might be:

*

10. JSON example files of the HowTo 
===================================

* filter_categories.json::

      {
       "actions": [
           {
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

* put_categories.json::

   {
       "mixins": [
           {
               "term": "resource_tpl",
               "scheme": "http: //schemas.ogf.org/occi/infrastructure#",
               "title": "MediumVM",
               "related": [],
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
               "location": "/template/resource/resource_tpl/"
           }
       ]
   }

* delete_categories.json::

   {
       "kinds": [
           {
               "term": "storage",
               "scheme": "http: //schemas.ogf.org/occi/infrastructure#"
           }
       ]
   }

* get_resources.json::

   {
       "resources": [
           {
               "attributes": {
                   "occi": {
                       "compute": {
                           "speed": 2,
                           "memory": 4,
                           "cores": 2
                       }
                   }
               }
           }
       ]
   }

* post_resources.json::

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
                   }
               },
               "id": "996ad860-2a9a-504f-8861-aeafd0b2ae29",
               "title": "Compute resource",
               "summary": "This is a compute resource"
           }
       ]
   }

* trigger_action.json::

   {
       "actions": [
           {
               "term": "start",
               "scheme": "http://schemas.ogf.org/occi/infrastructure/compute/action#"
           }
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
       }
   }

* associate_mixin.json::

    {
    "X-OCCI-Location": [
        "http://localhost:8090/{location1}/vm1",
        "http://localhost:8090/{location2}/vm2"
    ]
   }

* update_mixins.json::

   {
       "X-OCCI-Location": [
           "http://localhost:8090/{location1}/vm1",
           "http://localhost:8090/{location2}/vm2"
       ]
   }

* dissociate_mixins.json::

   {
       "X-OCCI-Location": [
           "http://localhost:8090/{location1}/vm1",
           "http://localhost:8090/{location2}/vm2"
       ]
      }

* post_custom_resource.json::

   {
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

* full_update_resource.json::

   {
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

* partial_update_resource.json::

    {
        "resources": [
            {
                "attributes": {
                    "occi": {
                        "compute": {
                            "speed": 5,
                            "cores": 2
                        }
                    }
                }
            }
        ]
    }
