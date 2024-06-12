from django.http import HttpRequest


def is_request_htmx(request: HttpRequest) -> dict:
    return {"is_request_htmx": request.is_htmx}
