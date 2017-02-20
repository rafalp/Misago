from django.conf import settings
from django.core import mail
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.core.validators import validate_email


class Command(BaseCommand):
    help = 'Sends test e-mail to given address'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str)

    def handle(self, *args, **options):
        try:
            email = options['email']
            validate_email(email)
            self.send_message(email)
        except ValidationError:
            self.stderr.write("This isn't valid e-mail address")

    def send_message(self, email):
        mail.send_mail(
            'Test Message',
            ("This message was sent to test if your "
             "site e-mail is configured correctly."),
            settings.DEFAULT_FROM_EMAIL, [email],
            fail_silently=False
        )
        self.stdout.write("Test message was sent to %s" % email)
