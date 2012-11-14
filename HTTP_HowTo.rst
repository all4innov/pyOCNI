==========================================================
 pyOCNI - HTTP rendering HowTo
==========================================================

:Version: 0.9
:Source: https://github.com/jordan-developer/pyOCNI
:Keywords: OCCI, OCNI, REST, Interface, HTTP, JSON, CouchDB, Eventlet, Webob, Cloud Computing, Cloud Networking

Developers
==========

Copyright (C) Houssem Medhioub <houssem.medhioub@it-sudparis.eu>

Copyright (C) Bilel Msekni <bilel.msekni@telecom-sudparis.eu>

Redistribution of this software is permitted under the terms of the Apache License, Version 2.0

0. What is it?
==============

Using pyOCNI with HTTP rendering format.

1. The Latest Version
=====================

version 0.9

2. API Documentation
====================
the api documentation are available through this html file: pyOCNI/pyocni/doc/index.html

4. HowTo use
=====================================================================
In order to use pyOCNI, you must respect certain rules :

#. All requests/responses must follow the OCCI standard, any detected conflict will cancel the request.
#. Kinds, Mixins and Actions can be created, retrieved, updated or deleted (CRUD) on the fly.
#. Scheme + Term = OCCI_ID : unique identifier of the OCCI (Kind/Mixin/Action) description
#. PyOCNI_Server_Address + location = OCCI_Location of (Kind/Mixin/Action) description
#. location word refers to a kind or mixin location.

 PyOCNI supports both OCCI HTTP rendering formats : **text/plain** and **text/occi**. The difference between these two
 formats is that the response will be inside the body for the text/plain while it will be inside the headers for the text/occi.
 It's up to the user to define what format he wants in the request Content-Type header.

**Note:** To simplify the output, contents of the requests are using the text/plain format and available under section **HTTP files to execute the HowTo**.


4.1. Category management
----------------------

1.Retrieval of all registered Categories (Kinds, Mixins and Actions)::

    curl -X GET -H 'accept: text/plain' -v http://localhost:8090/-/

* Response::

   Category: compute;
        scheme="http://schemas.ogf.org/occi/infrastructure#";
        class="kind";
        title="Compute Resource type";
        rel="http://schemas.ogf.org/occi/core#resource";
        attributes="occi.compute.cores occi.compute.state{immutable} ...";
        actions="http://schemas.ogf.org/occi/infrastructure/compute/action#stop ...";
        location="http://example.com/compute/"

   Category: start;
        scheme="http://schemas.ogf.org/occi/infrastructure/compute/action#";
        class="action";
        title="Start Compute Resource";
        attributes="method"

   Category: stop;
        scheme="http://schemas.ogf.org/occi/infrastructure/compute/action#";
        class="action";
        title="Stop Compute Resource";
        attributes="method"

   Category: my_stuff;
        scheme="http://example.com/occi/my_stuff#";
        class="mixin";
        location="http://example.com/my_stuff/"


2.Retrieval of specific categories (Kinds, Mixins and Actions) using filtering::

   curl -X GET -d@filter_categories -H 'content-type: text/plain' -H 'accept: text/plain' -v http://localhost:8090/-/

* Response::

   Category: stop;
           scheme="http://schemas.ogf.org/occi/infrastructure/compute/action#";
           class="action";
           title="Stop Compute Resource";
           attributes="method"

5.Adding a category (Kind or Mixin or Action)::

    curl -X POST -d@post_category -H 'content-type: text/plain' -H 'accept: text/plain' -v http://localhost:8090/-/

* Response::

   N/A

4.Full Update of a category (Kind or Mixin or Action)::

   curl -X PUT -d@put_category -H 'content-type: text/plain' -H 'accept: text/plain' -v http://localhost:8090/-/

* Response::

   N/A

5.Deletion of a category (Kind or Mixins or Actions)::

   curl -X DELETE -d@delete_category -H 'content-type: text/plain' -H 'accept: text/plain' -v http://localhost:8090/-/

* Response::

   N/A

4.2. Path management
----------------------

1.Get Resources,Links and URLs below a path ::

   curl -X GET -H 'accept: text/plain' -v http://localhost:8090/{path}

* Response::

   http://localhost:8090/{path}/vm3
   http://localhost:8090/{path}/fooVM
   http://localhost:8090/{path}/user/

2.Get Resources and Links below a path::

   curl -X GET -H 'accept: text/plain' -v http://localhost:8090/{primary}/{secondary}

* Response::

    X-OCCI-Location: http://localhost:8090/{primary}/{secondary}/vm1
    X-OCCI-Location: http://localhost:8090/{primary}/{secondary}/vm2
    X-OCCI-Location: http://localhost:8090/{primary}/{secondary}/vm3

3.Delete all Resources and Links below a path::

   curl -X DELETE -H 'accept: text/plain' -v http://localhost:8090/{primary}/{secondary}

