#!/usr/bin/env python

from setuptools import setup

setup(
    name='networkxxgmml',
    version='0.1',
    description='XGMML parser for networkx',
    author='Yasunobu OKAMURA',
    author_email='okamura@informationsea.info',
    url='https://github.com/informationsea/xgmml-networkx',
    pb_modules=['networkxxgmml'],
    install_requires=['distribute', 'networkx']
)
