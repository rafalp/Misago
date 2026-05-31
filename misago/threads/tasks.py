from celery import shared_task

from ..categories.tasks import synchronize_categories as synchronize_categories_task
from .models import Thread
from .synchronize import synchronize_thread


@shared_task(name="threads.synchronize", serializer="json")
def synchronize_threads(thread_ids: list[int], synchronize_categories: bool = False):
    category_ids: set[int] = set()

    for thread in Thread.objects.filter(id__in=thread_ids):
        synchronize_thread(thread)
        category_ids.add(thread.category_id)

    if synchronize_categories:
        synchronize_categories_task(category_ids)
