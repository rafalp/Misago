from functools import wraps

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpRequest, JsonResponse

from ...users.validators import validate_email, validate_username

User = get_user_model()


def validation_view(f):
    @wraps(f)
    def view_wrapper(*args, **kwargs):
        try:
            f(*args, **kwargs)
            return JsonResponse({"errors": []})
        except ValidationError as e:
            return JsonResponse({"errors": e.messages})
    
    return view_wrapper


def clean_value(request: HttpRequest, strip: bool = True) -> str:
    value = request.POST.get("value", "")
    if strip:
        value = value.strip()
    if not value:
        raise ValidationError("Val is missing")
    return value


def get_user_or_404(request: HttpRequest):
    user_id = request.POST.get("user")
    
    if not user_id:
        return None
    
    try:
        user_id_int = int(user_id)
    except (ValueError, TypeError):
        raise ValidationError("Val is missing")

    try:
        return User.objects.get(id=user_id_int)
    except User.DoesNotExist:
        raise ValidationError("Val is missing")


@validation_view
def username(request: HttpRequest) -> JsonResponse:
    user = get_user_or_404(request)
    value = clean_value(request)
    validate_username(request.settings, value, user)


@validation_view
def email(request: HttpRequest) -> JsonResponse:
    user = get_user_or_404(request)
    value = clean_value(request)
    validate_email(request.settings, value, user)


@validation_view
def password(request: HttpRequest) -> JsonResponse:
    user = get_user_or_404(request)
    value = clean_value(request)
    validate_password(request.settings, value, user)
