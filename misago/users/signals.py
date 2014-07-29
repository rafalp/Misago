import django.dispatch
from django.dispatch import receiver


delete_user_content = django.dispatch.Signal()
username_changed = django.dispatch.Signal()


"""
Register default signal handlers
"""
@receiver(username_changed)
def sync_username_in_user_models(sender, **kwargs):
    sender.user_renames.update(changed_by_username=sender.username,
                               changed_by_slug=sender.slug)
