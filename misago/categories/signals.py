from django.dispatch import Signal, receiver

from misago.users.signals import anonymize_user_content, username_changed

from .models import Category


delete_category_content = Signal()
move_category_content = Signal(providing_args=["new_category"])


@receiver([anonymize_user_content, username_changed])
def update_usernames(sender, **kwargs):
    Category.objects.filter(last_poster=sender).update(
        last_poster_name=sender.username,
        last_poster_slug=sender.slug,
    )
