from time import time

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from misago import __version__


@require_http_methods(["POST"])
def dismiss_dev_warning(request: HttpRequest) -> HttpResponse:
    request.session["dismiss_dev_warning"] = {
        "version": __version__,
        "time": int(time()),
    }

    if request.is_htmx:
        return HttpResponse()

    return redirect(reverse("misago:index"))
