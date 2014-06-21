#-*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages
from misago import __version__ as version

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

requirements_path = os.path.join(os.path.dirname(__file__),
                                 'misago/project_template/requirements.txt')
with open(requirements_path, "r") as f:
    REQUIREMENTS = [x.strip() for x in f.readlines()]

REQUIREMENTS = REQUIREMENTS[1:]


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


EXCLUDE_FROM_PACKAGES = ['misago.project_template',
                         'misago.bin']


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
    dependency_links=[
        'https://github.com/django/django/archive/stable/1.7.x.zip',
    ],
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    scripts=['misago/bin/misago-start.py'],
    entry_points={'console_scripts': [
        'misago-start = misago.core.setup:start_misago_project',
    ]},
    test_suite="runtests.runtests",
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
