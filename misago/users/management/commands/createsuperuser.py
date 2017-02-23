"""
Misago-native rehash of Django's createsuperuser command that
works with double authentication fields on user model
"""
import sys
from getpass import getpass

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.db import DEFAULT_DB_ALIAS, IntegrityError
from django.utils.encoding import force_str
from django.utils.six.moves import input

from misago.users.validators import validate_email, validate_username


UserModel = get_user_model()


class NotRunningInTTYException(Exception):
    pass


class Command(BaseCommand):
    help = 'Used to create a superuser.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            dest='username',
            default=None,
            help="Specifies the username for the superuser.",
        )
        parser.add_argument(
            '--email',
            dest='email',
            default=None,
            help="Specifies the username for the superuser.",
        )
        parser.add_argument(
            '--password',
            dest='password',
            default=None,
            help="Specifies the username for the superuser.",
        )
        parser.add_argument(
            '--noinput',
            action='store_false',
            dest='interactive',
            default=True,
            help=(
                "Tells Misago to NOT prompt the user for input "
                "of any kind. You must use --username with "
                "--noinput, along with an option for any other "
                "required field. Superusers created with "
                "--noinput will  not be able to log in until "
                "they're given a valid password."
            ),
        )
        parser.add_argument(
            '--database',
            action='store',
            dest='database',
            default=DEFAULT_DB_ALIAS,
            help=('Specifies the database to use. Default is "default".'),
        )

    def execute(self, *args, **options):
        self.stdin = options.get('stdin', sys.stdin)  # Used for testing
        return super(Command, self).execute(*args, **options)

    def handle(self, *args, **options):
        username = options.get('username')
        email = options.get('email')
        password = options.get('password')
        interactive = options.get('interactive')
        verbosity = int(options.get('verbosity', 1))

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
                self.create_superuser(username, email, password, verbosity)
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
                        raw_value = getpass("Enter password: ").strip()
                        validate_password(
                            raw_value, user=UserModel(username=username, email=email)
                        )

                        repeat_raw_value = getpass("Repeat password: ").strip()
                        if raw_value != repeat_raw_value:
                            raise ValidationError("Entered passwords are different.")
                        password = raw_value
                    except ValidationError as e:
                        self.stderr.write(e.messages[0])

                # Call User manager's create_superuser using our wrapper
                self.create_superuser(username, email, password, verbosity)

            except KeyboardInterrupt:
                self.stderr.write("\nOperation cancelled.")
                sys.exit(1)
            except NotRunningInTTYException:
                self.stdout.write(
                    "Superuser creation skipped due to not running in a TTY. "
                    "You can run `manage.py createsuperuser` in your project "
                    "to create one manually."
                )

    def create_superuser(self, username, email, password, verbosity):
        try:
            user = UserModel.objects.create_superuser(
                username, email, password, set_default_avatar=True
            )

            if verbosity >= 1:
                message = "Superuser #%(pk)s has been created successfully."
                self.stdout.write(message % {'pk': user.pk})
        except ValidationError as e:
            self.stderr.write(e.messages[0])
        except IntegrityError as e:
            self.stderr.write(e.messages[0])
