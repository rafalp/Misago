from django.test import TestCase
from django.utils.six import StringIO

from ..management.commands import misagodbrelations


class MisagoDBRelationsTests(TestCase):
    def test_command_has_no_errors(self):
        """command raises no errors during execution"""
        command = misagodbrelations.Command()

        command.execute(stdout=StringIO())
