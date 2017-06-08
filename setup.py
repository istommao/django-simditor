"""setup.py"""
# -*- coding: utf-8 -*-
#/usr/bin/env python

from setuptools import setup, find_packages

VERSION = '0.0.2'
LONG_DESCRIPTION = open('intro.rst', 'r').read()

setup(
    name='django-simditor',
    verson=VERSION,
    description='Django admin Simditor integration.',
    long_description=LONG_DESCRIPTION,
    author='silence',
    author_email='istommao@gmail.com',
    url='https://github.com/istommao/django-simditor',
    zip_safe=False,
    install_requires=[
        'Django',
    ],
    packages=find_packages(exclude=["*.demo"]),
    include_package_data=True,
    keywords='Django admin Simditor integration!'
)
