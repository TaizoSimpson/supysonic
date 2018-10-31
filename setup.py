#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# This file is part of Supysonic.
# Supysonic is a Python implementation of the Subsonic server API.
#
# Copyright (C) 2013-2018 Alban 'spl0k' Féron
#                    2017 Óscar García Amor
#
# Distributed under terms of the GNU AGPLv3 license.

import supysonic as project

from setuptools import setup
from setuptools import find_packages


reqs = [
    'flask>=0.11',
    'pony>=0.7.6',
    'Pillow',
    'requests>=1.0.0',
    'mutagen>=1.33'
]
extras = {
    'watcher': [ 'watchdog>=0.8.0' ]
}

setup(
        name=project.NAME,
        version=project.VERSION,
        description=project.DESCRIPTION,
        keywords=project.KEYWORDS,
        long_description=project.LONG_DESCRIPTION,
        author=project.AUTHOR_NAME,
        author_email=project.AUTHOR_EMAIL,
        url=project.URL,
        license=project.LICENSE,
        packages=find_packages(exclude=['tests*']),
        install_requires = reqs,
        extras_require = extras,
        scripts=['bin/supysonic-cli', 'bin/supysonic-watcher'],
        zip_safe=False,
        include_package_data=True,
        test_suite='tests.suite',
        tests_require = [ 'lxml', 'responses' ] + [ r for er in extras.values() for r in er ],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Environment :: Web Environment',
            'Framework :: Flask',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: GNU Affero General Public License v3',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Topic :: Multimedia :: Sound/Audio'
        ]
     )

