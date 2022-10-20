#!/usr/bin/env python  
from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="xyz-dailylog",
    version="0.1.7",
    author="szuprefix",
    author_email="szuprefix@126.com",
    description="dailylog",
    long_description=open("README.rst").read(),
    license="MIT",
    url="https://github.com/szuprefix/py-xyz-dailylog",
    packages=find_packages(exclude=['tests.*', 'tests', 'testproject', 'example.*', 'example']),
    include_package_data=True,
    install_requires=[
        'django>=1.11.2',
        'xyz-restful>=0.0.6',
        'xyz-util>=0.0.7',
        'pymongo'
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
