#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Synopsis:          This script is the primary configuration file for the pydplus project
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     09 Jun 2025
"""

import setuptools
import codecs
import os.path


def read(rel_path):
    """This function reads the ``version.py`` script in order to retrieve the version."""
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    """This function retrieves the current version of the package without needing to import the
       :py:mod:`pydplus.utils.version` module in order to avoid dependency issues."""
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delimiter = '"' if '"' in line else "'"
            return line.split(delimiter)[1]
    raise RuntimeError('Unable to find the version string')


with open('README.md', 'r') as fh:
    long_description = fh.read()

version = get_version('src/pydplus/utils/version.py')

setuptools.setup(
    name='pydplus',
    version=version,
    author='Jeff Shurtliff',
    author_email='jeff.shurtliff@rsa.com',
    description='A Python toolset for the RSA ID Plus cloud authentication platform',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jeffshurtliff/pydplus',
    project_urls={
        'Issue Tracker': 'https://github.com/jeffshurtliff/pydplus/issues',
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Communications :: FIDO',
        'Topic :: Office/Business',
        'Topic :: Security',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Systems Administration :: Authentication/Directory',
    ],
    python_requires='>=3.9.23',
    install_requires=[
        'urllib3>=2.4.0',
        'requests>=2.32.3',
        'setuptools>=65.5.1',
        'pytest>=8.3.5',
        'PyYAML>=6.0.2',
        'PyJWT>=2.10.1',
        'cryptography>=45.0.3',
    ],
    extras_require={
        'sphinx': [
            'Sphinx>=7.4.7',
            'sphinxcontrib-applehelp>=2.0.0',
            'sphinxcontrib-devhelp>=2.0.0',
            'sphinxcontrib-htmlhelp>=2.1.0',
            'sphinxcontrib-jsmath>=1.0.1',
            'sphinxcontrib-qthelp>=2.0.0',
            'sphinxcontrib-serializinghtml>=2.0.0',
        ],
    }
)
