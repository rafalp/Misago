#-*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages

from misago import __version__ as version


SETUP_DIR = os.path.dirname(__file__)


with open(os.path.join(SETUP_DIR, 'requirements.txt'), "r") as f:
    REQUIREMENTS = [x.strip() for x in f.readlines()]


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


EXCLUDE_FROM_PACKAGES = [
    'misago.project_template',
    'misago.bin'
]


setup(
    name='Misago',
    version=version,
    license='GNU General Public License v2 (GPLv2)',
    description=(
        "Misago is modern, fully featured forum application written in "
        "Python and ES6, powered by Django and React.js. It works out of "
        "the box and plays nicely with other projects like Django-CMS."
    ),
    url='http://www.misago-project.org/',
    author=u'Rafał Pitoń',
    author_email='kontakt@rpiton.com',
    install_requires=REQUIREMENTS,
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    scripts=[
        'misago/bin/misago-start.py',
    ],
    entry_points={'console_scripts': [
        'misago-start = misago.core.setup:start_misago_project',
    ]},
    test_suite="runtests.runtests",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
