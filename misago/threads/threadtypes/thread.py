from django.urls import reverse
from django.utils.translation import pgettext_lazy

from . import ThreadType
from ...categories import THREADS_ROOT_NAME


class Thread(ThreadType):
    root_name = THREADS_ROOT_NAME

    def get_category_name(self, category):
        if category.level:
            return category.name
        return pgettext_lazy(
            "threads root category name", "None (will become top level category)"
        )

    def get_category_absolute_url(self, category):
        if category.level:
            return reverse(
                "misago:category-thread-list",
                kwargs={"category_id": category.id, "slug": category.slug},
            )

        return reverse("misago:thread-list")

    def get_category_last_thread_url(self, category):
        return reverse(
            "misago:thread",
            kwargs={
                "thread_id": category.last_thread_id,
                "slug": category.last_thread_slug,
            },
        )

    def get_category_last_thread_new_url(self, category):
        return reverse(
            "misago:thread-post-unread",
            kwargs={"slug": category.last_thread_slug, "id": category.last_thread_id},
        )

    def get_category_last_post_url(self, category):
        return reverse(
            "misago:thread-post-last",
            kwargs={"slug": category.last_thread_slug, "id": category.last_thread_id},
        )

    def get_thread_absolute_url(self, thread, page=1):
        if page > 1:
            return reverse(
                "misago:thread",
                kwargs={"thread_id": thread.id, "slug": thread.slug, "page": page},
            )

        return reverse(
            "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
        )

    def get_thread_last_post_url(self, thread):
        return reverse(
            "misago:thread-post-last",
            kwargs={"slug": thread.slug, "thread_id": thread.id},
        )

    def get_thread_new_post_url(self, thread):
        return reverse(
            "misago:thread-post-unread",
            kwargs={"slug": thread.slug, "thread_id": thread.id},
        )

    def get_thread_best_answer_url(self, thread):
        return reverse(
            "misago:thread-post-solution",
            kwargs={"slug": thread.slug, "thread_id": thread.id},
        )

    def get_thread_unapproved_post_url(self, thread):
        return reverse(
            "misago:thread-post-unapproved",
            kwargs={"slug": thread.slug, "id": thread.id},
        )
