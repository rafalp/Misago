from io import StringIO

from django.core.management import call_command

from ..management.commands import createfakehistory


def test_management_command_has_no_errors(db):
    call_command(createfakehistory.Command(), stdout=StringIO())
