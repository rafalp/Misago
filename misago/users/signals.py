import django.dispatch
from django.dispatch import receiver


delete_user_content = django.dispatch.Signal()
username_changed = django.dispatch.Signal()


"""
Signal handlers
"""
@receiver(username_changed)
def handle_name_change(sender, **kwargs):
    sender.user_renames.update(changed_by_username=sender.username,
                               changed_by_slug=sender.slug)
    sender.warnings_given.update(giver_username=sender.username,
                                 giver_slug=sender.slug)
    sender.warnings_canceled.update(canceler_username=sender.username,
                                    canceler_slug=sender.slug)
