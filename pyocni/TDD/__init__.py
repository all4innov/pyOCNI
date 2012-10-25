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
Created on Feb 25, 2011

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@license: Apache License, Version 2.0
"""

import eventlet.patcher

httplib2 = eventlet.patcher.import_patched("httplib2")

import pprint

if __name__ == '__main__':
    h = httplib2.Http(".cache")
    #h.add_credentials('name', 'password')

    #    ====== Retrieval of all registered Kinds and Mixins  ======
    #curl -X GET -H 'accept: application/occi+json' -v http://127.0.0.1:8090/-/

    print ('========================================================================================================')
    print ('sending the request: Retrieval of all registered Kinds and Mixins...')
    resp, content = h.request('http://127.0.0.1:8090/-/',
        'GET',
        headers={'content-type': 'application/occi+json', 'accept': 'application/occi+json'},
        body='')
    print('********** The response header **********')
    pprint.pprint(resp)
    print('********** The content **********')
    print(content)

    #    ================= Creation of Resource instance (Compute) =================
    # curl -X POST -d@post_compute.json -H 'content-type: application/occi+json' -v http://157.159.249.133:8090/compute/
    #print ('========================================================================================================')
    #print ('sending the request: Creation of Resource instance (compute) ')
    #resp, content = h.request('http://157.159.249.33:8090/compute/',
    #                         'POST',
    #                          headers={'content-type': 'application/occi+json', 'accept': 'application/occi+json'},
    #                          body='''
#    {
#        "kind": {
#            "term": "compute",
#            "scheme": "http://schemas.ogf.org/occi/infrastructure",
#            "class": "kind"
#        },
#        "occi.core.id": "compute107",
#        "occi.core.title": "compute107 created by Houssem",
#        "occi.core.summary": "a summary of Compute 107 resource",
#        "mixins": [ ],
#        "links": ["a", "b"],
#        "attributes": {
#            "occi.compute.architecture": "x86_64",
#            "occi.compute.state": "active",
#            "occi.compute.speed": 1.0,
#            "occi.compute.memory": 512,
#            "occi.compute.cores": 1,
#            "occi.compute.hostname": "compute107"
#        }
#    }
#    ''')
#
#    print('********** The response header **********')
#    pprint.pprint(resp)
#    print('********** The content **********')
#    print(content)
#
#    #    ================= Creation of Resource instance (network) with ipnetwork mixin  =================
#    #    curl -X POST -d@post_network_ipnetwork.json -H 'content-type: application/occi+json' -v http://157.159.249.133:8090/network/
#    print ('========================================================================================================')
#    print ('sending the request: Creation of Resource instance (network) with ipnetwork mixin ')
#    resp, content = h.request('http://127.0.0.1:8090/network/',
#                              'POST',
#                              headers={'content-type': 'application/occi+json', 'accept': 'application/occi+json'},
#                              body='''
#    {
#        "kind": {
#            "term": "network",
#            "scheme": "http://schemas.ogf.org/occi/infrastructure",
#            "class": "kind"
#        },
#        "occi.core.id": "network10",
#        "occi.core.title": "network10 created by Houssem",
#        "occi.core.summary": "a summary of Network 10 resource",
#        "mixins": [
#            {
#            "term": "ipnetwork",
#            "scheme": "http://schemas.ogf.org/occi/infrastructure/network",
#            "class": "mixin"
#            }
#        ],
#        "links": [],
#        "attributes": {
#            "occi.network.vlan": "10",
#            "occi.network.label": "dmz",
#            "occi.network.state": "active",
#            "occi.network.address": "192.168.1.1",
#            "occi.network.gateway": "192.168.1.1",
#            "occi.network.allocation": "dynamic"
#        }
#    }
#    ''')
#
#    print('********** The response header **********')
#    pprint.pprint(resp)
#    print('********** The content **********')
#    print(content)
#
#    #    ================= Creation of Resource instance (CloNeNode) =================
#    #    curl -X POST -d@post_clonenode.json -H 'content-type: application/occi+json' -v http://157.159.249.133:8090/clonenode/
#    print ('========================================================================================================')
#    print ('sending the request: Creation of Resource instance (CloNeNode) ')
#    resp, content = h.request('http://127.0.0.1:8090/CloNeNode/',
#                              'POST',
#                              headers={'content-type': 'application/occi+json', 'accept': 'application/occi+json'},
#                              body='''
#    {
#        "kind": {
#            "term": "CloNeNode",
#            "scheme": "http://schemas.ogf.org/occi/ocni",
#            "class": "kind"
#        },
#        "occi.core.id": "CloNeNode10",
#        "occi.core.title": "CloNeNode10",
#        "occi.core.summary": "CloNeNode created by Houssem",
#        "mixins": [
#        ],
#        "links": ["a", "b"],
#        "attributes": {
#            "ocni.clonenode.availability":[
#                {
#                    "ocni.availability.start":"08:00",
#                    "ocni.availability.end":"12:30"
#                },
#                {
#                    "ocni.availability.start":"14:00",
#                    "ocni.availability.end":"18:00"
#                }
#            ],
#            "ocni.clonenode.location": "EU",
#            "ocni.clonenode.state": "active"
#        }
#    }
#    ''')
#
#    print('********** The response header **********')
#    pprint.pprint(resp)
#    print('********** The content **********')
#    print(content)
#
#    #    ================= Creation of Resource instance (CloNeNode) with openFlow Mixin =================
#    #    curl -X POST -d@post_clonenode_openflow.json -H 'content-type: application/occi+json' -v http://157.159.249.133:8090/clonenode/
#
#    print ('========================================================================================================')
#    print ('sending the request: Creation of Resource instance (CloNeNode) with openFlow Mixin')
#    resp, content = h.request('http://127.0.0.1:8090/CloNeNode/',
#                              'POST',
#                              headers={'content-type': 'application/occi+json', 'accept': 'application/occi+json'},
#                              body='''
#    {
#        "kind": {
#            "term": "CloNeNode",
#            "scheme": "http://schemas.ogf.org/occi/ocni",
#            "class": "kind"
#        },
#        "occi.core.id": "CloNeNode20",
#        "occi.core.title": "CloNeNode20",
#        "occi.core.summary": "CloNeNode with openflow mixin created by Houssem",
#        "mixins": [
#            {
#                "term": "OpenFlowCloNeNode",
#                "scheme": "http://schemas.ogf.org/occi/ocni",
#                "class": "mixin"
#            }
#        ],
#        "links": [],
#        "attributes": {
#            "ocni.clonenode.availability":[
#                {
#                    "ocni.availability.start":"08:00",
#                    "ocni.availability.end":"12:30"
#                },
#                {
#                    "ocni.availability.start":"14:00",
#                    "ocni.availability.end":"18:00"
#                }
#            ],
#            "ocni.clonenode.location": "EU",
#            "ocni.clonenode.state": "active",
#            "ocni.openflowclonenode.datapath_id" : "0x004E46324304",
#            "ocni.openflowclonenode.ports" : ["6632","245"],
#            "ocni.openflowclonenode.of_controller" : ["192.168.10.2","192.168.10.2"],
#            "ocni.openflowclonenode.of_controller_port" : "6633"
#        }
#    }
#    ''')
#
#    print('********** The response header **********')
#    pprint.pprint(resp)
#    print('********** The content **********')
#    print(content)
#
#    #    ================= Creation of Resource resource instance (CloNeLink) =================
#    #    curl -X POST -H 'accept: application/occi+json' -v http://127.0.0.1:8090/CloNeLink/
#    """
#
#    """
#
#    #    ================= Creation of Resource instance (CloNeLink) with l3vpn Mixin =================
#    #    curl -X POST -d@post_clonelink_l3vpn.json -H 'content-type: application/occi+json' -v http://157.159.249.133:8090/clonelink/
#    print ('========================================================================================================')
#    print ('sending the request: Creation of Resource instance (CloNeLink) with l3vpn Mixin')
#    resp, content = h.request('http://127.0.0.1:8090/CloNeLink/',
#                              'POST',
#                              headers={'content-type': 'application/occi+json', 'accept': 'application/occi+json'},
#                              body='''
#    {
#       "kind":{
#          "term":"CloNeLink",
#          "scheme":"http://schemas.ogf.org/occi/ocni",
#          "class":"kind"
#       },
#       "occi.core.id":"CloNeLink30",
#       "occi.core.title":"CloNeLink30",
#       "occi.core.summary":"CloNeLink with l3vpn mixin created by Houssem",
#       "mixins":[
#          {
#             "term":"L3VPN",
#             "scheme":"http://schemas.ogf.org/occi/ocni",
#             "class":"mixin"
#          }
#       ],
#       "links":[
#
#       ],
#       "attributes":{
#          "ocni.clonelink.availability":[
#             {
#                "ocni.availability.start":"08:00",
#                "ocni.availability.end":"12:30"
#             },
#             {
#                "ocni.availability.start":"14:00",
#                "ocni.availability.end":"18:00"
#             }
#          ],
#          "ocni.clonelink.state":"active",
#          "ocni.clonelink.bandwidth":"100Mbps",
#          "ocni.clonelink.latency":"100ms",
#          "ocni.clonelink.jitter":"",
#          "ocni.clonelink.loss":"0.01%",
#          "ocni.clonelink.routing_scheme":"unicast",
#          "ocni.l3vpn.infrastructure_request_id":"2222",
#          "ocni.l3vpn.customer_id":"0987",
#          "ocni.l3vpn.service_type":{
#             "ocni.l3vpn.service_type.type":"CaaS",
#             "ocni.l3vpn.service_type.layer":"L2",
#             "ocni.l3vpn.service_type.class_of_service":"guaranteed"
#          },
#          "ocni.l3vpn.service_description":[
#             {
#                "ocni.l3vpn.service_description.endpoint_id":"0987",
#                "ocni.l3vpn.service_description.in_bandwidth":"100Mbps",
#                "ocni.l3vpn.service_description.out_bandwidth":"100Mbps",
#                "ocni.l3vpn.service_description.max_in_bandwidth":"120Mbps",
#                "ocni.l3vpn.service_description.max_out_bandwidth":"120Mbps",
#                "ocni.l3vpn.service_description.latency":"100ms",
#                "ocni.l3vpn.service_description.max_latency":"200ms"
#             },
#             {
#                "ocni.l3vpn.service_description.endpoint_id":"1001",
#                "ocni.l3vpn.service_description.in_bandwidth":"100Mbps",
#                "ocni.l3vpn.service_description.out_bandwidth":"100Mbps",
#                "ocni.l3vpn.service_description.max_in_bandwidth":"120Mbps",
#                "ocni.l3vpn.service_description.max_out_bandwidth":"120Mbps",
#                "ocni.l3vpn.service_description.latency":"100ms",
#                "ocni.l3vpn.service_description.max_latency":"200ms"
#             }
#          ],
#          "ocni.l3vpn.elastisity":{
#             "ocni.l3vpn.elastisity.supported":"yes",
#             "ocni.l3vpn.elastisity.reconfiguration_time":"120s"
#          },
#          "ocni.l3vpn.scalability":{
#             "ocni.l3vpn.scalability.supported":"yes",
#             "ocni.l3vpn.scalability.setup_time":"10s"
#          }
#       }
#    }
#    ''')
#
#    print('********** The response header **********')
#    pprint.pprint(resp)
#    print('********** The content **********')
#    print(content)
#
#    #    ================= Retrieval of Resource instance (compute) =================
#    #    curl -X GET -H 'accept: application/occi+json' -v http://127.0.0.1:8090/compute/user1/compute1
#    print ('========================================================================================================')
#    print ('sending the request: Retrieval of Resource instance (http://127.0.0.1:8090/compute/user1/compute1) ')
#    resp, content = h.request('http://127.0.0.1:8090/compute/user1/compute1',
#                              'GET',
#                              headers={'content-type': 'application/occi+json', 'accept': 'application/occi+json'},
#                              body='')
#    print('********** The response header **********')
#    pprint.pprint(resp)
#    print('********** The content **********')
#    print(content)
#
#    #    ================= Retrieval of Resource instance (CloNeNode) =================
#    #    curl -X GET -H 'accept: application/occi+json' -v http://127.0.0.1:8090/CloNeNode/user1/CloNeNode10
#
#    print ('========================================================================================================')
#    print ('sending the request: Retrieval of Resource instance (http://127.0.0.1:8090/CloNeNode/user1/CloNeNode20) ')
#    resp, content = h.request('http://127.0.0.1:8090/CloNeNode/user1/CloNeNode20',
#                              'GET',
#                              headers={'content-type': 'application/occi+json', 'accept': 'application/occi+json'},
#                              body='')
#    print('********** The response header **********')
#    pprint.pprint(resp)
#    print('********** The content **********')
#    print(content)
#
#    #    ================= Retrieval of Resource instance (CloNeLink) =================
#    #    curl -X GET -H 'accept: application/occi+json' -v http://127.0.0.1:8090/CloNeLink/user1/CloNeLink30
#    print ('========================================================================================================')
#    print ('sending the request: Retrieval of Resource instance (http://127.0.0.1:8090/CloNeLink/user1/CloNeLink30) ')
#    resp, content = h.request('http://127.0.0.1:8090/CloNeLink/user1/CloNeLink30',
#                              'GET',
#                              headers={'content-type': 'application/occi+json', 'accept': 'application/occi+json'},
#                              body='')
#    print('********** The response header **********')
#    pprint.pprint(resp)
#    print('********** The content **********')
#    print(content)
#
#    #    ================= Retrieval of all resource instance below a path =================
#    #    curl -X GET -H 'accept: application/occi+json' -v http://127.0.0.1:8090/compute/user1/
#
#    print ('========================================================================================================')
#    print (
#        'sending the request: Retrieval of all Resource instances below a path (http://127.0.0.1:8090/CloNeNode/user1/) ')
#    resp, content = h.request('http://127.0.0.1:8090/CloNeNode/user1/',
#                              'GET',
#                              headers={'content-type': 'application/occi+json', 'accept': 'application/occi+json'},
#                              body='')
#    print('********** The response header **********')
#    pprint.pprint(resp)
#    print('********** The content **********')
#    print(content)

