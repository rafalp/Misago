from django.test import TestCase
from django.utils.six import StringIO

from misago.core.management.commands import remakemisagochecksums


class RemakeMisagoChecksumsTests(TestCase):
    def test_remake_checksums(self):
        """command raises no errors"""
        command = remakemisagochecksums.Command()

        out = StringIO()
        command.execute("--force", stdout=out)
        command_output = out.getvalue().splitlines()[-1].strip()
        self.assertEqual(command_output, "Done!")
