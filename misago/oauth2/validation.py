from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from unidecode import unidecode

from ..hooks import oauth2_user_data_filters

User = get_user_model()


def validate_user_data(request, user, user_data):
    filtered_data = filter_user_data(request, user, user_data)

    return filtered_data


def filter_user_data(request, user, user_data):
    if oauth2_user_data_filters:
        return filter_user_data_with_filters(
            request, user, user_data, oauth2_user_data_filters
        )

    if user_data["name"]:
        user_data["name"] = filter_name(user, user_data["name"])

    return user_data


def filter_user_data_with_filters(request, user, user_data, filters):
    for filter_ in filters:
        user_data = filter_(request, user, user_data) or user_data
    return user_data


def filter_name(user, name):
    clean_name = "".join(
        [c for c in unidecode(name.replace(" ", "_")) if c.isalnum() or c == "_"]
    )

    if not clean_name:
        clean_name = "User_%s" % get_random_string(4)

    if user and user.username == clean_name:
        return clean_name  # No change in name

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
