from django.http import HttpRequest


def full_path(request: HttpRequest) -> dict:
    return {
        "path": request.path_info,
        "full_path": request.get_full_path_info(),
    }
