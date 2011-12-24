# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

# Copyright (C) 2011 Houssem Medhioub - Institut Telecom
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
Created on Feb 25, 2011

@author: Providence Salumu Munga, Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Telecom - Telecom SudParis
@version: 0.1
@license: LGPL - Lesser General Public License
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
