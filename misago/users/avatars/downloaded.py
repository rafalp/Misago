from io import BytesIO

import requests
from PIL import Image

from . import store


class AvatarDownloadError(RuntimeError):
    pass


def set_avatar(user, avatar_url):
    try:
        r = requests.get(avatar_url, timeout=5)
        if r.status_code != 200:
            raise AvatarDownloadError("could not retrieve avatar from the server")

        image = Image.open(BytesIO(r.content))

        # Crop avatar into square
        width, height = image.size

        if width > height:
            left = int((width - height) / 2)
            image = image.crop((left, 0, width + left, height))
        elif height > width:
            top = int((height - width) / 2)
            image = image.crop((0, top, width, top + height))

        store.store_new_avatar(user, image)
    except requests.exceptions.RequestException:
        raise AvatarDownloadError("failed to connect to avatar server")
