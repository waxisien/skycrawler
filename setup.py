#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import skycrawler

setup(
    name='skycrawler',
    version=skycrawler.__version__,
    packages=find_packages(),
    long_description=open('README.md').read(),
    url='http://github.com/waxisien/skycrawler',
)
