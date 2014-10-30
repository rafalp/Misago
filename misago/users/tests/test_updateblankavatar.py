from django.test import TestCase
from django.utils.six import StringIO

from misago.users.management.commands import updateblankavatar


class UpdateBlankAvatarTests(TestCase):
    def test_regen_blank_avatar(self):
        """command regens blank avatar"""
        command = updateblankavatar.Command()

        out = StringIO()
        command.execute(stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, 'Blank avatar was updated')
