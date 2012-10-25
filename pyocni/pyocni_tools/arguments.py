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

@author: Providence Salumu Munga
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@license: Apache License, Version 2.0
"""

from optparse import OptionParser

parser = OptionParser()
parser.add_option('-c', '--config_file',
                  default='./OCCILogging.conf',
                  help='Configuration file path',
                  type='string',
                  action='store',
                  dest='config_file')
parser.add_option('-o', '--output_file',
                  default='',
                  help='log file',
                  type='string',
                  action='store',
                  dest='output_file')
(options, args) = parser.parse_args()
Parameters = options
