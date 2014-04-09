"""
Misago-native rehash of Django's createsuperuser command that
works with double authentication fields on user model
"""
from optparse import make_option
import sys
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS, IntegrityError
from django.utils.encoding import force_str
from django.utils.six.moves import input
from misago.users.validators import (validate_email, validate_username,
                                     validate_password)


class NotRunningInTTYException(Exception):
    pass


class Command(BaseCommand):
    help = 'Used to create a superuser.'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

        self.option_list = BaseCommand.option_list + (
            make_option('--username', dest='username', default=None,
                help='Specifies the username for the superuser.'),
            make_option('--email', dest='email', default=None,
                help='Specifies the username for the superuser.'),
            make_option('--password', dest='password', default=None,
                help='Specifies the username for the superuser.'),
            make_option('--noinput', action='store_false', dest='interactive', default=True,
                help=('Tells Miago to NOT prompt the user for input of any kind. '
                      'You must use --username with --noinput, along with an option for '
                      'any other required field. Superusers created with --noinput will '
                      ' not be able to log in until they\'re given a valid password.')),
            make_option('--database', action='store', dest='database',
                default=DEFAULT_DB_ALIAS, help='Specifies the database to use. Default is "default".'),
        )

    def execute(self, *args, **options):
        self.stdin = options.get('stdin', sys.stdin)  # Used for testing
        return super(Command, self).execute(*args, **options)

    def handle(self, *args, **options):
        username = options.get('username')
        email = options.get('email')
        password = options.get('password')
        interactive = options.get('interactive')

        # Validate initial inputs
        if username is not None:
            try:
                username = username.strip()
                validate_username(username)
            except ValidationError as e:
                self.stderr.write(e.messages[0])
                username = None

        if email is not None:
            try:
                email = email.strip()
                validate_email(email)
            except ValidationError as e:
                self.stderr.write(e.messages[0])
                email = None

        if password is not None:
            try:
                password = password.strip()
                validate_password(password)
            except ValidationError as e:
                self.stderr.write(e.messages[0])
                password = None

        if not interactive:
            if username and email and password:
                # Call User manager's create_superuser using our wrapper
                self.create_superuser(username, email, password)
        else:
            try:
                if hasattr(self.stdin, 'isatty') and not self.stdin.isatty():
                    raise NotRunningInTTYException("Not running in a TTY")

                # Prompt for username/password, and any other required fields.
                # Enclose this whole thing in a try/except to trap for a
                # keyboard interrupt and exit gracefully.
                while not username:
                    try:
                        message = force_str("Enter displayed username: ")
                        raw_value = input(message).strip()
                        validate_username(raw_value)
                        username = raw_value
                    except ValidationError as e:
                        self.stderr.write(e.messages[0])

                while not email:
                    try:
                        raw_value = input("Enter E-mail address: ").strip()
                        validate_email(raw_value)
                        email = raw_value
                    except ValidationError as e:
                        self.stderr.write(e.messages[0])

                while not password:
                    try:
                        raw_value = input("Enter password: ").strip()
                        validate_password(raw_value)
                        repeat_raw_value = input("Repeat password: ").strip()
                        if raw_value != repeat_raw_value:
                            raise ValidationError(
                                "Entered passwords are different.")
                        password = raw_value
                    except ValidationError as e:
                        self.stderr.write(e.messages[0])

                # Call User manager's create_superuser using our wrapper
                self.create_superuser(username, email, password)

            except KeyboardInterrupt:
                self.stderr.write("\nOperation cancelled.")
                sys.exit(1)
            except NotRunningInTTYException:
                self.stdout.write(
                    "Superuser creation skipped due to not running in a TTY. "
                    "You can run `manage.py createsuperuser` in your project "
                    "to create one manually."
                )

    def create_superuser(self, username, email, password):
        try:
            User = get_user_model()
            user = User.objects.create_superuser(username, email, password)

            message = "Superuser #%(pk)s has been created successfully."
            self.stdout.write(message % {'pk': user.pk})
        except ValidationError as e:
            self.stderr.write(e.messages[0])
        except IntegrityError as e:
            self.stderr.write(e.messages[0])
