from datetime import date

from PIL import Image

from django.core.management.base import BaseCommand

from misago.users.avatars import cache
from misago.users.avatars.paths import BLANK_AVATAR


class FakeUser(object):
    pk = 'blank'
    id = 'blank'
    joined_on = date(2014, 1, 1)


class Command(BaseCommand):
    help = 'Overwrites cached blank avatar with new one.'

    def handle(self, *args, **options):
        cache.store_new_avatar(FakeUser, Image.open(BLANK_AVATAR))
        self.stdout.write('Blank avatar cache was refreshed.')
