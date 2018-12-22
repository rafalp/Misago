from django.db import models


def create_audit_trail(request, obj):
    return create_user_audit_trail(request.user, request.user_ip, obj)


def create_user_audit_trail(user, ip_address, obj):
    if not isinstance(obj, models.Model):
        raise ValueError("obj must be a valid Django model instance")

    if user.is_anonymous:
        return None

    return user.audittrail_set.create(
        user=user, ip_address=ip_address, content_object=obj
    )
