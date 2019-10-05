#!/usr/bin/env python
# This file is part of SOCAD
# Copyright (C) 2018  Miguel Fernandes
#
# SOCAD is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SOCAD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
"""Python setup."""

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='SOCAD',
    version='0.1.0',
    description='Connect Cadence Virtuoso to a Python client using TCP sockets.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Miguel Fernandes',
    author_email='me@mdmfernandes.com',
    url='https://github.com/mdmfernandes/socad',
    packages=find_packages(exclude=['example']),
    keywords=[
        'socket communications', 'cadence virtuoso'
    ],
    platforms=['any'],
    license='GPLv3',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)'
    ],
    python_requires='>=3.6',
    #install_requires=[]
)
