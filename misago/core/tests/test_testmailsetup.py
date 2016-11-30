from django.core import mail
from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO


from ..management.commands import testemailsetup


class TestEmailSetupTests(TestCase):
    def test_email_setup(self):
        """command sets test email in outbox"""
        command = testemailsetup.Command()

        out = StringIO()
        call_command(command, "t@mail.com", stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, 'Test message was sent to t@mail.com')
        self.assertEqual('Test Message', mail.outbox[0].subject)

    def test_invalid_args(self):
        """
        there are no unhandled exceptions when command receives invalid args
        """
        command = testemailsetup.Command()

        out = StringIO()
        err = StringIO()

        call_command(command, "bawww", stdout=out, stderr=err)
        command_output = err.getvalue().splitlines()[-1].strip()
        self.assertEqual(command_output, "This isn't valid e-mail address")
