from .models import DeletedUser


def record_user_deleted_by_self():
    return DeletedUser.objects.create(deleted_by=DeletedUser.DELETED_BY_SELF)


def record_user_deleted_by_staff():
    return DeletedUser.objects.create(deleted_by=DeletedUser.DELETED_BY_STAFF)


def record_user_deleted_by_system():
    return DeletedUser.objects.create(deleted_by=DeletedUser.DELETED_BY_SYSTEM)
