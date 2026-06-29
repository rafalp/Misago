from django.contrib import messages
from django.core.exceptions import ValidationError
from django.forms import Form
from django.http import HttpRequest
from django.utils.translation import pgettext, pgettext_lazy

from ..categories.tasks import synchronize_categories
from ..notifications.tasks import notify_on_new_thread_reply
from ..permissions.proxy import UserPermissionsProxy
from ..threads.approve import approve_post
from ..threads.create import create_thread
from ..threads.delete import delete_post
from ..threads.hide import hide_post, unhide_post
from ..threads.lock import lock_post, unlock_post
from ..threads.models import Thread
from ..threads.move import move_post
from ..threads.synchronize import synchronize_thread
from .actions import (
    ConfirmMixin,
    FormMixin,
    ModerationResult,
    PostsModerationAction,
)
from .forms import HideForm, SelectThreadForm, SplitThreadForm
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
        HidePostsModerationAction,
        UnhidePostsModerationAction,
        ApprovePostsModerationAction,
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
        HidePostsModerationAction,
        UnhidePostsModerationAction,
        ApprovePostsModerationAction,
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

    def execute(self) -> ModerationResult:
        request = self.request
        valid_posts = [post for post in self.posts if not post.is_locked]

        for post in valid_posts:
            lock_post(post, request=request)

        messages.success(
            self.request,
            pgettext("posts moderation success", "Posts locked"),
        )

        return ModerationResult(
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

    def execute(self) -> ModerationResult:
        request = self.request
        valid_posts = [post for post in self.posts if post.is_locked]

        for post in valid_posts:
            unlock_post(post, request=request)

        messages.success(
            self.request,
            pgettext("posts moderation success", "Posts unlocked"),
        )

        return ModerationResult(
            updated_items=[post.id for post in valid_posts],
        )


class HidePostsModerationAction(FormMixin, PostsModerationAction):
    id = "hide"
    full_name = pgettext_lazy("posts moderation action name", "Hide posts")
    button_label = pgettext_lazy("posts moderation button label", "Hide")

    form_class = HideForm
    template_name = "misago/moderation/hide.html"

    def validate(self):
        for post in self.posts:
            if post.id == self.thread.first_post_id:
                raise ValidationError(
                    pgettext(
                        "posts moderation validation",
                        "Thread's original post can't be hidden.",
                    )
                )

        for post in self.posts:
            if not post.is_hidden:
                return

        raise ValidationError(
            pgettext("posts moderation validation", "Posts are already hidden.")
        )

    def form_valid(self, form) -> ModerationResult:
        request = self.request
        valid_posts = [post for post in self.posts if not post.is_hidden]
        hidden_reason = form.cleaned_data["hidden_reason"]

        for post in valid_posts:
            hide_post(post, request.user, hidden_reason, request=request)

        messages.success(
            self.request,
            pgettext("posts moderation success", "Posts hidden"),
        )

        return ModerationResult(
            updated_items=[post.id for post in valid_posts],
        )


class UnhidePostsModerationAction(PostsModerationAction):
    id = "unhide"
    button_label = pgettext_lazy("posts moderation button label", "Unhide")

    def validate(self):
        for post in self.posts:
            if post.is_hidden:
                return

        raise ValidationError(
            pgettext("posts moderation validation", "Posts are already unhidden.")
        )

    def execute(self) -> ModerationResult:
        request = self.request
        valid_posts = [post for post in self.posts if post.is_hidden]

        for post in valid_posts:
            unhide_post(post, request=request)

        messages.success(
            self.request,
            pgettext("posts moderation success", "Posts unhidden"),
        )

        return ModerationResult(
            updated_items=[post.id for post in valid_posts],
        )


class ApprovePostsModerationAction(PostsModerationAction):
    id = "approve"
    button_label = pgettext_lazy("posts moderation button label", "Approve")

    def validate(self):
        for post in self.posts:
            if post.is_unapproved:
                return

        raise ValidationError(
            pgettext("posts moderation validation", "Posts are already approved.")
        )

    def execute(self) -> ModerationResult:
        request = self.request
        thread = self.thread
        valid_posts = [post for post in self.posts if post.is_unapproved]

        for post in valid_posts:
            approve_post(post, request=request)

        synchronize_thread(thread, request=request)

        for post in valid_posts:
            notify_on_new_thread_reply.delay(post.id)

        synchronize_categories.delay([thread.category_id])

        messages.success(
            self.request,
            pgettext("posts moderation success", "Posts approved"),
        )

        return ModerationResult(
            updated_items=[post.id for post in valid_posts],
        )


class SplitPostsModerationAction(FormMixin, PostsModerationAction):
    id = "split"
    full_name = "Split posts into a new thread"
    button_label = "Split"

    form_class = SplitThreadForm
    template_name = "misago/moderation/split_thread.html"

    def validate(self):
        for post in self.posts:
            if post.id == self.thread.first_post:
                raise ValidationError(
                    pgettext(
                        "post moderation validation",
                        "The first post in a thread can't be split.",
                    )
                )

    def form_valid(self, form) -> ModerationResult:
        request = self.request
        thread = self.thread
        posts = self.posts

        new_thread = create_thread(
            form.cleaned_data["category"],
            form.cleaned_data["title"],
            pinned=form.cleaned_data["pin"],
            is_locked=form.cleaned_data["is_locked"],
            is_hidden=form.cleaned_data["is_hidden"],
            request=request,
        )

        for post in posts:
            move_post(post, new_thread)

        synchronize_thread(thread, request=request)
        synchronize_thread(new_thread, request=request)

        sync_categories_ids = list({thread.category_id, new_thread.category_id})
        synchronize_categories.delay(sync_categories_ids)

        messages.success(
            self.request,
            pgettext("posts moderation success", "Posts were split into a new thread."),
        )

        if form.cleaned_data["redirect_to"] == "new":
            return ModerationResult(redirect_to=self.get_thread_url(new_thread))

        return ModerationResult(
            deleted_items=[post.id for post in posts],
        )

    def get_thread_url(self, thread: Thread) -> str:
        from ..threads.views.backend import thread_backend

        return thread_backend.get_thread_url(thread)


class MovePostsModerationAction(FormMixin, PostsModerationAction):
    id = "move"
    full_name = "Move posts to another thread"
    button_label = "Move"

    form_class = SelectThreadForm
    template_name = "misago/moderation/select_thread.html"

    def validate(self):
        for post in self.posts:
            if post.id == self.thread.first_post:
                raise ValidationError(
                    pgettext(
                        "post moderation validation",
                        "The first post in a thread can't be moved.",
                    )
                )

    def form_valid(self, form) -> ModerationResult:
        request = self.request
        thread = self.thread
        posts = self.posts

        new_thread = form.cleaned_data["other_thread"]

        for post in posts:
            move_post(post, new_thread)

        synchronize_thread(thread, request=request)
        synchronize_thread(new_thread, request=request)

        sync_categories_ids = list({thread.category_id, new_thread.category_id})
        synchronize_categories.delay(sync_categories_ids)

        return ModerationResult(
            deleted_items=[post.id for post in posts],
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
            if post.id == self.thread.first_post_id:
                raise ValidationError(
                    pgettext(
                        "post moderation validation",
                        "The first post in a thread can't be deleted.",
                    )
                )

    def confirmed(self) -> ModerationResult:
        for post in self.posts:
            delete_post(post)

        synchronize_thread(self.thread)
        synchronize_categories.delay([self.thread.category_id])

        messages.success(
            self.request,
            pgettext("posts moderation success", "Posts deleted"),
        )

        return ModerationResult(
            deleted_items=[post.id for post in self.posts],
        )
