from django.http import HttpRequest


def user_permissions(request: HttpRequest) -> dict:
    return {"user_permissions": request.user_permissions}
