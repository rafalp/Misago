from ..deletesrecord import (
    record_user_deleted_by_self,
    record_user_deleted_by_staff,
    record_user_deleted_by_system,
)
from ..models import DeletedUser


def test_deletion_by_self_creates_record(db):
    record_user_deleted_by_self()
    DeletedUser.objects.get(deleted_by=DeletedUser.DELETED_BY_SELF)


def test_deletion_by_staff_creates_record(db):
    record_user_deleted_by_staff()
    DeletedUser.objects.get(deleted_by=DeletedUser.DELETED_BY_STAFF)


def test_deletion_by_system_creates_record(db):
    record_user_deleted_by_system()
    DeletedUser.objects.get(deleted_by=DeletedUser.DELETED_BY_SYSTEM)
