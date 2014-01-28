import os
import sys
from optparse import OptionParser
from django.core import management


def get_misago_project_template():
    misago_path = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(misago_path, 'project_template')


def start_misago_project():
    parser = OptionParser(usage="usage: %prog project_name")
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("project_name must be specified")
    project_name = args[0]
    if project_name.startswith("-"):
        parser.error("project_name cannot start with '-'")


    # Ensure the given directory name doesn't clash with an existing
    # Python package/module.
    try:
        __import__(project_name)
    except ImportError:
        pass
    else:
        parser.error("'%s' conflicts with the name of an existing "
                     "Python module and cannot be used as a project "
                     "name. Please try another name." % project_name)

    argv = ['start-misago.py', 'startproject', project_name,
            '--template=%s' % get_misago_project_template()]

    management.execute_from_command_line(argv)
