from django.dispatch import receiver, Signal

from misago.forums.signals import move_forum_content
from misago.threads.signals import move_thread, remove_thread_participant


all_read = Signal()
forum_read = Signal(providing_args=["forum"])
thread_tracked = Signal(providing_args=["thread"])
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


@receiver(thread_tracked)
def decrease_new_threads_count(sender, **kwargs):
    user = sender
    thread = kwargs['thread']
    user.new_threads.decrease()


@receiver(thread_read)
def decrease_unread_count(sender, **kwargs):
    user = sender
    thread = kwargs['thread']
    user.unread_threads.decrease()


@receiver(all_read)
def zero_unread_counters(sender, **kwargs):
    sender.new_threads.set(0)
    sender.unread_threads.set(0)


@receiver(remove_thread_participant)
def remove_private_thread_readtrackers(sender, **kwargs):
    user = kwargs['user']
    user.threadread_set.filter(thread=sender).delete()
