from StringIO import StringIO

from PIL import Image
import requests

from misago.conf import settings

from misago.users.avatars import cache


GRAVATAR_URL = 'http://www.gravatar.com/avatar/%s?s=%s'


def set_avatar(user):
    url_formats = (user.email_hash, max(settings.MISAGO_AVATARS_SIZES))
    r = requests.get(GRAVATAR_URL % url_formats)
    image = Image.open(StringIO(r.content))
    cache.store_new_avatar(user, image)
