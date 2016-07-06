from django.contrib.auth import get_user_model
from django.dispatch import Signal, receiver

from misago.core.signals import secret_key_changed


delete_user_content = Signal()
username_changed = Signal()


"""
Signal handlers
"""
@receiver(username_changed)
def handle_name_change(sender, **kwargs):
    sender.user_renames.update(changed_by_username=sender.username)
    sender.warnings_given.update(giver_username=sender.username,
                                 giver_slug=sender.slug)
    sender.warnings_canceled.update(canceler_username=sender.username,
                                    canceler_slug=sender.slug)


@receiver(secret_key_changed)
def update_signatures_checksums(sender, **kwargs):
    User = get_user_model()

    for user in User.objects.iterator():
        if user.signature:
            new_checksum = make_signature_checksum(user.signature_parsed, user)
            user.signature_checksum = new_checksum
            user.save(update_fields=['signature_checksum'])
