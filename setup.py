#-*- coding: utf-8 -*-
import os
from setuptools import setup
from misago import __version__ as version

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

with open(os.path.join(os.path.dirname(__file__), 'misago/project_template/requirements.txt'), "r") as f:
    REQUIREMENTS = [x.strip() for x in f.readlines()]


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='misago',
    version=version,
    packages=['misago'],
    include_package_data=True,
    license='GNU General Public License v2 (GPLv2)',
    description='Misago is be complete, featured and modern forum solution.',
    long_description=README,
    url='http://www.misago-project.org/',
    author=u'Rafał Pitoń',
    author_email='kontakt@rpiton.com',
    install_requires=REQUIREMENTS,
    scripts=['misago/bin/misago-start.py'],
    entry_points={'console_scripts': [
        'misago-start = misago.core.setup:start_misago_project',
    ]},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
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
