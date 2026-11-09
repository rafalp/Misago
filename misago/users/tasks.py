from celery import shared_task
from django.contrib.auth import get_user_model

# from ..conf.shortcuts import get_dynamic_settings
from ..permissions.permissionsid import get_permissions_id
from .delete import delete_user as delete_user_util
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

    delete_user_util(
        user,
        content_action=content_action,
        anonymous_username=anonymous_username,
    )

    if user_id == deleted_by_id:
        record_user_deleted_by_self()
    else:
        record_user_deleted_by_staff()


# @shared_task
# def delete_user_with_content(id):
#     try:
#         user = User.objects.get(id=id)
#     except User.DoesNotExist:
#         return
#     if not user.is_misago_admin and not user.is_staff:
#
#         settings = get_dynamic_settings()
#         delete_user_util(
#             user,
#             content_action=DeleteUserContentAction.DELETE,
#             anonymous_username=settings.anonymous_username,
#         )
#         record_user_deleted_by_staff()