* Response::

   N/A

4.3. Multiple resource management
----------------------

1.Get multiple resources of a kind/mixin::

   curl -X GET -H 'accept: text/plain' -v http://localhost:8090/{location}/

* Response::

    X-OCCI-Location: http://localhost:8090/{location}/vm1
    X-OCCI-Location: http://localhost:8090/{location}/vm2
    X-OCCI-Location: http://localhost:8090/{location}/vm3

2.Get specific resources of a kind/mixin using filtering::

   curl -X GET -d@get_resources -H 'content-type: text/plain' -H 'accept: text/plain' -v http://localhost:8090/{location}/

* Response::

    X-OCCI-Location: http://localhost:8090/{location}/vm1
    X-OCCI-Location: http://localhost:8090/{location}/vm2

3.Create a resource of a kind::

   curl -X POST -d@post_resource -H 'content-type: text/plain' -H 'accept: text/plain' -v http://localhost:8090/{kind_location}/

* Response::

        Location: http://localhost:8090/{kind_location}/resource1_id

4.Trigger an action on multiple resources of a kind/mixin::

   curl -X POST -d@trigger_action.json -H 'content-type: text/plain' -H 'accept: text/plain' -v http://localhost:8090/{location}/?action={action_name}

* Response::

   N/A

3.Associate a mixin to multiple resources::

   curl -X POST -d@associate_mixins.json -H 'content-type: text/plain' -H 'accept: text/plain' -v http://localhost:8090/{mixin_location}/

* Response::

   N/A

5.Full update of the mixin collection of multiple resources::

   curl -X PUT -d@update_mixins.json -H 'content-type: text/plain' -H 'accept: text/plain' -v http://localhost:8090/{mixin_location}/

* Response::

   N/A

6.Dissociate resource from mixins::

   curl -X DELETE -d@dissociate_mixin.json -H 'content-type: text/plain' -H 'accept: text/plain' -v http://localhost:8090/{mixin_location}/

* Response::

   N/A

4.4. Single resource management
----------------------

1.Create a Resource with a custom URL path::

   curl -X PUT -d@post_custom_resource.json -H 'content-type: text/plain' -H 'accept: text/plain' -v http://localhost:8090/{location}/{my_custom_resource_id}

* Response::

   N/A

2.Get a Resource::

   curl -X GET -H 'content-type: text/plain' -H 'accept: text/plain' -v http://localhost:8090/{location}/{resource-id}

* Response::

     Category: compute;
      scheme="http://schemas.ogf.org/occi/infrastructure#"
      class="kind";
     Link: </users/foo/compute/b9ff813e-fee5-4a9d-b839-673f39746096?action=start>;
      rel="http://schemas.ogf.org/occi/infrastructure/compute/action#start"
     X-OCCI-Attribute: occi.core.id="urn:uuid:b9ff813e-fee5-4a9d-b839-673f39746096"
     X-OCCI-Attribute: occi.core.title="My Dummy VM"
     X-OCCI-Attribute: occi.compute.architecture="x86"
     X-OCCI-Attribute: occi.compute.state="inactive"
     X-OCCI-Attribute: occi.compute.speed=1.33
     X-OCCI-Attribute: occi.compute.memory=2.0
     X-OCCI-Attribute: occi.compute.cores=2
     X-OCCI-Attribute: occi.compute.hostname="dummy"

3.Full Update of a Resource::

   curl -X PUT -d@full_update_resource -H 'content-type: text/plain' -H 'accept: text/plain' -v http://localhost:8090/{location}/{resource-id}

* Response::

    X-OCCI-Location: http://localhost:8090/{location}/{resource-id}

4.Partial Update of a Resource::

   curl -X POST -d@partial_update_resource -H 'content-type: text/plain' -H 'accept: text/plain' -v http://localhost:8090/{location}/{resource-id}

   * Response::

   {
    "X-OCCI-Location": [
        "http://localhost:8090/{location}/{resource-id}"
    ]
   }

5.Trigger an action on a resource::

   curl -X POST -d@action_on_resource -H 'content-type: text/plain' -H 'accept: text/plain' -v http://localhost:8090/{location}/{resource-id}?action={action_name}

* Response::

   N/A

6.Delete a Resource::

   curl -X DELETE -H 'content-type: text/plain' -H 'accept: text/plain' -v http://localhost:8090/{location}/{resource-id}

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

      Category: my_stuff;
        scheme="http://example.com/occi/my_stuff#";
        class="mixin";


* post_categories::

   Category: compute;
           scheme="http://schemas.ogf.org/occi/infrastructure#";
           class="kind";
           title="Compute Resource type";
           rel="http://schemas.ogf.org/occi/core#resource";
           attributes="occi.compute.cores occi.compute.state{immutable} ...";
           actions="http://schemas.ogf.org/occi/infrastructure/compute/action#stop ...";
           location="http://example.com/compute/"

* put_categories::

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
