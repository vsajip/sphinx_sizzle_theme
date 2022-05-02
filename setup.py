# -*- coding: utf-8 -*-
#
# Copyright 2019 by Vinay Sajip. All Rights Reserved.
#

from io import open
from setuptools import setup
from sphinx_sizzle_theme import __version__

setup(
    name='sphinx_sizzle_theme',
    version=__version__,
    url='https://bitbucket.org/vinay.sajip/sphinx_sizzle_theme/',
    license='MIT',
    author='Vinay Sajip',
    author_email='vinay_sajip@yahoo.co.uk',
    description='Sizzle theme for Sphinx',
    long_description=open('README.rst', encoding='utf-8').read(),
    zip_safe=False,
    packages=['sphinx_sizzle_theme'],
    package_data={'sphinx_sizzle_theme': [
        'theme.conf',
        '*.html',
        'version.txt',
        'static/css/*.css',
        'static/js/*.js',
        'static/fonts/*.*'
    ]},
    entry_points = {
        'sphinx.html_themes': [
            'sizzle = sphinx_sizzle_theme',
        ]
    },
    install_requires=[
       'sphinx'
    ],
    classifiers=[
        'Framework :: Sphinx',
        'Framework :: Sphinx :: Theme',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
        'Topic :: Documentation',
        'Topic :: Software Development :: Documentation',
    ],
)
