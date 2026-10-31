from django.db.models import Q
from django.dispatch import receiver

from ..users.signals import (
    archive_user_data,
    username_changed,
)
from .models import Notification
from .registry import registry
from .utils import update_actor_name as update_actor_name_util


@receiver(archive_user_data)
def archive_user_notifications(sender, archive=None, **kwargs):
    queryset = Notification.objects.filter(Q(user=sender) | Q(actor=sender)).order_by(
        "id"
    )

    for notification in queryset.iterator(chunk_size=50):
        item_name = notification.created_at.strftime("%H%M%S-notification")
        archive.add_text(
            item_name,
            registry.get_message(notification),
            date=notification.created_at,
        )


@receiver(username_changed)
def update_actor_name(sender, **kwargs):
    update_actor_name_util(sender)
