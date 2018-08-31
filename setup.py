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
        'beautifulsoup4==4.6.3',
        'click==6.6',
        'Flask==1.0.2',
        'Flask-Admin==1.5.2',
        'Flask-SQLAlchemy==2.3',
        'Flask-GraphQL==1.4.1',
        'graphene==2.0.1',
        'graphene-sqlalchemy==2.0.0',
        'graphql-core==2.0',
        'geopy==1.14.0',
        'itsdangerous==0.24',
        'Jinja2==2.10',
        'MarkupSafe==1.0',
        'progress==1.3',
        'SQLAlchemy==1.2.11',
        'Werkzeug==0.13',
        'WTForms==2.2.1'
    ],
)
