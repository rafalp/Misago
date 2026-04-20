from celery import shared_task

from .models import Category
from .synchronize import synchronize_category


@shared_task(name="categories.synchronize", serializer="json")
def synchronize_categories(category_ids: list[int]):
    for category in Category.objects.filter(id__in=category_ids):
        synchronize_category(category)
