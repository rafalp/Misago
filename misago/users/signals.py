from django.dispatch import receiver, Signal


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


from django.contrib.auth import get_user_model
from django.db.models.signals import pre_delete
@receiver(pre_delete, sender=get_user_model())
def recache_active_users_list_on_active_user_delete(sender, **kwargs):
    from misago.core.cache import cache
    from misago.users.activepostersranking import (get_active_posters_ranking,
                                                   clear_active_posters_ranking)

    for user in get_active_posters_ranking()['users']:
        if user == kwargs['instance']:
            clear_active_posters_ranking()


from misago.core.signals import secret_key_changed
@receiver(secret_key_changed)
def update_signatures_checksums(sender, **kwargs):
    User = get_user_model()

    for user in User.objects.iterator():
        if user.signature:
            new_checksum = make_signature_checksum(user.signature_parsed, user)
            user.signature_checksum = new_checksum
            user.save(update_fields=['signature_checksum'])