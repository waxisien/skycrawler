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
    scripts=['scripts/searchengine.py'],
    install_requires=[
        'beautifulsoup4==4.8.1',
        'click==7.0',
        'Flask==1.1.1',
        'Flask-Admin==1.5.4',
        'Flask-Cors==3.0.9',
        'Flask-GraphQL==2.0.0',
        'Flask-SQLAlchemy==2.4.1',
        'graphene==2.1.8',
        'graphene-sqlalchemy==2.2.2',
        'graphql-core==2.2.1',
        'geopy==2.0.0',
        'itsdangerous==1.1.0',
        'Jinja2==2.10.3',
        'MarkupSafe==1.1.1',
        'progress==1.5',
        'SQLAlchemy==1.3.11',
        'urllib3==1.25.10',
        'Werkzeug==0.16',
        'WTForms==2.2.1',
    ],
)
