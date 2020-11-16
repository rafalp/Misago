from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from . import ThreadType
from ...categories import PRIVATE_THREADS_ROOT_NAME


class PrivateThread(ThreadType):
    root_name = PRIVATE_THREADS_ROOT_NAME

    def get_category_name(self, category):
        return _("Private threads")

    def get_category_absolute_url(self, category):
        return reverse("misago:private-threads")

    def get_category_last_thread_url(self, category):
        return reverse(
            "misago:private-thread",
            kwargs={"slug": category.last_thread_slug, "pk": category.last_thread_id},
        )

    def get_category_last_thread_new_url(self, category):
        return reverse(
            "misago:private-thread-new",
            kwargs={"slug": category.last_thread_slug, "pk": category.last_thread_id},
        )

    def get_category_last_post_url(self, category):
        return reverse(
            "misago:private-thread-last",
            kwargs={"slug": category.last_thread_slug, "pk": category.last_thread_id},
        )

    def get_thread_absolute_url(self, thread, page=1):
        if page > 1:
            return reverse(
                "misago:private-thread",
                kwargs={"slug": thread.slug, "pk": thread.pk, "page": page},
            )

        return reverse(
            "misago:private-thread", kwargs={"slug": thread.slug, "pk": thread.pk}
        )

    def get_thread_last_post_url(self, thread):
        return reverse(
            "misago:private-thread-last", kwargs={"slug": thread.slug, "pk": thread.pk}
        )

    def get_thread_new_post_url(self, thread):
        return reverse(
            "misago:private-thread-new", kwargs={"slug": thread.slug, "pk": thread.pk}
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

    def get_post_read_api_url(self, post):
        return reverse(
            "misago:api:private-thread-post-read",
            kwargs={"thread_pk": post.thread_id, "pk": post.pk},
        )
