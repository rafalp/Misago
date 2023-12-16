from dataclasses import dataclass

from django.contrib.auth import get_user_model
from django.forms import ValidationError
from django.utils.crypto import get_random_string
from unidecode import unidecode

from ..users.validators import (
    dj_validate_email,
    validate_username_content,
    validate_username_length,
)
from .exceptions import OAuth2UserDataValidationError
from .hooks import filter_user_data_hook, validate_user_data_hook

User = get_user_model()


class UsernameSettings:
    username_length_max: int = 200
    username_length_min: int = 1


def validate_user_data(request, user, user_data, response_json):
    try:
        return validate_user_data_hook(
            validate_user_data_action,
            request,
            user,
            user_data,
            response_json,
        )
    except ValidationError as exc:
        raise OAuth2UserDataValidationError(error_list=[str(exc.message)])


def validate_user_data_action(request, user, user_data, response_json):
    filtered_data = filter_user_data(request, user, user_data)
    validate_username_content(filtered_data["name"])
    validate_username_length(UsernameSettings, filtered_data["name"])
    dj_validate_email(filtered_data["email"])
    return filtered_data


def filter_user_data(request, user, user_data):
    return filter_user_data_hook(filter_user_data_action, request, user, user_data)


def filter_user_data_action(request, user, user_data):
    return {
        "id": user_data["id"],
        "name": filter_name(user, user_data["name"] or ""),
        "email": user_data["email"] or "",
        "avatar": user_data["avatar"],
    }


def filter_user_data_with_filters(request, user, user_data, filters):
    for filter_user_data in filters:
        user_data = filter_user_data(request, user, user_data.copy()) or user_data
    return user_data


def filter_name(user, name):
    if user and user.username == name:
        return name

    clean_name = "".join(
        [c for c in unidecode(name.replace(" ", "_")) if c.isalnum() or c == "_"]
    )

    if user and user.username == clean_name:
        return clean_name  # No change in name

    if not clean_name.replace("_", ""):
        clean_name = "User_%s" % get_random_string(4)

    clean_name_root = clean_name
    while True:
        try:
            db_user = User.objects.get_by_username(clean_name)
        except User.DoesNotExist:
            return clean_name

        if not user or user.pk != db_user.pk:
            clean_name = f"{clean_name_root}_{get_random_string(4)}"
        else:
            return clean_name
