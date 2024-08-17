from functools import wraps

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import BadRequest, ValidationError
from django.http import HttpRequest, JsonResponse
from django.utils.translation import pgettext
from django.views.decorators.debug import sensitive_post_parameters

from ...users.validators import validate_email, validate_username

User = get_user_model()


def validation_view(f):
    @wraps(f)
    def view_wrapper(request: HttpRequest, *args, **kwargs):
        try:
            if request.method != "POST":
                raise BadRequest()

            f(request, *args, **kwargs)
            return JsonResponse({"errors": []})
        except ValidationError as e:
            return JsonResponse({"errors": e.messages}, status=400)

    return view_wrapper


def clean_value(request: HttpRequest, strip: bool = True) -> str:
    value = request.POST.get("value", "")
    if strip:
        value = value.strip()
    if not value.strip():
        raise ValidationError(
            pgettext("account validation api", "'value' can't be empty."),
        )
    return value


def get_user_from_data(request: HttpRequest):
    user_id = request.POST.get("user")

    if not user_id:
        return None

    try:
        user_id_int = int(user_id)
        if user_id_int < 1:
            raise ValueError()
    except (ValueError, TypeError):
        raise ValidationError(
            pgettext("account validation api", "'user' must be a positive integer."),
        )

    try:
        return User.objects.get(id=user_id_int)
    except User.DoesNotExist:
        raise ValidationError(
            pgettext(
                "account validation api", "'user' doesn't match any user account."
            ),
        )


@validation_view
def username(request: HttpRequest) -> JsonResponse:
    user = get_user_from_data(request)
    value = clean_value(request)
    validate_username(request.settings, value, user)


@validation_view
def email(request: HttpRequest) -> JsonResponse:
    user = get_user_from_data(request)
    value = clean_value(request)
    validate_email(value, user)


@sensitive_post_parameters()
@validation_view
def password(request: HttpRequest) -> JsonResponse:
    user = get_user_from_data(request)
    value = clean_value(request, strip=False)
    validate_password(value, user)
