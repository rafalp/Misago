from django.contrib import messages
from django.core.exceptions import ValidationError
from django.forms import Form
from django.http import HttpRequest
from django.utils.translation import pgettext, pgettext_lazy

from ..attachments.models import Attachment
from ..categories.tasks import synchronize_categories
from ..notifications.tasks import notify_on_new_thread_reply
from ..permissions.proxy import UserPermissionsProxy
from ..postedits.create import create_post_edit
from ..threads.approve import approve_post
from ..threads.create import create_thread
from ..threads.delete import delete_post
from ..threads.hide import hide_post, unhide_post
from ..threads.lock import lock_post, unlock_post
from ..threads.merge import get_post_merge_conflicts, merge_posts
from ..threads.models import Post, Thread
from ..threads.move import move_post
from ..threads.synchronize import synchronize_thread
from ..threadupdates.create import (
    create_deleted_posts_thread_update,
    create_moved_posts_from_thread_update,
    create_moved_posts_to_thread_update,
    create_split_posts_from_thread_update,
    create_split_posts_into_thread_update,
)
from .actions import (
    ConfirmMixin,
    FormMixin,
    ModerationActionTemplateResult,
    ModerationResult,
    PostModerationAction,
)
from .forms import (
    HideForm,
    MergePostConflictsForm,
    MergePrivateThreadPostForm,
    MergeThreadPostForm,
    MovePostsForm,
    SplitPostsForm,
)
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
            MovePostModerationAction,
        ]

    actions.append(MergeThreadPostModerationAction)

    if post.id != post.thread.first_post_id:
        actions.append(DeletePostModerationAction)

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

    actions.append(MergePrivateThreadPostModerationAction)

    if post.id != post.thread.first_post_id:
        actions.append(DeletePostModerationAction)

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

    form_class = SplitPostsForm
    template_name = "misago/moderation/split_posts.html"

    def get_form(self, form_submitted: bool) -> Form:
        kwargs = {
            "prefix": self.form_prefix,
            "request": self.request,
            "initial": {
                "category": self.thread.category_id,
            },
        }

        if form_submitted:
            return self.form_class(self.request.POST, **kwargs)

        return self.form_class(**kwargs)

    def validate(self):
        if self.post.id == self.thread.first_post_id:
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

        thread_update = create_split_posts_from_thread_update(
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
            thread_updates=[thread_update],
        )

    def get_thread_url(self, thread: Thread) -> str:
        from ..threads.views.backend import thread_backend

        return thread_backend.get_thread_url(thread)


class MovePostModerationAction(FormMixin, PostModerationAction):
    swap_root = True

    id = "move"
    full_name = "Move post to another thread"
    button_label = "Move"

    form_class = MovePostsForm
    template_name = "misago/moderation/move_posts.html"

    def get_form(self, form_submitted: bool) -> Form:
        kwargs = {
            "prefix": self.form_prefix,
            "request": self.request,
            "current_thread": self.thread,
        }

        if form_submitted:
            return self.form_class(self.request.POST, **kwargs)

        return self.form_class(**kwargs)

    def validate(self):
        if self.post.id == self.thread.first_post_id:
            raise ValidationError(
                pgettext(
                    "post moderation validation",
                    "The first post in a thread can't be split.",
                )
            )

    def form_valid(self, form) -> ModerationResult:
        request = self.request
        thread = self.thread
        target_thread = form.cleaned_data["target_thread"]
        post = self.post

        move_post(post, target_thread)

        thread_update = create_moved_posts_from_thread_update(
            target_thread, thread, 1, request.user, request=request
        )
        create_moved_posts_to_thread_update(
            thread, target_thread, 1, request.user, request=request
        )

        synchronize_thread(thread, request=request)
        synchronize_thread(target_thread, request=request)

        sync_categories_ids = list({thread.category_id, target_thread.category_id})
        synchronize_categories.delay(sync_categories_ids)

        messages.success(
            self.request,
            pgettext("post moderation success", "Post was split into a new thread."),
        )

        if form.cleaned_data["redirect_to"] == "target":
            return ModerationResult(redirect_to=self.get_thread_url(target_thread))

        return ModerationResult(
            deleted_items=[post.id],
            thread_updates=[thread_update],
        )

    def get_thread_url(self, thread: Thread) -> str:
        from ..threads.views.backend import thread_backend

        return thread_backend.get_thread_url(thread)


