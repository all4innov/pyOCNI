==========================================================
 pyocni - PyOCNI (Python Open Cloud Networking Interface)
==========================================================

:Version: 0.2

Developers
==========

Copyright (C) Houssem Medhioub <houssem.medhioub@it-sudparis.eu>

Copyright (C) Bilel Msekni <bilel.msekni@telecom-sudparis.eu>

Redistribution of this software is permitted under the terms of the **LGPL** License

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

PyOCNI (Python Open Cloud Networking Interface): A Python implementation of an extended OCCI with a JSON serialization and a cloud networking extension.


1. The Latest Version
=====================

version 0.2

11 Jan 2012

status: Still an ongoing work


2. API Documentation
====================
the api documentation are available through this html file:
PyOCNI/pyocni/doc/index.html

3. Installation
===============

3.1. Requirements
-----------------
This software needs this packages to run:

* python <= 2.7
* python-all-dev (for eventlet/greenlet install/make)
* python-setuptools (to execute the setup.py file)
* couchdbkit

3.2. Install
------------
sudo python setup.py install

3.3. Configuration
------------------

* Logger configuration:  OCCILogging.conf
* Server configuration:  occi_server.conf
* CouchDB configuration: couchdb_server.conf

3.4. Server running
-------------------
python start.py


4. HowTo use (examples. The json files are at the end of this README)
=====================================================================

In order to use PyOCNI, you must respect certain rules :

#. All data must follow the JSON format declared by OCCI [occi+json], any detected conflict will cancel the request.
#. Kinds, Mixins and Actions can be created, read, updated or deleted (CRUD) on the fly.
#. Kinds, Mixins and Actions can be read and created by anyone but updated and deleted by only their creator
#. Resources and Links can be created, read, updated or deleted(CRUD) on the fly.
#. Resources and Links can be read and created by anyone but updated and deleted by only their creator
#. Kinds, Mixins, Actions, Resources and Links have their own distinct storage format (see below)
#. The new data provided in an update request must be sent in consistency with the raw format
#. An update request is done through the update of the fields mentioned in the DocumentSkeleton (see below)

These are some commands that you can use with PyOCNI

__________________________________________________________________________________________________________________

Retrieval of all registered Kinds, Mixins and Actions:
::

   curl -X GET -H 'accept: application/json:occi' -v http://localhost:8090/-/