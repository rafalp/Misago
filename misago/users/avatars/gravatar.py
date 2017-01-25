from io import BytesIO

import requests
from PIL import Image

from misago.conf import settings

from . import store


GRAVATAR_URL = 'http://www.gravatar.com/avatar/%s?s=%s&d=404'


class GravatarError(RuntimeError):
    pass


class NoGravatarAvailable(GravatarError):
    pass


def set_avatar(user):
    url_formats = (user.email_hash, max(settings.MISAGO_AVATARS_SIZES))
    try:
        r = requests.get(GRAVATAR_URL % url_formats, timeout=5)
        if r.status_code != 200:
            raise NoGravatarAvailable("gravatar is not available for this e-mail")

        image = Image.open(BytesIO(r.content))
        store.store_new_avatar(user, image)
    except requests.exceptions.RequestException:
        raise GravatarError("failed to connect to gravatar servers")
