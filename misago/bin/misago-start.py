#!/usr/bin/env python
import os
import sys
from optparse import OptionParser
from django.core import management


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


    MISAGO_PROJECT_TEMPLATE = os.path.join(os.path.dirname(__file__),
                                           'misago/project_template')
    argv = [sys.args[0], 'startproject', project_name,
            '--template=%s' % MISAGO_PROJECT_TEMPLATE]
    management.execute_from_command_line(argv)


if __name__ == "__main__":
    start_misago_project()
