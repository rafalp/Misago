from celery import shared_task
from django.contrib.auth import get_user_model

from ...conf.shortcuts import get_dynamic_settings
from ..deletesrecord import record_user_deleted_by_staff

User = get_user_model()


@shared_task
def delete_user_with_content(id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return

    if not user.is_misago_admin and not user.is_staff:
        settings = get_dynamic_settings()
        user.delete(anonymous_username=settings.anonymous_username, delete_content=True)
        record_user_deleted_by_staff()
