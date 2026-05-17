from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.utils.translation import pgettext, pgettext_lazy

from ..categories.tasks import synchronize_categories
from ..permissions.proxy import UserPermissionsProxy
from ..threads.delete import delete_post
from ..threads.models import Thread
from ..threads.synchronize import synchronize_thread
from .actions import (
    ModerationActionResult,
    PostsModerationAction,
    FormMixin,
    ConfirmMixin,
)
from .forms import SplitPostsForm
from .hooks import (
    get_private_thread_posts_moderation_actions_hook,
    get_thread_posts_moderation_actions_hook,
)


def get_thread_posts_moderation_actions(
    user_permissions: UserPermissionsProxy,
    thread: Thread,
    request: HttpRequest | None = None,
) -> list[type[PostsModerationAction]]:
    return get_thread_posts_moderation_actions_hook(
        _get_thread_posts_moderation_actions_action,
        user_permissions,
        thread,
        request,
    )


def _get_thread_posts_moderation_actions_action(
    user_permissions: UserPermissionsProxy,
    thread: Thread,
    request: HttpRequest | None = None,
) -> list[type[PostsModerationAction]]:
    if not user_permissions.is_category_moderator(thread.category_id):
        return []

    return [
        LockPostsModerationAction,
        UnlockPostsModerationAction,
        SplitPostsModerationAction,
        DeletePostsModerationAction,
    ]


def get_private_thread_posts_moderation_actions(
    user_permissions: UserPermissionsProxy,
    thread: Thread,
    request: HttpRequest | None = None,
) -> list[type[PostsModerationAction]]:
    return get_private_thread_posts_moderation_actions_hook(
        _get_private_thread_posts_moderation_actions_action,
        user_permissions,
        thread,
        request,
    )


def _get_private_thread_posts_moderation_actions_action(
    user_permissions: UserPermissionsProxy,
    thread: Thread,
    request: HttpRequest | None = None,
) -> list[type[PostsModerationAction]]:
    if not user_permissions.is_private_threads_moderator:
        return []

    return [
        LockPostsModerationAction,
        UnlockPostsModerationAction,
        SplitPostsModerationAction,
        DeletePostsModerationAction,
    ]


class LockPostsModerationAction(PostsModerationAction):
    id = "lock"
    button_label = pgettext_lazy("posts moderation button label", "Lock")

    def validate(self):
        for post in self.posts:
            if not post.is_locked:
                return

        raise ValidationError(
            pgettext("posts moderation validation", "Posts are already locked.")
        )

    def execute(self) -> ModerationActionResult:
        valid_posts = [post for post in self.posts if not post.is_locked]

        for post in valid_posts:
            post.is_locked = True
            post.save()

        messages.success(
            self.request,
            pgettext("posts moderation success", "Posts locked"),
        )

        return ModerationActionResult(
            updated_items=[post.id for post in valid_posts],
        )


class UnlockPostsModerationAction(PostsModerationAction):
    id = "unlock"
    button_label = pgettext_lazy("posts moderation button label", "Unlock")

    def validate(self):
        for post in self.posts:
            if post.is_locked:
                return

        raise ValidationError(
            pgettext("posts moderation validation", "Posts are already unlocked.")
        )

    def execute(self) -> ModerationActionResult:
        valid_posts = [post for post in self.posts if post.is_locked]

        for post in valid_posts:
            post.is_locked = False
            post.save()

        messages.success(
            self.request,
            pgettext("posts moderation success", "Posts unlocked"),
        )

        return ModerationActionResult(
            updated_items=[post.id for post in valid_posts],
        )


class SplitPostsModerationAction(FormMixin, PostsModerationAction):
    id = "split"
    full_name = "Split posts into a new thread"
    button_label = "Split"
    form_class = SplitPostsForm
    template_name = "misago/moderation/split_posts.html"

    def validate(self):
        for post in self.posts:
            if post.id == self.thread.first_post:
                raise ValidationError(
                    pgettext(
                        "post moderation validation",
                        "The first post in a thread can't be split.",
                    )
                )

    def form_valid(self, form) -> ModerationActionResult:
        messages.success(
            self.request,
            pgettext("posts moderation success", "Posts were split into a new thread."),
        )

        return ModerationActionResult(
            deleted_items=[post.id for post in self.posts],
        )


class DeletePostsModerationAction(ConfirmMixin, PostsModerationAction):
    id = "delete"
    full_name = "Delete posts"
    button_label = "Delete"
    confirmation_message = pgettext_lazy(
        "posts moderation",
        "Are you sure you want to delete the selected posts? This action cannot be undone.",
    )

    def validate(self):
        for post in self.posts:
            if post.id == self.thread.first_post:
                raise ValidationError(
                    pgettext(
                        "post moderation validation",
                        "The first post in a thread can't be deleted.",
                    )
                )

    def confirmed(self) -> ModerationActionResult:
        for post in self.posts:
            delete_post(post)

        synchronize_thread(self.thread)
        synchronize_categories.delay([post.category_id])

        messages.success(
            self.request,
            pgettext("posts moderation success", "Posts deleted"),
        )

        return ModerationActionResult(
            deleted_items=[post.id for post in self.posts],
        )
