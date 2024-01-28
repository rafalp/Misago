from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models import Q
from django.db.models.signals import pre_delete

from ..users.signals import (
    anonymize_user_data,
    archive_user_data,
    delete_user_content,
    username_changed,
)
from .registry import registry
from .models import Notification, WatchedThread


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


@receiver([anonymize_user_data, username_changed])
def update_actor_name(sender, **kwargs):
    Notification.objects.filter(actor=sender).update(actor_name=sender.username)


@receiver(delete_user_content)
def delete_user_data(sender, **kwargs):
    Notification.objects.filter(Q(user=sender) | Q(actor=sender)).delete()
    WatchedThread.objects.filter(user=sender).delete()


@receiver(pre_delete, sender=get_user_model())
def delete_user_account(sender, *, instance, **kwargs):
    Notification.objects.filter(actor=instance).update(actor=None)
    Notification.objects.filter(user=instance).delete()
    WatchedThread.objects.filter(user=instance).delete()
