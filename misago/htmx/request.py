from django.http import HttpRequest


def is_request_htmx(request: HttpRequest) -> bool:
    return request.headers.get("hx-request") == "true"
