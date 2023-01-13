from django.contrib.auth import get_user_model
from django.utils import timezone

from ..users.setupnewuser import setup_new_user
from .exceptions import OAuth2UserIdNotProvidedError
from .models import Subject
from .validation import validate_user_data

User = get_user_model()


def get_user_from_data(request, user_data):
    if not user_data["id"]:
        raise OAuth2UserIdNotProvidedError()

    user = get_user_by_subject(user_data["id"])
    if not user and user_data["email"]:
        user = get_user_by_email(user_data["id"], user_data["email"])

    created = not bool(user)

    cleaned_data = validate_user_data(request, user, user_data)

    # TODO: recover from email conflict error!
    if not user:
        user = create_new_user(request, cleaned_data)
    else:
        update_existing_user(request, user, cleaned_data)

    return user, created


def get_user_by_subject(user_id):
    try:
        subject = Subject.objects.select_related("user").get(sub=user_id)
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


def update_existing_user(request, user, user_data):
    save_changes = False

    if user.username != user_data["name"]:
        user.set_username(user_data["name"])
        save_changes = True

    if user.email != user_data["email"]:
        user.set_email(user_data["email"])
        save_changes = True

    if save_changes:
        user.save()
