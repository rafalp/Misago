from django.urls import reverse

from ..permissions.checkutils import check_permissions
from ..permissions.privatethreads import (
    check_edit_private_thread_post_permission,
)
from ..threads.models import Post
from ..threads.postfeed import PostFeed
from ..threadupdates.models import ThreadUpdate


class PrivateThreadPostFeed(PostFeed):
    def get_moderator_status(self) -> bool:
        return self.request.user_permissions.is_private_threads_moderator

    def allow_edit_post(self, post: Post) -> bool:
        with check_permissions() as can_edit_post:
            check_edit_private_thread_post_permission(
                self.request.user_permissions, self.thread, post
            )

        return can_edit_post

    def get_edit_thread_post_url(self) -> str | None:
        return reverse(
            "misago:private-thread-edit",
            kwargs={"thread_id": self.thread.id, "slug": self.thread.slug},
        )

    def get_edit_post_url(self, post: Post) -> str | None:
        return reverse(
            "misago:private-thread-post-edit",
            kwargs={
                "thread_id": self.thread.id,
                "slug": self.thread.slug,
                "post_id": post.id,
            },
        )

    def get_post_edits_url(self, post: Post) -> str | None:
        return reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": self.thread.id,
                "slug": self.thread.slug,
                "post_id": post.id,
            },
        )

    def get_post_likes_url(self, post: Post) -> str | None:
        return reverse(
            "misago:private-thread-post-likes",
            kwargs={
                "thread_id": self.thread.id,
                "slug": self.thread.slug,
                "post_id": post.id,
            },
        )

    def get_post_like_url(self, post: Post) -> str | None:
        return reverse(
            "misago:private-thread-post-like",
            kwargs={
                "thread_id": self.thread.id,
                "slug": self.thread.slug,
                "post_id": post.id,
            },
        )

    def get_post_unlike_url(self, post: Post) -> str | None:
        return reverse(
            "misago:private-thread-post-unlike",
            kwargs={
                "thread_id": self.thread.id,
                "slug": self.thread.slug,
                "post_id": post.id,
            },
        )

    def get_hide_thread_update_url(self, thread_update: ThreadUpdate) -> str | None:
        return reverse(
            "misago:private-thread-update-hide",
            kwargs={
                "thread_id": self.thread.id,
                "slug": self.thread.slug,
                "thread_update_id": thread_update.id,
            },
        )

    def get_unhide_thread_update_url(self, thread_update: ThreadUpdate) -> str | None:
        return reverse(
            "misago:private-thread-update-unhide",
            kwargs={
                "thread_id": self.thread.id,
                "slug": self.thread.slug,
                "thread_update_id": thread_update.id,
            },
        )

    def get_delete_thread_update_url(self, thread_update: ThreadUpdate) -> str | None:
        return reverse(
            "misago:private-thread-update-delete",
            kwargs={
                "thread_id": self.thread.id,
                "slug": self.thread.slug,
                "thread_update_id": thread_update.id,
            },
        )
