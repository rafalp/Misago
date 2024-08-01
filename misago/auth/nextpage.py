from django.http import HttpRequest
from django.utils.http import url_has_allowed_host_and_scheme
from django.shortcuts import redirect

NEXT_PAGE = "next"


def get_next_page_url(request: HttpRequest) -> str | None:
    redirect_to = request.POST.get(
        NEXT_PAGE, request.GET.get(NEXT_PAGE)
    )
    
    return clean_next_page_url(request, redirect_to)


def clean_next_page_url(request: HttpRequest, redirect_to: str) -> str | None:
    url_is_safe = url_has_allowed_host_and_scheme(
        url=redirect_to,
        allowed_hosts=request.get_host(),
        require_https=request.is_secure(),
    )

    return redirect_to if url_is_safe else None