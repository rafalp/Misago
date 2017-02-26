from django.dispatch import Signal, receiver

from misago.categories import PRIVATE_THREADS_ROOT_NAME
from misago.categories.signals import delete_category_content, move_category_content
from misago.threads.signals import move_thread


all_read = Signal()
category_read = Signal(providing_args=["category"])
thread_tracked = Signal(providing_args=["thread"])
thread_read = Signal(providing_args=["thread"])


@receiver(delete_category_content)
def delete_category_threads(sender, **kwargs):
    sender.categoryread_set.all().delete()
    sender.threadread_set.all().delete()


@receiver(move_category_content)
def delete_category_tracker(sender, **kwargs):
    sender.categoryread_set.all().delete()
    sender.threadread_set.all().delete()


@receiver(move_thread)
def delete_thread_tracker(sender, **kwargs):
    sender.threadread_set.all().delete()


@receiver(thread_read)
def decrease_unread_private_count(sender, **kwargs):
    user = sender
    thread = kwargs['thread']

    if thread.category.thread_type.root_name != PRIVATE_THREADS_ROOT_NAME:
        return

    if user.unread_private_threads:
        user.unread_private_threads -= 1
        user.save(update_fields=['unread_private_threads'])
