import django.dispatch
from django.dispatch import receiver

from misago.core import serializer

from misago.forums.models import Forum, ForumRole


delete_forum_content = django.dispatch.Signal()
move_forum_content = django.dispatch.Signal()


"""
Signal handlers
"""
from misago.core.signals import secret_key_changed
@receiver(secret_key_changed)
def update_roles_pickles(sender, **kwargs):
    for role in ForumRole.objects.iterator():
        if role.pickled_permissions:
            role.pickled_permissions = serializer.regenerate_checksum(
                role.pickled_permissions)
            role.save(update_fields=['pickled_permissions'])


from misago.users.signals import username_changed
@receiver(username_changed)
def update_usernames(sender, **kwargs):
    Forum.objects.filter(last_poster=sender).update(
        last_poster_name=sender.username,
        last_poster_slug=sender.slug)
