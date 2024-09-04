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
                "misago:category", kwargs={"id": category.id, "slug": category.slug}
            )

        return reverse("misago:threads")

    def get_category_last_thread_url(self, category):
        return reverse(
            "misago:thread",
            kwargs={"slug": category.last_thread_slug, "id": category.last_thread_id},
        )

    def get_category_last_thread_new_url(self, category):
        return reverse(
            "misago:thread-unread-post",
            kwargs={"slug": category.last_thread_slug, "id": category.last_thread_id},
        )

    def get_category_last_post_url(self, category):
        return reverse(
            "misago:thread-last-post",
            kwargs={"slug": category.last_thread_slug, "id": category.last_thread_id},
        )

    def get_thread_absolute_url(self, thread, page=1):
        if page > 1:
            return reverse(
                "misago:thread",
                kwargs={"slug": thread.slug, "id": thread.id, "page": page},
            )

        return reverse("misago:thread", kwargs={"slug": thread.slug, "id": thread.id})

    def get_thread_last_post_url(self, thread):
        return reverse(
            "misago:thread-last-post", kwargs={"slug": thread.slug, "id": thread.pk}
        )

    def get_thread_new_post_url(self, thread):
        return reverse(
            "misago:thread-unread-post", kwargs={"slug": thread.slug, "id": thread.pk}
        )

    def get_thread_best_answer_url(self, thread):
        return reverse(
            "misago:thread-solution-post", kwargs={"slug": thread.slug, "id": thread.pk}
        )

    def get_thread_unapproved_post_url(self, thread):
        return reverse(
            "misago:thread-unapproved-post",
            kwargs={"slug": thread.slug, "id": thread.pk},
        )

    def get_thread_api_url(self, thread):
        return reverse("misago:api:thread-detail", kwargs={"pk": thread.pk})

    def get_thread_editor_api_url(self, thread):
        return reverse("misago:api:thread-post-editor", kwargs={"thread_pk": thread.pk})

    def get_thread_merge_api_url(self, thread):
        return reverse("misago:api:thread-merge", kwargs={"pk": thread.pk})

    def get_thread_poll_api_url(self, thread):
        return reverse("misago:api:thread-poll-list", kwargs={"thread_pk": thread.pk})

    def get_thread_watch_api_url(self, thread):
        return reverse("misago:apiv2:thread-watch", kwargs={"thread_id": thread.id})

    def get_thread_posts_api_url(self, thread):
        return reverse("misago:api:thread-post-list", kwargs={"thread_pk": thread.pk})

    def get_poll_api_url(self, poll):
        return reverse(
            "misago:api:thread-poll-detail",
            kwargs={"thread_pk": poll.thread_id, "pk": poll.pk},
        )

    def get_poll_votes_api_url(self, poll):
        return reverse(
            "misago:api:thread-poll-votes",
            kwargs={"thread_pk": poll.thread_id, "pk": poll.pk},
        )

    def get_post_merge_api_url(self, thread):
        return reverse("misago:api:thread-post-merge", kwargs={"thread_pk": thread.pk})

    def get_post_move_api_url(self, thread):
        return reverse("misago:api:thread-post-move", kwargs={"thread_pk": thread.pk})

    def get_post_split_api_url(self, thread):
        return reverse("misago:api:thread-post-split", kwargs={"thread_pk": thread.pk})

    def get_post_absolute_url(self, post):
        return reverse(
            "misago:thread-post",
            kwargs={"slug": post.thread.slug, "pk": post.thread.pk, "post": post.pk},
        )

    def get_post_api_url(self, post):
        return reverse(
            "misago:api:thread-post-detail",
            kwargs={"thread_pk": post.thread_id, "pk": post.pk},
        )

    def get_post_likes_api_url(self, post):
        return reverse(
            "misago:api:thread-post-likes",
            kwargs={"thread_pk": post.thread_id, "pk": post.pk},
        )

    def get_post_editor_api_url(self, post):
        return reverse(
            "misago:api:thread-post-editor",
            kwargs={"thread_pk": post.thread_id, "pk": post.pk},
        )

    def get_post_edits_api_url(self, post):
        return reverse(
            "misago:api:thread-post-edits",
            kwargs={"thread_pk": post.thread_id, "pk": post.pk},
        )
