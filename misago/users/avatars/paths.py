import os

from misago.conf import settings


AVATARS_STORE = settings.MISAGO_AVATAR_STORE
MEDIA_AVATARS = os.path.join(settings.MEDIA_ROOT, 'avatars')
BLANK_AVATAR = os.path.join(MEDIA_AVATARS, 'blank.png')