"""
======================================================================================================================
======================================================================================================================
======================================================================================================================
houssem-Latitude[02:58:08]houssem~$ curl -X GET -H 'accept: application/occi+json' -v http://127.0.0.1:8090/-/
* About to connect() to 127.0.0.1 port 8090 (#0)
*   Trying 127.0.0.1... connected
* Connected to 127.0.0.1 (127.0.0.1) port 8090 (#0)
> GET /-/ HTTP/1.1
> User-Agent: curl/7.21.6 (x86_64-pc-linux-gnu) libcurl/7.21.6 OpenSSL/1.0.0e zlib/1.2.3.4 libidn/1.22 librtmp/2.3
> Host: 127.0.0.1:8090
> accept: application/occi+json
>
< HTTP/1.1 200 OK
< Content-Type: application:occi+json; charset=UTF-8
< Server: ocni-server/1.1 (linux) OCNI/1.1
< Content-Length: 4072
< Date: Sat, 26 Nov 2011 01:58:18 GMT
<
[
    {
        "term": "network",
        "title": "network resource",
        "actions": [
            "http://schemas.ogf/occi/infrastructure/network/action#up",
            "http://schemas.ogf/occi/infrastructure/network/action#down"
        ],
        "location": "/network/",
        "rel": [
            "http://schemas.ogf.org/occi/core#resource"
        ],
        "attributes": [
            "occi.network.vlan",
            "occi.network.label",
            "occi.network.state"
        ],
        "scheme": "http://schemas.ogf.org/occi/infrastructure",
        "class": "kind"
    },
    {
        "term": "storage",
        "title": "storage resource",
        "actions": [
            "http://schemas.ogf/occi/infrastructure/storage/action#online",
            "http://schemas.ogf/occi/infrastructure/storage/action#offline",
            "http://schemas.ogf/occi/infrastructure/storage/action#backup",
            "http://schemas.ogf/occi/infrastructure/storage/action#snapshot",
            "http://schemas.ogf/occi/infrastructure/storage/action#resize"
        ],
        "location": "/storage/",
        "rel": [
            "http://schemas.ogf.org/occi/core#resource"
        ],
        "attributes": [
            "occi.storage.size",
            "occi.storage.state"
        ],
        "scheme": "http://schemas.ogf.org/occi/infrastructure",
        "class": "kind"
    },
    {
        "term": "networkinterface",
        "title": "network interface link",
        "actions": [],
        "location": "/networkinterface/",
        "rel": [
            "http://schemas.ogf.org/occi/core#link"
        ],
        "attributes": [
            "occi.networkinterface.interface",
            "occi.networkinterface.mac",
            "occi.networkinterface.state"
        ],
        "scheme": "http://schemas.ogf.org/occi/infrastructure",
        "class": "kind"
    },
    {
        "term": "storagelink",
        "title": "storage link",
        "actions": [],
        "location": "/storagelink/",
        "rel": [
            "http://schemas.ogf.org/occi/core#link"
        ],
        "attributes": [
            "occi.storagelink.deviceid",
            "occi.storagelink.mountpoint",
            "occi.storagelink.state"
        ],
        "scheme": "http://schemas.ogf.org/occi/infrastructure",
        "class": "kind"
    },
    {
        "term": "compute",
        "title": "compute resource",
        "actions": [
            "http://schemas.ogf/occi/infrastructure/compute/action#start",
            "http://schemas.ogf/occi/infrastructure/compute/action#stop",
            "http://schemas.ogf/occi/infrastructure/compute/action#restart",
            "http://schemas.ogf/occi/infrastructure/compute/action#suspend"
        ],
        "location": "/compute/",
        "rel": [
            "http://schemas.ogf.org/occi/core#resource"
        ],
        "attributes": [
            "occi.compute.architecture",
            "occi.compute.cores",
            "occi.compute.hostname",
            "occi.compute.speed",
            "occi.compute.memory",
            "occi.compute.state"
        ],
        "scheme": "http://schemas.ogf.org/occi/infrastructure",
        "class": "kind"
    },
    {
        "term": "ipnetwork",
        "title": "ip network mixin",
        "actions": [],
        "location": "/ipnetworking/",
        "rel": [],
        "attributes": [
            "occi.network.address",
            "occi.network.gateway",
            "occi.network.allocation"
        ],
        "scheme": "http://schemas.ogf.org/occi/infrastructure/network",
        "class": "mixin"
    },
    {
        "term": "ipnetworkinterface",
        "title": "ip network interface mixin",
        "actions": [],
        "location": "/ipnetworkinterface/",
        "rel": [],
        "attributes": [
            "occi.networkinterface.address",
            "occi.networkinterface.gateway",
            "occi.networkinterface.allocation"
        ],
        "scheme": "http://schemas.ogf.org/occi/infrastructure/networkinterface",
        "class": "mixin"
    }
* Connection #0 to host 127.0.0.1 left intact
* Closing connection #0
]


======================================================================================================================
======================================================================================================================
======================================================================================================================

houssem-Latitude[02:59:30]houssem~$ curl -X GET -H 'accept: application/occi+json' -v http://127.0.0.1:8090/compute/user1/compute1
* About to connect() to 127.0.0.1 port 8090 (#0)
*   Trying 127.0.0.1... connected
* Connected to 127.0.0.1 (127.0.0.1) port 8090 (#0)
> GET /compute/user1/compute1 HTTP/1.1
> User-Agent: curl/7.21.6 (x86_64-pc-linux-gnu) libcurl/7.21.6 OpenSSL/1.0.0e zlib/1.2.3.4 libidn/1.22 librtmp/2.3
> Host: 127.0.0.1:8090
> accept: application/occi+json
>
< HTTP/1.1 200 OK
< Content-Type: application:occi+json; charset=UTF-8
< Server: ocni-server/1.1 (linux) OCNI/1.1
< Content-Length: 629
< Date: Sat, 26 Nov 2011 01:59:37 GMT
<
{
    "kind": {
        "term": "compute",
        "scheme": "http://schemas.ogf.org/occi/infrastructure",
        "class": "kind",
        "title": "compute resource"
    },
    "occi.core.title": "compute1 created by Houssem",
    "links": [],
    "occi.core.summary": "",
    "mixins": [],
    "location": "/compute/user1/compute1",
    "attributes": {
        "occi.compute.architecture": "",
        "occi.compute.state": "active",
        "occi.compute.speed": 0.0,
        "occi.compute.memory": 0,
        "occi.compute.cores": 0,
        "occi.compute.hostname": ""
    },
    "occi.core.id": "/compute/user1/compute1"
* Connection #0 to host 127.0.0.1 left intact
* Closing connection #0
}

======================================================================================================================
======================================================================================================================
======================================================================================================================


"""""
