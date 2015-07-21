#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from setuptools import setup, find_packages
from setuptools.command.sdist import sdist as _sdist
from misago import __version__ as version

here = os.path.dirname(__file__)

with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

with open(os.path.join(here, 'requirements.txt')) as f:
    REQUIREMENTS = [x.strip() for x in f.readlines()]


def copy_data_files(paths):
    for path in paths:
        dest = os.path.join('misago', path)
        if os.path.exists(dest):
            shutil.rmtree(dest)
        shutil.copytree(path, dest)


class sdist(_sdist):

    def run(self):
        copy_data_files(['attachments', 'media', 'static', 'templates'])
        _sdist.run(self)


setup(
    name='Misago',
    version=version,
    license='GNU General Public License v2 (GPLv2)',
    description='Misago is complete, featured and modern forum solution.',
    long_description=README,
    url='http://www.misago-project.org/',
    author=u'Rafał Pitoń',
    author_email='kontakt@rpiton.com',
    install_requires=REQUIREMENTS,
    extras_require={
        'postgresql': ['psycopg2'],
    },
    cmdclass={'sdist': sdist},
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
