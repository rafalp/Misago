import os
import re
from optparse import OptionParser

from django.core import management


def validate_project_name(parser, project_name):
    if project_name[0].isdigit():
        parser.error("project_name cannot start with digit")

    if project_name.startswith("-"):
        parser.error("project_name cannot start with '-'")

    if re.search("[^0-9a-zA-Z]", project_name):
        parser.error("project_name cannot contain special characters")

    # Ensure the given directory name doesn't clash with an existing
    # Python package/module.
    try:
        __import__(project_name)
    except ImportError:
        pass
    else:
        parser.error((
            "'%s' conflicts with the name of an existing "
            "Python module and cannot be used as a project "
            "name. Please try another name."
        ) % project_name)

    return project_name


def get_misago_project_template():
    misago_path = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(misago_path, 'project_template')


def start_misago_project():
    parser = OptionParser(usage="usage: %prog project_name")
    _, args = parser.parse_args()

    if len(args) != 1:
        parser.error("project_name must be specified")

    project_name = validate_project_name(parser, args[0])

    argv = [
        'start-misago.py', 'startproject', project_name,
        '--template=%s' % get_misago_project_template()
    ]

    management.execute_from_command_line(argv)
