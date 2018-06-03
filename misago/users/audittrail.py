from django.db import models

from .models import AuditTrail


def create_user_audit_trail(request, obj):
    if not isinstance(obj, models.Model):
        raise ValueError("obj must be a valid Django model instance")

    if request.user.is_anonymous:
        return None

    return AuditTrail.objects.create(
        user=request.user,
        ip_address=request.user_ip,
        content_object=obj,
    )
