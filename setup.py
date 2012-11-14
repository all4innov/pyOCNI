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
Created on Jun 01, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@license: Apache License, Version 2.0
"""
import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='pyocni',
      author='Houssem Medhioub',
      author_email='houssem.medhioub@it-sudparis.eu',
      version='0.3',
      description='PyOCNI: A Python implementation of an extended OCCI with a JSON serialization',
      long_description=read('README'),
      url='http://www.example.com/pyocni',
      #packages=['pyocni'],
      packages=find_packages(), #['pyocni'],
      package_data = {
        # If any package contains *.txt or *.rst files, include them:
        'pyocni': ['*.conf', '*.py'],
        # And include any *.msg files found in the 'pyocni' package, too:
        'pyocni': ['*.conf', '*.msg'],
       },
      install_requires=[
          'config',
          'configobj',
          #'logging',
          'ordereddict',
          'simplejson',
          'jsonpickle',
          'routes',
          'webob',
          'pesto',
          'eventlet',
          'sphinx',
          'ZODB3',
          'httplib2',
          'couchdb',
          'couchdbkit',
          'tornado'
          #'pack>=0.97',
          #'pack'
      ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: Apache License, Version 2.0',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 2.7'
      ]
)
