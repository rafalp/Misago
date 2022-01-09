from ..conf import settings


def make_media_url(path: str) -> str:
    return settings.media_url + path
