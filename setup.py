#!/usr/bin/python
# Copyright 2015, The Lvn Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Setup module for lvn."""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
  name='lvn',
  version='0.1',
  description='Additional local convenience for SVN.',
  long_description=('Additional local convenience for SVN.\n'
                    ' - Local branches.'),
  url='https://github.com/halyavin/lvn',
  author='Dmitry Azhichakov <dazhichakov@gmail.com>, Andrey Khalyavin <halyavin@gmail.ru>',
  license='BSD-3',
  classifiers=[
    'Programming Language :: Python :: 2.7',
    'License :: OSI Approved :: BSD License',
    'Topic :: Software Development :: Version Control',
  ],
  keywords='svn subversion development',
  packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
  entry_points={
    'console_scripts': [
      'lvn=lvn.main:main',
    ],
  },
)
