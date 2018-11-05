from django.utils import timezone

from misago.users.models.deleteduser import DeletedUser

import hashlib


def hash_email(email):
    return hashlib.md5(email.lower().encode('utf-8')).hexdigest()

def create_user_deletion(deleted_by, deleted_on=timezone.now()):
    return DeletedUser.objects.create(
        deleted_by=deleted_by,
        deleted_on=deleted_on
    )
