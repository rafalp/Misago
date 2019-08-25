import jwt
from django.http import Http404, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .user import get_or_create_user
from .validators import UserDataValidator


@csrf_exempt
@require_POST
def sso_sync(request):
    if not request.settings.enable_sso:
        raise Http404()

    access_token = request.POST.get("access_token")
    if not access_token:
        return HttpResponseBadRequest("Request did not contain the access token")

    try:
        user_data = jwt.decode(
            access_token, request.settings.sso_private_key, algorithms=["HS256"]
        )
    except jwt.PyJWTError:
        return HttpResponseBadRequest("Access token is invalid")

    validator = UserDataValidator(user_data)
    if not validator.is_valid():
        failed_fields = ", ".join(validator.errors.keys())
        return HttpResponseBadRequest(f"User data failed to validate: {failed_fields}")

    user = get_or_create_user(request, validator.cleaned_data)

    return JsonResponse({"id": user.id})
