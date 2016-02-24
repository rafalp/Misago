from django.dispatch import receiver, Signal
from misago.core import serializer
from misago.categories.models import Category, CategoryRole


delete_category_content = Signal()
move_category_content = Signal(providing_args=["new_category"])


"""
Signal handlers
"""
from misago.core.signals import secret_key_changed
@receiver(secret_key_changed)
def update_roles_pickles(sender, **kwargs):
    for role in CategoryRole.objects.iterator():
        if role.pickled_permissions:
            role.pickled_permissions = serializer.regenerate_checksum(
                role.pickled_permissions)
            role.save(update_fields=['pickled_permissions'])


from misago.users.signals import username_changed
@receiver(username_changed)
def update_usernames(sender, **kwargs):
    Category.objects.filter(last_poster=sender).update(
        last_poster_name=sender.username,
        last_poster_slug=sender.slug
    )
