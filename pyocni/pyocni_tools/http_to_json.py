# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

# Copyright (C) 2012 Houssem Medhioub - Institut Mines-Telecom
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
Created on Jul 13, 2012

@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@version: 0.3
@license: LGPL - Lesser General Public License
"""

import pprint

try:
    import simplejson as json
except ImportError:
    import json

class http_json(object):
    """

    This class is used to convert between OCCI http object and OCCI JSON object

    """

    def attribute_from_http_to_json(self, attribute='', json_result={}):
        """

        method to convert and add one OCCI HTTP attribute to an OCCI JSON object

        # the attribute 'attribute' contains the OCCI HTTP Attribute. e.g. 'occi.compute.hostname="foobar"'
        # the attribute 'json_result' contains an OCCI JSON object. e.g. {} or {'occi': {'compute': {'cores': 2, 'hostname': 'foobar'}}}
        """

        pprint.pprint(" =============== Getting ===============")
        pprint.pprint('the get attribute : ' + attribute)
        print('the get json : ' + str(json_result))

        attribute_partitioned = attribute.partition('=')
        attribute_name = attribute_partitioned[0]
        attribute_value = attribute_partitioned[2]
        pprint.pprint('the attribute name : ' + attribute_name)
        pprint.pprint('the attribute value : ' + attribute_value)

        attribute_name_partitioned = attribute_name.split('.')
        pprint.pprint(attribute_name_partitioned)

        a = json_result
        for i in range(len(attribute_name_partitioned)):
            if a.has_key(attribute_name_partitioned[i]):
                if i < (len(attribute_name_partitioned) - 1):
                    a = a[attribute_name_partitioned[i]]
                else:
                    a[attribute_name_partitioned[i]] = json.loads(attribute_value)
            else:
                if i < (len(attribute_name_partitioned) - 1):
                    a[attribute_name_partitioned[i]] = {}
                    a = a[attribute_name_partitioned[i]]
                    json_result.update(a)
                else:
                    a[attribute_name_partitioned[i]] = json.loads(attribute_value)

        pprint.pprint(" =============== Sending ===============")
        pprint.pprint('the sent attribute : ' + attribute)
        print('the sent json : ' + str(json_result))
        return json_result

if __name__ == '__main__':
    a = http_json()
    result = a.attribute_from_http_to_json(attribute='occi.compute.hostname="foobar"', json_result={})
    result = a.attribute_from_http_to_json(attribute='occi.compute.cores=2', json_result=result)
    result = a.attribute_from_http_to_json(attribute='occi.ocni.id="ocniID"', json_result=result)
    print '____________________________ Result (python object) _______________________________________'
    print result
    print '____________________________ Result (JSON format) _______________________________________'
    jj = json.dumps(result)
    print jj
