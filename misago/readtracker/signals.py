from django.dispatch import Signal, receiver

from ..threads.signals import merge_thread, move_thread

thread_read = Signal()


@receiver(merge_thread)
def merge_thread_tracker(sender, **kwargs):
    other_thread = kwargs["other_thread"]
    other_thread.readthread_set.all().delete()


@receiver(move_thread)
def move_thread_tracker(sender, **kwargs):
    sender.readthread_set.update(category=sender.category, thread=sender)
