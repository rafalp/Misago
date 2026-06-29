from django.contrib import messages
from django.core.exceptions import ValidationError
from django.forms import Form
from django.http import HttpRequest
from django.utils.translation import pgettext, pgettext_lazy

from ..categories.models import Category
from ..categories.tasks import synchronize_categories
from ..notifications.tasks import notify_on_new_thread_reply
from ..permissions.proxy import UserPermissionsProxy
from ..threads.approve import approve_post
from ..threads.create import create_thread
from ..threads.delete import delete_post
from ..threads.hide import hide_post, unhide_post
from ..threads.lock import lock_post, unlock_post
from ..threads.models import Post, Thread
from ..threads.move import move_post
from ..threads.synchronize import synchronize_thread
from ..threadupdates.create import (
    create_split_posts_from_thread_update,
    create_split_posts_into_thread_update,
)
from .actions import (
    ConfirmMixin,
    FormMixin,
    ModerationResult,
    PostModerationAction,
)
from .forms import HideForm, SelectThreadForm, SplitThreadForm
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

    if post.is_unapproved:
        actions.append(ApprovePostModerationAction)

    if post.id != post.thread.first_post_id:
        if post.is_hidden:
            actions.append(UnhidePostModerationAction)
        else:
            actions.append(HidePostModerationAction)

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
        if post.is_hidden:
            actions.append(UnhidePostModerationAction)
        else:
            actions.append(HidePostModerationAction)

    if post.is_unapproved:
        actions.append(ApprovePostModerationAction)

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

    def execute(self) -> ModerationResult:
        post = self.post

        lock_post(post, request=self.request)

        messages.success(
            self.request,
            pgettext("post moderation success", "Post locked"),
        )

        return ModerationResult(
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

    def execute(self) -> ModerationResult:
        post = self.post

        unlock_post(post, request=self.request)

        messages.success(
            self.request,
            pgettext("post moderation success", "Post unlocked"),
        )

        return ModerationResult(
            updated_items=[post.id],
        )


class HidePostModerationAction(FormMixin, PostModerationAction):
    id = "hide"
    full_name = pgettext_lazy("post moderation button label", "Hide post")
    button_label = pgettext_lazy("post moderation button label", "Hide")

    form_class = HideForm
    template_name = "misago/moderation/hide.html"

    def validate(self):
        if self.post.id == self.thread.first_post_id:
            raise ValidationError(
                pgettext(
                    "post moderation validation",
                    "The thread's original post can't be hidden.",
                )
            )

        if self.post.is_hidden:
            raise ValidationError(
                pgettext("post moderation validation", "Post is already hidden.")
            )

    def form_valid(self, form) -> ModerationResult:
        request = self.request
        post = self.post

        hide_post(
            post, request.user, form.cleaned_data["hidden_reason"], request=request
        )

        messages.success(
            self.request,
            pgettext("post moderation success", "Post hidden"),
        )

        return ModerationResult(
            updated_items=[post.id],
        )


class UnhidePostModerationAction(PostModerationAction):
    id = "unhide"
    button_label = pgettext_lazy("post moderation button label", "Unhide")

    def validate(self):
        if not self.post.is_hidden:
            raise ValidationError(
                pgettext("post moderation validation", "Post is already unhidden.")
            )

    def execute(self) -> ModerationResult:
        post = self.post

        unhide_post(post, request=self.request)

        messages.success(
            self.request,
            pgettext("post moderation success", "Post unhidden"),
        )

        return ModerationResult(
            updated_items=[post.id],
        )


class ApprovePostModerationAction(PostModerationAction):
    id = "approve"
    button_label = pgettext_lazy("post moderation button label", "Approve")

    def validate(self):
        if not self.post.is_unapproved:
            raise ValidationError(
                pgettext("post moderation validation", "Post is already approved.")
            )

    def execute(self) -> ModerationResult:
        request = self.request
        thread = self.thread
        post = self.post

        approve_post(post, request=request)

        synchronize_thread(thread, request=request)

        notify_on_new_thread_reply.delay(post.id)
        synchronize_categories.delay([thread.category_id])

        messages.success(
            self.request,
            pgettext("post moderation success", "Post approved"),
        )

        return ModerationResult(
            updated_items=[post.id],
        )


class SplitPostModerationAction(FormMixin, PostModerationAction):
    swap_root = True

    id = "split"
    full_name = "Split post into a new thread"
    button_label = "Split"

    form_class = SplitThreadForm
    template_name = "misago/moderation/split_thread.html"

    def get_form(self, form_submitted: bool) -> Form:
        form_kwargs = {
            "prefix": self.form_prefix,
            "request": self.request,
            "initial": {
                "category": self.thread.category_id,
            },
        }
        if form_submitted:
            return self.form_class(self.request.POST, **form_kwargs)

        return self.form_class(**form_kwargs)

    def validate(self):
        if self.post.id == self.thread.first_post:
            raise ValidationError(
                pgettext(
                    "post moderation validation",
                    "The first post in a thread can't be split.",
                )
            )

    def form_valid(self, form) -> ModerationResult:
        request = self.request
        thread = self.thread
        post = self.post

        new_thread = create_thread(
            form.cleaned_data["category"],
            form.cleaned_data["title"],
            pinned=form.cleaned_data["pin"],
            is_locked=form.cleaned_data["is_locked"],
            is_hidden=form.cleaned_data["is_hidden"],
            request=request,
        )

        move_post(post, new_thread)

        create_split_posts_from_thread_update(
            new_thread, thread, 1, request.user, request=request
        )
        create_split_posts_into_thread_update(
            thread, new_thread, 1, request.user, request=request
        )

        synchronize_thread(thread, request=request)
        synchronize_thread(new_thread, request=request)

        sync_categories_ids = list({thread.category_id, new_thread.category_id})
        synchronize_categories.delay(sync_categories_ids)

        messages.success(
            self.request,
            pgettext("post moderation success", "Post was split into a new thread."),
        )

        if form.cleaned_data["redirect_to"] == "new":
            return ModerationResult(redirect_to=self.get_thread_url(new_thread))

        return ModerationResult(
            deleted_items=[post.id],
        )

    def get_thread_url(self, thread: Thread) -> str:
        from ..threads.views.backend import thread_backend

        return thread_backend.get_thread_url(thread)


class DeletePostModerationAction(ConfirmMixin, PostModerationAction):
    swap_root = True

    id = "delete"
    full_name = "Delete post"
    button_label = "Delete"
    confirmation_message = pgettext_lazy(
        "post moderation",
        "Are you sure you want to delete the selected post? This action cannot be undone.",
    )

    def validate(self):
        if self.post.id == self.thread.first_post_id:
            raise ValidationError(
                pgettext(
                    "post moderation validation",
                    "First post in a thread can't be deleted.",
                )
            )

    def confirmed(self) -> ModerationResult:
        post = self.post

        delete_post(post)
        synchronize_thread(self.thread)
        synchronize_categories.delay([post.category_id])

        messages.success(
            self.request,
            pgettext("post moderation success", "Post deleted"),
        )

        return ModerationResult(
            deleted_items=[post.id],
        )
