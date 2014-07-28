from PIL import Image

from django.core.management.base import BaseCommand

from misago.users.avatars import store
from misago.users.avatars.paths import BLANK_AVATAR


class FakeDate(object):
    def strftime(self, format=''):
        return 'blank'


class FakeUser(object):
    pk = 'blank'
    id = 'blank'
    joined_on = FakeDate()


class Command(BaseCommand):
    help = 'Updates stored blank avatar.'

    def handle(self, *args, **options):
        store.store_new_avatar(FakeUser, Image.open(BLANK_AVATAR))
        self.stdout.write('Blank avatar was updated.')
