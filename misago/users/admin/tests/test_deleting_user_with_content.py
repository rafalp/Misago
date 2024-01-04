import pytest
from django.contrib.auth import get_user_model

from ...models import DeletedUser
from ..tasks import delete_user_with_content

User = get_user_model()


def test_task_does_nothing_for_nonexisting_user_id(db):
    delete_user_with_content(1)


def test_task_does_nothing_for_staff_id(staffuser):
    delete_user_with_content(staffuser.id)
    staffuser.refresh_from_db()


def test_task_does_nothing_for_admin_id(admin):
    delete_user_with_content(admin.id)
    admin.refresh_from_db()


def test_task_deletes_user(user):
    delete_user_with_content(user.id)
    with pytest.raises(User.DoesNotExist):
        user.refresh_from_db()


def test_task_records_user_deletion(user):
    delete_user_with_content(user.id)
    DeletedUser.objects.get(deleted_by=DeletedUser.DELETED_BY_STAFF)
