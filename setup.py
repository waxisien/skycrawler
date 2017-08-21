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
    install_requires=[
        'beautifulsoup4==4.6.0',
        'click==6.6',
        'Flask==0.11.1',
        'Flask-Admin==1.5.0',
        'Flask-SQLAlchemy==2.2',
        'Flask-GraphQL==1.4.1',
        'graphene-sqlalchemy==1.1.1',
        'geopy==1.11.0',
        'itsdangerous==0.24',
        'Jinja2==2.8',
        'MarkupSafe==0.23',
        'progress==1.3',
        'SQLAlchemy==1.1.9',
        'Werkzeug==0.11.11',
        'WTForms==2.1'
    ],
)
