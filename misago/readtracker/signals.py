from django.dispatch import Signal, receiver

from ..categories.signals import delete_category_content, move_category_content
from ..threads.signals import merge_thread, move_thread

thread_read = Signal()


@receiver(delete_category_content)
def delete_category_threads(sender, **kwargs):
    sender.readthread_set.all().delete()
    sender.readcategory_set.all().delete()


@receiver(move_category_content)
def move_category_tracker(sender, **kwargs):
    sender.readthread_set.update(category=kwargs["new_category"])
    sender.readcategory_set.update(category=kwargs["new_category"])


@receiver(merge_thread)
def merge_thread_tracker(sender, **kwargs):
    other_thread = kwargs["other_thread"]
    other_thread.readthread_set.all().delete()


@receiver(move_thread)
def move_thread_tracker(sender, **kwargs):
    sender.readthread_set.update(category=sender.category, thread=sender)
