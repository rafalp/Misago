import os

from path import path

from misago.conf import settings


AVATARS_CACHE = settings.MISAGO_AVATAR_CACHE
MEDIA_AVATARS = os.path.join(settings.MEDIA_ROOT, 'avatars')
BLANK_AVATAR = os.path.join(MEDIA_AVATARS, 'blank.png')
