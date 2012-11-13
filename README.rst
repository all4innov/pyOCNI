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

PyOCNI offers two OCCI rendering formats : HTTP and JSON. The following commands are JSON specific. If you want to see HTTP command please check here.

**Note:** To simplify the output, contents of the requests are available in section [**json files to execute the HowTo**]


4.1. Category management
----------------------

Retrieval of all registered Categories (Kinds, Mixins and Actions)::
   
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

Retrieval of specific Kinds, Mixins and Actions using filtering::

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
   
Update of Categories (Kinds and/or Mixins and/or Actions)::

   curl -X PUT -d@put_categories.json -H 'content-type: application/occi+json' -H 'accept: application/occi+json' -v http://localhost:8090/-/

* Response::

   200 OK

Deletion of Categories (Kinds and/or Mixins and/or Actions)::

   curl -X DELETE -d@delete_categories.json -H 'content-type: application/occi+json' -H 'accept: application/occi+json' -v http://localhost:8090/-/

* Response::

   200 OK

________________________________________________________________________________________________________________________

________________________________________________________________________________________________________________________

4.1. Kind management
----------------------

* Create Kinds::

   curl -X POST -d@post_kinds.json -H 'content-type: application/occi+json' -H 'accept: application/occi+json' -v 'http://localhost:8090/-/'

* Retrieval of a registered Kind::

   curl -X GET -H 'content-type: application/occi+json' -H 'accept: application/occi+json' -v http://localhost:8090/-/{resource}/

* Get Kinds with filetering::

   curl -X GET -d@get_kinds.json -H 'content-type: application/occi+json' -H 'accept: application/occi+json' -v http://localhost:8090/-/

* Update Kinds::

   curl -X PUT -d@put_kinds.json -H 'content-type: application/occi+json' -H 'accept: application/occi+json' -v http://localhost:8090/-/

* Update Kind providers::

   curl -X DELETE -d@put_providers.json -H 'content-type: application/occi+json' -H 'accept: application/occi+json' -v http://localhost:8090/-/

* Delete Kinds::

   curl -X DELETE -d@delete_kinds.json -H 'content-type: application/occi+json' -H 'accept: application/occi+json' -v http://localhost:8090/-/

________________________________________________________________________________________________________________________

________________________________________________________________________________________________________________________


* Get Resources,Links and URLs below a path ::

   curl -X GET -H 'content-type: application/occi+json' -H 'accept: application/occi+json'  -v http://localhost:8090/{path}

* Get Resources and Links below a path::

   curl -X GET -d@get_res_link_b_path.json -H 'content-type: application/occi+json' -H 'accept: application/occi+json'  -v http://localhost:8090/{primary}/{secondary}

* Delete all Resources and Links below a path::

   curl -X DELETE -H 'content-type: application/occi+json' -H 'accept: application/occi+json'  -v http://localhost:8090/{primary}/{secondary}

________________________________________________________________________________________________________________________

________________________________________________________________________________________________________________________

* Create Resources of a kind::

   curl -X POST -d@post_resources.json -H 'content-type: application/occi+json' -H 'accept: application/occi+json'  -v http://localhost:8090/{resource}/

* Create a Resource with a custom URL path::

   curl -X PUT -d@post_custom_resource.json -H 'content-type: application/occi+json' -H 'accept: application/occi+json'  -v http://localhost:8090/{resource}/{user_id}/{my_custom_resource_id}

* Get a Resource::

   curl -X GET -H 'content-type: application/occi+json' -H 'accept: application/occi+json'  -v http://localhost:8090/{resource}/{user-id}/{resource-id}

* Full Update a Resource::

   curl -X PUT -d@full_update_resource.json -H 'content-type: application/occi+json' -H 'accept: application/occi+json'  -v http://localhost:8090/{resource}/{user-id}/{resource-id}

* Partial Update a Resource::

   curl -X POST -d@partial_update_resource.json -H 'content-type: application/occi+json' -H 'accept: application/occi+json'  -v http://localhost:8090/{resource}/{user-id}/{resource-id}

* Delete a Resource::

   curl -X DELETE -H 'content-type: application/occi+json' -H 'accept: application/occi+json'  -v http://localhost:8090/{resource}/{user-id}/{resource-id}

________________________________________________________________________________________________________________________

________________________________________________________________________________________________________________________

* Create Links of a kind::

   curl -X POST -d@post_links.json -H 'content-type: application/occi+json' -H 'accept: application/occi+json'  -v http://localhost:8090/{link}/

* Create a Link with a custom resource path::

   curl -X PUT -d@post_custom_resource.json -H 'content-type: application/occi+json' -H 'accept: application/occi+json'  -v http://localhost:8090/{my_custom_link_path}

* Get a Link::

   curl -X GET -H 'content-type: application/occi+json' -H 'accept: application/occi+json'  -v http://localhost:8090/{link}/{user-id}/{link-id}

* Full update a Link::

   curl -X PUT -d@full_update_link.json -H 'content-type: application/occi+json' -H 'accept: application/occi+json'  -v http://localhost:8090/{link}/{user-id}/{link-id}

* Patial update a Link::

   curl -X POST -d@partial_update_link.json -H 'content-type: application/occi+json' -H 'accept: application/occi+json'  -v http://localhost:8090/{link}/{user-id}/{link-id}

* Delete a link::

   curl -X DELETE -H 'content-type: application/occi+json' -H 'accept: application/occi+json'  -v http://localhost:8090/{link}/{user-id}/{link-id}


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

10. json files to execute the HowTo use examples (available under client/request_examples folder)
=======================================================================

