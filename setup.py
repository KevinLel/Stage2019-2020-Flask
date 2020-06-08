#!/usr/bin/env python
#coding:latin-1
import os
from setuptools import setup

setup(
    name = 'Homeo',
    version='1.0',
    license='GNU General Public License v3',
    author='Kevin Leleu',
    author_email='kevin.leleu.pro@gmail.com',
    description='Description de mon application flask',
    packages=['my_app'],
    platforms='any',
    install_requires=[
        'flask','requests','peewee','flask-login', 'wtforms', 'flask-wtf', 'flask-mail', 'reportlab', 'pbkdf2'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)