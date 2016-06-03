from django.test import TestCase
from django.utils.six import StringIO

from misago.core.management.commands import misagorequirements


class MisagoRequirementsTests(TestCase):
    def test_list_misago_requirements(self):
        """command returns requirements.txt contents"""
        command = misagorequirements.Command()

        out = StringIO()
        command.execute(stdout=out)
        command_output = out.getvalue()

        self.assertIn("django", command_output)
