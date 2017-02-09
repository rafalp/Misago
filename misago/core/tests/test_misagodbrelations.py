from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO

from misago.core.management.commands import misagodbrelations


class MisagoDBRelationsTests(TestCase):
    def test_command_has_no_errors(self):
        """command raises no errors during execution"""
        command = misagodbrelations.Command()

        call_command(command, stdout=StringIO())
