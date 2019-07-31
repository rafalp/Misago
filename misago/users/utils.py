import hashlib

from django.utils import timezone

from misago.users.models.deleteduser import DeletedUser


def hash_email(email):
    return hashlib.md5(email.lower().encode('utf-8')).hexdigest()

def record_user_deleted_by_self():
    return DeletedUser.objects.create(
        deleted_by=1
    )

def record_user_deleted_by_staff():
    return DeletedUser.objects.create(
        deleted_by=2
    )

def record_user_deleted_by_system():
    return DeletedUser.objects.create(
        deleted_by=3
    )
