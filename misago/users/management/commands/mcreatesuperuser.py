from optparse import make_option
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS
from django.utils.encoding import force_str
from django.utils.six.moves import input


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

    def handle(self, *args, **options):
        User = get_user_model()
        username = options.get('username')
        email = options.get('email')
        password = options.get('password')
        interactive = options.get('interactive')

        if not interactive:
            pass
        else:
            try:
                if hasattr(self.stdin, 'isatty') and not self.stdin.isatty():
                    raise NotRunningInTTYException("Not running in a TTY")
                while username is None:
                    break
                while email is None:
                    break
                while password is None:
                    break
            except KeyboardInterrupt:
                self.stderr.write("\nOperation cancelled.")
                sys.exit(1)
            except NotRunningInTTYException:
                self.stdout.write(
                    "Superuser creation skipped due to not running in a TTY. "
                    "You can run `manage.py createsuperuser` in your project "
                    "to create one manually."
                )
