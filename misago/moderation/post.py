from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.utils.translation import pgettext, pgettext_lazy

from ..categories.models import Category
from ..categories.tasks import synchronize_categories
from ..permissions.proxy import UserPermissionsProxy
from ..threads.delete import delete_post
from ..threads.hide import hide_post, unhide_post
from ..threads.lock import lock_post, unlock_post
from ..threads.models import Post, Thread
from ..threads.synchronize import synchronize_thread
from .actions import (
    ConfirmMixin,
    FormMixin,
    ModerationResult,
    PostModerationAction,
)
from .forms import HideForm, SplitPostsForm
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


class SplitPostModerationAction(FormMixin, PostModerationAction):
    id = "split"
    full_name = "Split post into a new thread"
    button_label = "Split"
    form_class = SplitPostsForm
    template_name = "misago/moderation/split_post.html"

    def form_valid(self, form) -> ModerationResult:
        post = self.post

        if form.cleaned_data["category"] == self.category.id:
            new_category = self.category
            sync_categories_ids = [new_category.id]
        else:
            new_category = Category.objects.get(id=form.cleaned_data["category"])
            sync_categories_ids = [self.category.id, new_category.id]

        from misago.core.utils import slugify

        if post.poster:
            poster_username = post.post.username
            poster_slug = post.post.slug
        else:
            poster_username = post.poster_name
            poster_slug = slugify(post.poster_name)

        new_thread = Thread.objects.create(
            category=new_category,
            title=form.cleaned_data["title"],
            slug=slugify(form.cleaned_data["title"]),
            started_at=post.posted_at,
            last_posted_at=post.posted_at,
            first_post=post,
            last_post=post,
            starter_name=poster_username,
            starter_slug=poster_slug,
            last_poster_name=poster_username,
            last_poster_slug=poster_slug,
        )

        post.category = new_category
        post.thread = new_thread
        post.save()

        synchronize_thread(new_thread, request=self.request)
        synchronize_categories.delay(sync_categories_ids)

        messages.success(
            self.request,
            pgettext("post moderation success", "Post was split into a new thread."),
        )

        return ModerationResult(
            deleted_items=[post.id],
        )


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
                    "The first post in a thread can't be deleted.",
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
