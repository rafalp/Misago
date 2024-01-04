from celery import shared_task
from django.contrib.auth import get_user_model

from ..permissions.permissionsid import get_permissions_id


NOTIFY_CHUNK_SIZE = 20

User = get_user_model()


@shared_task(name="users.remove-group", serializer="json")
def remove_group_from_users_groups_ids(group_id: int):
    queryset = User.objects.filter(groups_ids__contains=[group_id])
    for user in queryset.order_by("-id").iterator(chunk_size=20):
        user.groups_ids.remove(group_id)
        user.permissions_id = get_permissions_id(user.groups_ids)
        user.save(update_fields=["groups_ids", "permissions_id"])
