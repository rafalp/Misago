import os

from path import Path
from PIL import Image

from django.conf import settings
from django.core.management.base import BaseCommand

from misago.users.avatars.paths import AVATARS_STORE, BLANK_AVATAR


class Command(BaseCommand):
    help = 'Updates stored blank avatar.'

    def handle(self, *args, **options):
        avatars_dir = Path(os.path.join(AVATARS_STORE, 'blank'))

        # Empty existing blank avatar
        if avatars_dir.exists():
            avatars_dir.rmtree()
        avatars_dir.mkdir()

        # Generate new images
        image = Image.open(BLANK_AVATAR)
        for size in sorted(settings.MISAGO_AVATARS_SIZES, reverse=True):
            avatar_file = '%s.png' % size
            avatar_file = Path(os.path.join(avatars_dir, avatar_file))

            image = image.resize((size, size), Image.ANTIALIAS)
            image.save(avatar_file, "PNG")

        self.stdout.write('Blank avatar was updated')
