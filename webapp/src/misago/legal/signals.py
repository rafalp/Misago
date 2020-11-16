from django.dispatch import receiver

from ..users.signals import anonymize_user_data, username_changed
from .models import Agreement


@receiver([anonymize_user_data, username_changed])
def update_usernames(sender, **kwargs):
    Agreement.objects.filter(created_by=sender).update(created_by_name=sender.username)

    Agreement.objects.filter(last_modified_by=sender).update(
        last_modified_by_name=sender.username
    )
