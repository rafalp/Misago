from django.core.management.base import BaseCommand

from misago.conf import settings
from misago.users.avatars.gallery import load_avatar_galleries
from misago.users.models import AvatarGallery


class Command(BaseCommand):
    help = "Overwrites avatar gallery with contents of your gallery directory."

    def handle(self, *args, **options):
        # Empty existing gallery
        for avatar in AvatarGallery.objects.all():
            avatar.image.delete(False)
        AvatarGallery.objects.all().delete()

        if not settings.MISAGO_AVATAR_GALLERY:
            self.stdout.write(
                "No directory to load has been configured. "
                "Avatars gallery has been emptied."
            )
            return

        # Populate it with new items
        if load_avatar_galleries():
            self.stdout.write("New galleries have been loaded.")
        else:
            self.stdout.write(
                "No galleries to load have been found. "
                "Avatars gallery has been emptied."
            )
