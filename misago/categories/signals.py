from django.dispatch import Signal, receiver

from ..users.signals import username_changed
from .utils import update_usernames as update_usernames_util


@receiver(username_changed)
def update_usernames(sender, **kwargs):
    update_usernames_util(sender)
