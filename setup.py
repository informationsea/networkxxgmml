#!/usr/bin/env python

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup

setup(
    name='networkxgmml',
    version='0.1.4',
    description='XGMML parser for networkx',
    author='Yasunobu OKAMURA',
    author_email='okamura@informationsea.info',
    url='https://github.com/informationsea/networkxxgmml',
    py_modules=['networkxgmml'],
    install_requires=['setuptools', 'networkx']
)
