from django.dispatch import receiver, Signal

from misago.forums.signals import move_forum_content
from misago.threads.signals import move_thread


forum_read = Signal(providing_args=["forum"])
thread_read = Signal(providing_args=["thread"])


"""
Signal handlers
"""
@receiver(move_forum_content)
def delete_forum_tracker(sender, **kwargs):
    sender.forumread_set.all().delete()
    sender.threadread_set.all().delete()


@receiver(move_thread)
def delete_thread_tracker(sender, **kwargs):
    sender.threadread_set.all().delete()
