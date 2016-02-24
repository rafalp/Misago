from django.dispatch import receiver, Signal

from misago.categories.signals import move_category_content
from misago.threads.signals import move_thread, remove_thread_participant


all_read = Signal()
category_read = Signal(providing_args=["category"])
thread_tracked = Signal(providing_args=["thread"])
thread_read = Signal(providing_args=["thread"])


"""
Signal handlers
"""
@receiver(move_category_content)
def delete_category_tracker(sender, **kwargs):
    sender.categoryread_set.all().delete()
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


@receiver(thread_read)
def decrease_unread_private_count(sender, **kwargs):
    user = sender
    thread = kwargs['thread']
    if user.pk != thread.starter_id and user.unread_private_threads:
        user.unread_private_threads -= 1
        user.save(update_fields=['unread_private_threads'])


@receiver(all_read)
def zero_unread_counters(sender, **kwargs):
    sender.new_threads.set(0)
    sender.unread_threads.set(0)


@receiver(remove_thread_participant)
def remove_private_thread_readtrackers(sender, **kwargs):
    user = kwargs['user']
    user.threadread_set.filter(thread=sender).delete()
