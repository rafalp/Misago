from django.urls import reverse

from ..categories.enums import CategoryTree
from ..categories.models import Category
from .models import Thread


def get_thread_url(thread: Thread, category: Category | None = None) -> str:
    return _get_thread_url_action(thread, category)


def _get_thread_url_action(thread: Thread, category: Category | None = None) -> str:
    tree_id = (category or thread.category).tree_id

    if tree_id == CategoryTree.THREADS:
        return reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})

    if tree_id == CategoryTree.PRIVATE_THREADS:
        return reverse(
            "misago:private-thread", kwargs={"id": thread.id, "slug": thread.slug}
        )

    raise ValueError(
        f"Don't know how to build a thread URL for category tree ID: {tree_id}"
    )
