from django.utils import timezone

from .exceptions import OAuth2UserIdNotProvidedError
from .models import Subject
from .validation import validate_user_data


def get_user_from_data(request, user_data):
    if not user_data["id"]:
        raise OAuth2UserIdNotProvidedError()

    user = get_user_by_subject(user_data["id"])
    is_created = bool(user)

    clean_data = validate_user_data(request, user, user_data)

    return user, is_created


def get_user_by_subject(user_id):
    try:
        subject = Subject.objects.select_related("user").get(sub=user_id)
        subject.last_used_on = timezone.now()
        subject.save(update_fields=["last_used_on"])
        return subject.user
    except Subject.DoesNotExist:
        return None
