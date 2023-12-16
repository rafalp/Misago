from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.utils import timezone
from django.utils.translation import pgettext_lazy

from ..users.setupnewuser import setup_new_user
from .exceptions import OAuth2UserDataValidationError, OAuth2UserIdNotProvidedError
from .models import Subject
from .validation import validate_user_data

User = get_user_model()


def get_user_from_data(request, user_data, user_data_raw):
    if not user_data["id"]:
        raise OAuth2UserIdNotProvidedError()

    user = get_user_by_subject(user_data["id"])
    if not user and user_data["email"]:
        user = get_user_by_email(user_data["id"], user_data["email"])

    created = not bool(user)

    cleaned_data = validate_user_data(request, user, user_data, user_data_raw)

    try:
        with transaction.atomic():
            if not user:
                user = create_new_user(request, cleaned_data)
            else:
                update_existing_user(user, cleaned_data)
    except IntegrityError as error:
        raise_validation_error_from_integrity_error(error)

    return user, created


def get_user_by_subject(user_id):
    try:
        subject = Subject.objects.select_related("user", "user__ban_cache").get(
            sub=user_id
        )
        subject.last_used_on = timezone.now()
        subject.save(update_fields=["last_used_on"])
        return subject.user
    except Subject.DoesNotExist:
        return None


def get_user_by_email(user_id, user_email):
    try:
        user = User.objects.get_by_email(user_email)
        Subject.objects.create(sub=user_id, user=user)
    except User.DoesNotExist:
        return None


def create_new_user(request, user_data):
    activation_kwargs = {}
    if request.settings.account_activation == "admin":
        activation_kwargs = {"requires_activation": User.ACTIVATION_ADMIN}

    user = User.objects.create_user(
        user_data["name"],
        user_data["email"],
        joined_from_ip=request.user_ip,
        **activation_kwargs,
    )

    setup_new_user(request.settings, user, avatar_url=user_data["avatar"])
    Subject.objects.create(sub=user_data["id"], user=user)

    return user


def update_existing_user(user, user_data):
    save_changes = False

    if user.username != user_data["name"]:
        user.set_username(user_data["name"])
        save_changes = True

    if user.email != user_data["email"]:
        user.set_email(user_data["email"])
        save_changes = True

    if save_changes:
        user.save()


def raise_validation_error_from_integrity_error(error):
    error_str = str(error)

    if "misago_users_user_email_hash_key" in error_str:
        raise OAuth2UserDataValidationError(
            error_list=[
                pgettext_lazy(
                    "oauth2 error",
                    "Your e-mail address returned by the provider is not available for use on this site.",
                )
            ]
        )

    if "misago_users_user_slug_key" in error_str:
        raise OAuth2UserDataValidationError(
            error_list=[
                pgettext_lazy(
                    "oauth2 error",
                    "Your username returned by the provider is not available for use on this site.",
                )
            ]
        )
