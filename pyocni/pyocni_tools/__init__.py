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
Created on Feb 25, 2011

@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@version: 0.3
@license: LGPL - Lesser General Public License
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
