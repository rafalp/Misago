from django.dispatch import receiver
from django.db.models import Q

from ..users.signals import (
    anonymize_user_data,
    delete_user_content,
    username_changed,
)
from .models import Notification, WatchedThread


@receiver([anonymize_user_data, username_changed])
def update_actor_name(sender, **kwargs):
    Notification.objects.filter(actor=sender).update(actor_name=sender.username)


@receiver(delete_user_content)
def delete_user_data(sender, **kwargs):
    Notification.objects.filter(Q(user=sender) | Q(actor=sender)).delete()
    WatchedThread.objects.filter(user=sender).delete()
