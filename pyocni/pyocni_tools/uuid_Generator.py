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
Created on May 29, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@version: 0.1
@license: LGPL - Lesser General Public License
"""

import uuid


def get_UUID():

    """
    There are many ways to generate a uuid
    This example is using the generate random uuid method

    """
    _uuid=None
    _uuid=str(uuid.uuid4())
    return _uuid


if __name__== "__main__":
    _uuid=str(uuid.uuid4())
    print "New UUID = "+_uuid