import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='pyocni',
      author='Houssem Medhioub',
      author_email='houssem.medhioub@it-sudparis.eu',
      version='0.1',
      description='PyOCNI: A Python implementation of an extended OCCI with a JSON serialization',
      long_description=read('README'),
      url='http://www.example.com/pyocni',
      platforms=['any'],
      packages=['pyocni'],
      #packages=find_packages(), #['pyocni'],
      install_requires=[
          'config',
          'configobj',
          'logging',
          'ordereddict',
          'jsonpickle',
          'routes',
          'webob',
          'pesto',
          'eventlet',
          'sphinx'
          #'pack>=0.97',
          #'pack'
      ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 2.7'
      ]
)
