#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
from setuptools import find_packages, setup


here = os.path.abspath(os.path.dirname(__file__))
description = 'Generate AWS CloudFront\'s Signed URLs'

try:
    readme = open(os.path.join(here, 'README.rst')).read()
    changes = open(os.path.join(here, 'CHANGES.txt')).read()
    long_description = '\n\n'.join([readme, changes])
except IOError:
    long_description = description

requires = [
    'rsa',
]

tests_require = [
    'mock',
]

setup(
    name='cloudfrontsigner',
    version='0.1.dev1',
    description=description,
    long_description=long_description,
    author='OCHIAI, Gouji',
    author_email='gjo.ext@gmail.com',
    url='https://github.com/gjo/botocore_paste',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=tests_require,
    test_suite='cloudfrontsigner.tests',
    extras_require={
        'testing': tests_require,
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
)
