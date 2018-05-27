#!/usr/bin/python3

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

setup(
    name='aauth-dokuwiki',
    version='0.0.1',
    description='SSO and group provider for dokuwiki',
    url='https://github.com/kormat/aauth-dokuwiki',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=3',
    include_package_data=True,
)
