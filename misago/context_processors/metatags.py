from django.http import HttpRequest

from ..metatags.default import get_default_metatags


def default_metatags(request: HttpRequest) -> dict:
    return {"default_metatags": get_default_metatags(request)}