class MergeThreadPostModerationAction(FormMixin, PostModerationAction):
    swap_root = True

    id = "merge"
    full_name = pgettext_lazy("post moderation action name", "Merge post")
    button_label = pgettext_lazy("post moderation button label", "Merge")

    form_class = MergeThreadPostForm
    template_name = "misago/moderation/merge_post.html"

    conflicts_form_class = MergePostConflictsForm
    conflicts_template_name = "misago/moderation/merge_post_conflicts.html"

    def get_form(self, form_submitted: bool):
        kwargs = {
            "request": self.request,
            "prefix": self.form_prefix,
            "post": self.post,
        }

        if form_submitted:
            return self.form_class(self.request.POST, **kwargs)

        return self.form_class(**kwargs)

    def form_valid(self, form) -> ModerationResult:
        request = self.request
        thread = self.thread
        post = self.post
        other_post = form.cleaned_data["other_post"]
        edit_reason = form.cleaned_data["edit_reason"]

        conflicts = get_post_merge_conflicts([post, other_post], request)
        conflicts_resolutions = {}

        handle_conflicts = any([len(conflict) > 1 for conflict in conflicts.values()])
        if handle_conflicts:
            form_kwargs = {
                "request": request,
                "prefix": self.form_prefix,
                "conflicts": conflicts,
            }

            if request.POST.get("confirm_conflicts"):
                conflicts_form = self.conflicts_form_class(request.POST, **form_kwargs)

                if conflicts_form.is_valid():
                    conflicts_resolutions = conflicts_form.get_conflicts_resolutions()
                else:
                    return self.get_conflicts_form_result(form, conflicts_form)

            else:
                conflicts_form = self.conflicts_form_class(**form_kwargs)
                return self.get_conflicts_form_result(form, conflicts_form)

        else:
            conflicts_resolutions = {
                conflict: choices[0] for conflict, choices in conflicts.items()
            }

        attachments = list(
            Attachment.objects.filter(post__in=[post, other_post]).order_by("-id")
        )

        if form.cleaned_data["direction"] == "other":
            final_post, other_post = other_post, post
            old_content = final_post.original
            merge_posts(
                final_post,
                [other_post],
                conflicts_resolutions,
                request.user,
                edit_reason,
                request=request,
            )
        else:
            final_post = post
            old_content = final_post.original
            merge_posts(
                final_post,
                [other_post],
                conflicts_resolutions,
                request.user,
                edit_reason,
                request=request,
            )

        synchronize_thread(thread, request=request)

        for attachment in attachments:
            # A bit of black magic: by unsetting attachment post relations
            # we make 'create_post_edit' record attachment as new addition to a post
            if attachment.post_id != final_post.id:
                attachment.category = None
                attachment.thread = None
                attachment.post = None

        create_post_edit(
            post=final_post,
            user=request.user,
            edit_reason=edit_reason,
            old_content=old_content,
            new_content=final_post.original,
            attachments=attachments,
            edited_at=final_post.updated_at,
            request=request,
        )

        synchronize_categories.delay([final_post.category_id])

        messages.success(
            self.request,
            pgettext("post moderation success", "Posts merged"),
        )

        return self.get_result(final_post, other_post)

    def get_conflicts_form_result(self, merge_form: Form, conflicts_form: Form):
        return ModerationActionTemplateResult(
            context={
                "template_name": self.conflicts_template_name,
                "merge_form": merge_form,
                "conflicts_form": conflicts_form,
            },
        )

    def get_result(self, post: Post, other_post: Post) -> ModerationResult:
        redirect_to = self.get_redirect_url(post)

        if not self.request.is_htmx:
            return ModerationResult(redirect_to=redirect_to)

        refresh = self.request.path == redirect_to[: redirect_to.rindex("/") + 1]

        return ModerationResult(
            refresh=refresh,
            redirect_to=redirect_to if not refresh else None,
            updated_items=[post.id],
            deleted_items=[other_post.id],
        )

    def get_redirect_url(self, post: Post) -> str:
        from ..threads.views.backend import thread_backend

        redirect = thread_backend.get_post_redirect(self.request, post)
        return redirect["location"]


class MergePrivateThreadPostModerationAction(MergeThreadPostModerationAction):
    form_class = MergePrivateThreadPostForm

    def get_redirect_url(self, post: Post) -> str:
        from ..privatethreads.views.backend import private_thread_backend

        redirect = private_thread_backend.get_post_redirect(self.request, post)
        return redirect["location"]


class DeletePostModerationAction(ConfirmMixin, PostModerationAction):
    swap_root = True

    id = "delete"
    full_name = "Delete post"
    button_label = "Delete"
    confirmation_message = pgettext_lazy(
        "post moderation",
        "Are you sure you want to delete this post? This action cannot be undone.",
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
        request = self.request
        thread = self.thread
        post = self.post

        delete_post(post)

        thread_update = create_deleted_posts_thread_update(
            thread, 1, request.user, request=request
        )

        synchronize_thread(thread)
        synchronize_categories.delay([post.category_id])

        messages.success(
            request,
            pgettext("post moderation success", "Post deleted"),
        )

        return ModerationResult(
            deleted_items=[post.id],
            thread_updates=[thread_update],
        )
