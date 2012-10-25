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
Created on Jul 13, 2011

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@license: Apache License, Version 2.0
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
                    try:
                        a[attribute_name_partitioned[i]] = json.loads(attribute_value)
                    except Exception :
                        a[attribute_name_partitioned[i]] = attribute_value
            else:
                if i < (len(attribute_name_partitioned) - 1):
                    a[attribute_name_partitioned[i]] = {}
                    a = a[attribute_name_partitioned[i]]
                    json_result.update(a)
                else:
                    try:
                        a[attribute_name_partitioned[i]] = json.loads(attribute_value)
                    except Exception :
                        a[attribute_name_partitioned[i]] = attribute_value

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
