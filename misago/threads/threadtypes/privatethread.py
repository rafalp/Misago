from django.urls import reverse
from django.utils.translation import pgettext_lazy

from . import ThreadType
from ...categories import PRIVATE_THREADS_ROOT_NAME


class PrivateThread(ThreadType):
    root_name = PRIVATE_THREADS_ROOT_NAME

    def get_category_name(self, category):
        return pgettext_lazy("private threads category name", "Private threads")

    def get_category_absolute_url(self, category):
        return reverse("misago:private-threads")

    def get_category_last_thread_url(self, category):
        return reverse(
            "misago:private-thread",
            kwargs={"slug": category.last_thread_slug, "id": category.last_thread_id},
        )

    def get_category_last_thread_new_url(self, category):
        return reverse(
            "misago:private-thread-unread-post",
            kwargs={"slug": category.last_thread_slug, "id": category.last_thread_id},
        )

    def get_category_last_post_url(self, category):
        return reverse(
            "misago:private-thread-last-post",
            kwargs={"slug": category.last_thread_slug, "id": category.last_thread_id},
        )

    def get_thread_absolute_url(self, thread, page=1):
        if page > 1:
            return reverse(
                "misago:private-thread",
                kwargs={"slug": thread.slug, "id": thread.id, "page": page},
            )

        return reverse(
            "misago:private-thread", kwargs={"slug": thread.slug, "id": thread.id}
        )

    def get_thread_last_post_url(self, thread):
        return reverse(
            "misago:private-thread-last-post",
            kwargs={"slug": thread.slug, "id": thread.pk},
        )

    def get_thread_new_post_url(self, thread):
        return reverse(
            "misago:private-thread-unread-post",
            kwargs={"slug": thread.slug, "id": thread.pk},
        )

    def get_thread_api_url(self, thread):
        return reverse("misago:api:private-thread-detail", kwargs={"pk": thread.pk})

    def get_thread_editor_api_url(self, thread):
        return reverse(
            "misago:api:private-thread-post-editor", kwargs={"thread_pk": thread.pk}
        )

    def get_thread_posts_api_url(self, thread):
        return reverse(
            "misago:api:private-thread-post-list", kwargs={"thread_pk": thread.pk}
        )

    def get_post_merge_api_url(self, thread):
        return reverse(
            "misago:api:private-thread-post-merge", kwargs={"thread_pk": thread.pk}
        )

    def get_post_absolute_url(self, post):
        return reverse(
            "misago:private-thread-post",
            kwargs={"slug": post.thread.slug, "pk": post.thread.pk, "post": post.pk},
        )

    def get_post_api_url(self, post):
        return reverse(
            "misago:api:private-thread-post-detail",
            kwargs={"thread_pk": post.thread_id, "pk": post.pk},
        )

    def get_post_likes_api_url(self, post):
        return reverse(
            "misago:api:private-thread-post-likes",
            kwargs={"thread_pk": post.thread_id, "pk": post.pk},
        )

    def get_post_editor_api_url(self, post):
        return reverse(
            "misago:api:private-thread-post-editor",
            kwargs={"thread_pk": post.thread_id, "pk": post.pk},
        )

    def get_post_edits_api_url(self, post):
        return reverse(
            "misago:api:private-thread-post-edits",
            kwargs={"thread_pk": post.thread_id, "pk": post.pk},
        )

    def get_thread_watch_api_url(self, thread):
        return reverse(
            "misago:apiv2:private-thread-watch", kwargs={"thread_id": thread.id}
        )
