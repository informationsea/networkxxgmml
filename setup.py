#!/usr/bin/env python

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup

setup(
    name='networkxgmml',
    version='0.1.1',
    description='XGMML parser for networkx',
    author='Yasunobu OKAMURA',
    author_email='okamura@informationsea.info',
    url='https://github.com/informationsea/xgmml-networkx',
    py_modules=['networkxgmml'],
    install_requires=['setuptools', 'networkx']
)
