from django.dispatch import receiver

from ..users.signals import (
    anonymize_user_data,
    username_changed,
)
from .models import Notification


@receiver([anonymize_user_data, username_changed])
def update_usernames(sender, **kwargs):
    Notification.objects.filter(actor=sender).update(actor_name=sender.username)
