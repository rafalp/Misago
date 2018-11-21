import hashlib

from django.utils import timezone

from misago.users.models.deleteduser import DeletedUser


def hash_email(email):
    return hashlib.md5(email.lower().encode('utf-8')).hexdigest()


def record_user_deleted_by_self():
    return DeletedUser.objects.create(deleted_by=DeletedUser.DELETED_BY_USER)


def record_user_deleted_by_staff():
    return DeletedUser.objects.create(deleted_by=DeletedUser.DELETED_BY_STAFF)


def record_user_deleted_by_system():
    return DeletedUser.objects.create(deleted_by=DeletedUser.DELETED_BY_SYSTEM)
