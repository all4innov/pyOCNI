# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

# Copyright (C) 2011 Houssem Medhioub - Institut Mines-Telecom
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
Created on Nov 20, 2011

@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@version: 0.3
@license: LGPL - Lesser General Public License
"""

import pesto
from pesto import Response
import eventlet
from eventlet import wsgi

dispatcher = pesto.dispatcher_app()


@dispatcher.match('/-/', 'GET')
def all(request):
    return Response([
        'This is for getting all ...'
    ])


@dispatcher.match('/CloNeNode/<id:int>/', 'GET')
def CloNe(request, id):
    return Response([
        'This is a CloNeNode with ID: ' + str(id)
    ])

if __name__ == "__main__":
    wsgi.server(eventlet.listen(('', 8090)), dispatcher)

# to test that:
#                  curl -X GET -v http://127.0.0.1:8090/CloNeNode/1/
