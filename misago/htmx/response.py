from django.http import HttpResponse


def htmx_redirect(redirect_url: str) -> HttpResponse:
    """Return client-side HTMX redirect.

    Because browsers intercept 30X responses, redirect response made to
    HTMX request will be intercepted and executed by the browser itself.
    But in some cases we want to tell HTMX to do "classic" redirect to
    new URL in response to user's action.
    """

    response = HttpResponse(status=204)
    response.headers["hx-redirect"] = redirect_url
    return response
