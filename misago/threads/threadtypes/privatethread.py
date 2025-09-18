from django.urls import reverse
from django.utils.translation import pgettext_lazy

from . import ThreadType
from ...categories import PRIVATE_THREADS_ROOT_NAME


class PrivateThread(ThreadType):
    root_name = PRIVATE_THREADS_ROOT_NAME

    def get_category_name(self, category):
        return pgettext_lazy("private threads category name", "Private threads")

    def get_category_absolute_url(self, category):
        return reverse("misago:private-thread-list")

    def get_category_last_thread_url(self, category):
        return reverse(
            "misago:private-thread",
            kwargs={"slug": category.last_thread_slug, "id": category.last_thread_id},
        )

    def get_category_last_thread_new_url(self, category):
        return reverse(
            "misago:private-thread-post-unread",
            kwargs={"slug": category.last_thread_slug, "id": category.last_thread_id},
        )

    def get_category_last_post_url(self, category):
        return reverse(
            "misago:private-thread-post-last",
            kwargs={"slug": category.last_thread_slug, "id": category.last_thread_id},
        )

    def get_thread_absolute_url(self, thread, page=1):
        if page > 1:
            return reverse(
                "misago:private-thread",
                kwargs={"slug": thread.slug, "thread_id": thread.id, "page": page},
            )

        return reverse(
            "misago:private-thread",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )

    def get_thread_last_post_url(self, thread):
        return reverse(
            "misago:private-thread-post-last",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )

    def get_thread_new_post_url(self, thread):
        return reverse(
            "misago:private-thread-post-unread",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
