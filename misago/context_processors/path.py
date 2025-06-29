from django.http import HttpRequest


def full_path(request: HttpRequest) -> dict:
    return {
        "path": request.path,
        "full_path": request.get_full_path(),
    }
