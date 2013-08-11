from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from misago import __version__

class Command(BaseCommand):
    """
    Displays version number and license
    """
    help = 'Displays Misago Credits'
    def handle(self, *args, **options):
        self.stdout.write('\n')
        self.stdout.write('                                    _\n')
        self.stdout.write('                         ____ ___  (_)________  ____  ____ \n')
        self.stdout.write('                        / __ `__ \/ / ___/ __ `/ __ `/ __ \ \n')
        self.stdout.write('                       / / / / / / (__  ) /_/ / /_/ / /_/ / \n')
        self.stdout.write('                      /_/ /_/ /_/_/____/\__,_/\__, /\____/ \n')
        self.stdout.write('                                             /____/\n')
        self.stdout.write('\n')
        self.stdout.write('                    Your community is powered by Misago v.%s' % __version__)
        self.stdout.write('\n              For help and feedback visit http://misago-project.org')
        self.stdout.write('\n\n')
        self.stdout.write('================================================================================')
        self.stdout.write('\n\n')
        self.stdout.write('Copyright (C) %s, Rafal Piton' % timezone.now().year)
        self.stdout.write('\n')
        self.stdout.write('\nThis program is free software; you can redistribute it and/or modify it under')
        self.stdout.write('\nthe terms of the GNU General Public License version 3 as published by')
        self.stdout.write('\nthe Free Software Foundation')
        self.stdout.write('\n')
        self.stdout.write('\nThis program is distributed in the hope that it will be useful, but')
        self.stdout.write('\nWITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY')
        self.stdout.write('\nor FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License')
        self.stdout.write('\nfor more details.')
        self.stdout.write('\n')
        self.stdout.write('\nYou should have received a copy of the GNU General Public License along')
        self.stdout.write('\nalong with this program.  If not, see <http://www.gnu.org/licenses/>.')
        self.stdout.write('\n\n')
