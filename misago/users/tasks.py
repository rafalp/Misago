from celery import shared_task
from django.contrib.auth import get_user_model

from ..permissions.permissionsid import get_permissions_id
from . import delete
from .deletesrecord import record_user_deleted_by_self, record_user_deleted_by_staff
from .enums import DeleteUserContentAction

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
def delete_user(
    user_id: int,
    content_action: DeleteUserContentAction,
    anonymous_username: str,
    deleted_by_id: int | None = None,
):
    user = User.objects.filter(id=user_id).first()
    if not user:
        return

    delete.delete_user(
        user,
        content_action=content_action,
        anonymous_username=anonymous_username,
    )

    if user_id == deleted_by_id:
        record_user_deleted_by_self()
    else:
        record_user_deleted_by_staff()
