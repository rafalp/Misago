from celery import shared_task
from django.contrib.auth import get_user_model

from ..conf.shortcuts import get_dynamic_settings
from ..permissions.permissionsid import get_permissions_id
from .deletesrecord import record_user_deleted_by_self

NOTIFY_CHUNK_SIZE = 20

User = get_user_model()


@shared_task(name="users.remove-group", serializer="json")
def remove_group_from_users_groups_ids(group_id: int):
    queryset = User.objects.filter(groups_ids__contains=[group_id])
    for user in queryset.iterator(chunk_size=50):
        user.groups_ids.remove(group_id)
        user.permissions_id = get_permissions_id(user.groups_ids)
        user.save(update_fields=["groups_ids", "permissions_id"])


@shared_task(name="users.delete", serializer="json")
def delete_user(user_id: int):
    user = User.objects.filter(id=user_id).first()
    if not user:
        return

    record_user_deleted_by_self()

    settings = get_dynamic_settings()
    user.delete(anonymous_username=settings.anonymous_username)
