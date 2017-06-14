"""setup.py"""
# -*- coding: utf-8 -*-
#/usr/bin/env python

from setuptools import setup, find_packages

VERSION = '0.0.5'
LONG_DESCRIPTION = open('intro.rst', 'r').read()

INSTALL_REQUIRES = [
    'Django',
]

setup(
    name='django-simditor',
    version=VERSION,
    description='Django admin Simditor integration.',
    long_description=LONG_DESCRIPTION,
    author='Silence',
    author_email='istommao@gmail.com',
    url='https://github.com/istommao/django-simditor',
    zip_safe=False,
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
    keywords='Django admin Simditor integration!',
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ]
)
