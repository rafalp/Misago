from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from optparse import make_option
from misago.users.models import UserManager, Group

class Command(BaseCommand):
    args = 'username email password'
    help = 'Creates new user account'
    option_list = BaseCommand.option_list + (
        make_option('--admin',
            action='store_true',
            dest='admin',
            default=False,
            help='Make a new user an administrator'),
        )

    def handle(self, *args, **options):
        if len(args) < 3:
            raise CommandError('adduser requires exactly three arguments: user name, e-mail addres and password')
        
        # Get group
        if options['admin']:
            group = Group.objects.get(pk=1)
        else:
            group = Group.objects.get(pk=3)
           
        # Set user
        try:
            manager = UserManager()
            manager.create_user(args[0], args[1], args[2], group=group)
        except ValidationError as e:
            raise CommandError("New user cannot be created because of following errors:\n\n%s" % '\n'.join(e.messages))
        
        if options['admin']:
            self.stdout.write('Successfully created new administrator "%s"' % args[0])
        else:
            self.stdout.write('Successfully created new user "%s"' % args[0])
        self.stdout.write('\n\nNew user should use "%s" e-mail address and "%s" password to sign in.\n' % (args[1], args[2]))