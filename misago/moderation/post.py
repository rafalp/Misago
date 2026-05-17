from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.utils.translation import pgettext, pgettext_lazy

from ..permissions.proxy import UserPermissionsProxy
from ..threads.models import Post
from .actions import (
    ModerationActionResult,
    PostModerationAction,
    FormMixin,
    ConfirmMixin,
)
from .forms import SplitPostsForm
from .hooks import (
    get_private_thread_post_moderation_actions_hook,
    get_thread_post_moderation_actions_hook,
)


def get_thread_post_moderation_actions(
    user_permissions: UserPermissionsProxy,
    post: Post,
    request: HttpRequest | None = None,
) -> list[type[PostModerationAction]]:
    return get_thread_post_moderation_actions_hook(
        _get_thread_post_moderation_actions_action,
        user_permissions,
        post,
        request,
    )


def _get_thread_post_moderation_actions_action(
    user_permissions: UserPermissionsProxy,
    post: Post,
    request: HttpRequest | None = None,
) -> list[type[PostModerationAction]]:
    if not user_permissions.is_category_moderator(post.category_id):
        return []

    actions = []

    if post.is_locked:
        actions.append(UnlockPostModerationAction)
    else:
        actions.append(LockPostModerationAction)

    if post.id != post.thread.first_post_id:
        actions += [
            SplitPostModerationAction,
            DeletePostModerationAction,
        ]

    return actions


def get_private_thread_post_moderation_actions(
    user_permissions: UserPermissionsProxy,
    post: Post,
    request: HttpRequest | None = None,
) -> list[type[PostModerationAction]]:
    return get_private_thread_post_moderation_actions_hook(
        _get_private_thread_post_moderation_actions_action,
        user_permissions,
        post,
        request,
    )


def _get_private_thread_post_moderation_actions_action(
    user_permissions: UserPermissionsProxy,
    post: Post,
    request: HttpRequest | None = None,
) -> list[type[PostModerationAction]]:
    if not user_permissions.is_private_threads_moderator:
        return []

    actions = []

    if post.is_locked:
        actions.append(UnlockPostModerationAction)
    else:
        actions.append(LockPostModerationAction)

    if post.id != post.thread.first_post_id:
        actions += [
            DeletePostModerationAction,
        ]

    return actions


class LockPostModerationAction(PostModerationAction):
    id = "lock"
    button_label = pgettext_lazy("post moderation button label", "Lock")

    def validate(self):
        if self.post.is_locked:
            raise ValidationError(
                pgettext("post moderation validation", "Post is already locked.")
            )

    def execute(self) -> ModerationActionResult:
        post = self.post

        post.is_locked = True
        post.save()

        messages.success(
            self.request,
            pgettext("post moderation success", "Post locked"),
        )

        return ModerationActionResult(
            updated_items=[post.id],
        )


class UnlockPostModerationAction(PostModerationAction):
    id = "unlock"
    button_label = pgettext_lazy("post moderation button label", "Unlock")

    def validate(self):
        if not self.post.is_locked:
            raise ValidationError(
                pgettext("post moderation validation", "Post is already unlocked.")
            )

    def execute(self) -> ModerationActionResult:
        post = self.post

        post.is_locked = False
        post.save()

        messages.success(
            self.request,
            pgettext("post moderation success", "Post unlocked"),
        )

        return ModerationActionResult(
            updated_items=[post.id],
        )


class SplitPostModerationAction(FormMixin, PostModerationAction):
    id = "split"
    full_name = "Split post into a new thread"
    button_label = "Split"
    form_class = SplitPostsForm
    template_name = "misago/moderation/split_post.html"

    def validate(self):
        if self.post.id == self.thread.first_post_id:
            raise ValidationError(
                pgettext(
                    "post moderation validation",
                    "The first post in a thread can't be moved.",
                )
            )

    def form_valid(self, form) -> ModerationActionResult:
        post = self.post

        messages.success(
            self.request,
            pgettext("post moderation success", "Post was split into a new thread."),
        )

        return ModerationActionResult(
            deleted_items=[post.id],
        )


class DeletePostModerationAction(ConfirmMixin, PostModerationAction):
    id = "delete"
    full_name = "Delete post"
    button_label = "Delete"
    confirmation_message = pgettext_lazy(
        "post moderation",
        "Are you sure you want to delete the selected post? This action cannot be undone.",
    )

    def confirmed(self) -> ModerationActionResult:
        post = self.post

        messages.success(
            self.request,
            pgettext("post moderation success", "Post deleted"),
        )

        return ModerationActionResult(
            deleted_items=[post.id],
        )
