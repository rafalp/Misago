from django.http import HttpRequest
from django.shortcuts import redirect


def redirect_subscribed_to_watched(request: HttpRequest, **kwargs):
    return redirect(
        request.path.replace("/subscribed/", "/watched/"),
        permanent=True,
    )
