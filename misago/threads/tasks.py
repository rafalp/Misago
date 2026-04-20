from celery import shared_task

from .models import Thread
from .synchronize import synchronize_thread


@shared_task(name="threads.synchronize", serializer="json")
def synchronize_threads(thread_ids: list[int]):
    for thread in Thread.objects.filter(id__in=thread_ids):
        synchronize_thread(thread)
