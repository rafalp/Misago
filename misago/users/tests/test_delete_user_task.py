import pytest
from django.contrib.auth import get_user_model

from ..enums import DeleteUserContentAction
from ..models.deleteduser import DeletedUser
from ..tasks import delete_user

User = get_user_model()


def test_delete_user_task_deletes_user(user):
    delete_user(
        user.id,
        content_action=DeleteUserContentAction.LEAVE,
        anonymous_username="Anonymous",
        deleted_by_id=1,
    )

    with pytest.raises(User.DoesNotExist):
        user.refresh_from_db()


def test_delete_user_task_records_user_deletion(user):
    delete_user(
        user.id,
        content_action=DeleteUserContentAction.LEAVE,
        anonymous_username="Anonymous",
        deleted_by_id=1,
    )

    assert DeletedUser.objects.exists()


def test_delete_user_task_does_nothing_if_user_is_not_found(user):
    delete_user(
        user.id + 1,
        content_action=DeleteUserContentAction.LEAVE,
        anonymous_username="Anonymous",
        deleted_by_id=1,
    )

    user.refresh_from_db()
