from urllib.parse import urlencode

from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect

from .cursor import EmptyPageError


def redirect_to_last_page(
    request: HttpRequest, empty_page_error: EmptyPageError
) -> HttpResponseRedirect:
    last_page_url = request.path_info

    if request.GET:
        new_querystring = request.GET.dict()
        new_querystring.pop("cursor", None)
        if empty_page_error.last_cursor:
            new_querystring["cursor"] = empty_page_error.last_cursor
        last_page_url += "?" + urlencode(new_querystring)

    return redirect(last_page_url)
