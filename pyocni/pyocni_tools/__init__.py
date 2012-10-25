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
Created on Feb 25, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@license: Apache License, Version 2.0
"""


def create_new_class(classname, parentclasses, gl=globals()):
    """

     This function creates a new class in the provided namespace (gl) with the name classname inheriting
     from all classes in parentclasses, which is a list of strings.

    """

    if len(parentclasses) > 0:
        parent = map(lambda p: p.__name__, parentclasses)
        createclass = 'class %s (%s):\n\tpass' % (classname, ','.join(parent))
    else:
        createclass = 'class %s:\n\tpass' % classname
    exec createclass in gl
    gl[classname] = eval(classname, gl)


def classPath2modulePath(stringIn):
    """

    if it get: specification.ocni.AvailabilityInterval
    it will return: specification.ocni

    """

    tem = stringIn.split('.')
    res = ''
    #l'indice pour la boucle while
    i = 0
    while i < len(tem) - 1:
        res += tem[i]
        if i < len(tem) - 2:
            res += '.'
        i += 1
    return res

if __name__ == '__main__':
    # ============================== Test of create_new_class function (start) ====================
    class clazz1:
        def __init__(self, a):
            self.a = a

        def foo(self):
            return "clazz1: " + str(self.a)

    class clazz2:
        def __init__(self, b, a):
            self.b = b
            self.a = a

        def bar(self):
            return "clazz2: " + str(self.b) + str(self.a)

    # to create a new class names 'Test' that inherit from 'Foobar' and 'Barfoo'
    create_new_class("Test", [clazz1, clazz2], globals())
    print Test.__bases__
    t = Test("23")
    # this will print "foo23"
    print t.foo()
    # To instantiate an object from a class who's name is stored as string
    t2 = globals()['Test']('23')
    print t2.foo()
    #print t.bar() # this will throw an exception, because self.b is not defined
    # ============================== Test of create_new_class function (end) =====================

    pass
