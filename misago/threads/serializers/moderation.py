from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy, ngettext
from rest_framework import serializers

from ...acl.objectacl import add_acl_to_obj
from ...categories import THREADS_ROOT_NAME
from ...conf import settings
from ..mergeconflict import MergeConflict
from ..models import Thread
from ..permissions import (
    allow_delete_best_answer,
    allow_delete_event,
    allow_delete_post,
    allow_delete_thread,
    allow_merge_post,
    allow_merge_thread,
    allow_move_post,
    allow_split_post,
    can_reply_thread,
    can_see_thread,
    can_start_thread,
    exclude_invisible_posts,
)
from ..threadtypes import trees_map
from ..utils import get_thread_id_from_url
from ..validators import validate_category, validate_thread_title


__all__ = [
    "DeletePostsSerializer",
    "DeleteThreadsSerializer",
    "MergePostsSerializer",
    "MergeThreadSerializer",
    "MergeThreadsSerializer",
    "MovePostsSerializer",
    "NewThreadSerializer",
    "SplitPostsSerializer",
]


def get_posts_limit(settings):
    return settings.posts_per_page + settings.posts_per_page_orphans


class DeletePostsSerializer(serializers.Serializer):
    error_empty_or_required = gettext_lazy(
        "You have to specify at least one post to delete."
    )

    posts = serializers.ListField(
        allow_empty=False,
        child=serializers.IntegerField(
            error_messages={
                "invalid": gettext_lazy("One or more post ids received were invalid.")
            }
        ),
        error_messages={
            "required": error_empty_or_required,
            "null": error_empty_or_required,
            "empty": error_empty_or_required,
        },
    )

    def validate_posts(self, data):
        limit = get_posts_limit(self.context["settings"])
        if len(data) > limit:
            message = ngettext(
                "No more than %(limit)s post can be deleted at a single time.",
                "No more than %(limit)s posts can be deleted at a single time.",
                limit,
            )
            raise ValidationError(message % {"limit": limit})

        user_acl = self.context["user_acl"]
        thread = self.context["thread"]

        posts_queryset = exclude_invisible_posts(
            user_acl, thread.category, thread.post_set
        )
        posts_queryset = posts_queryset.filter(id__in=data).order_by("id")

        posts = []
        for post in posts_queryset:
            post.category = thread.category
            post.thread = thread

            if post.is_event:
                allow_delete_event(user_acl, post)
            else:
                allow_delete_best_answer(user_acl, post)
                allow_delete_post(user_acl, post)

            posts.append(post)

        if len(posts) != len(data):
            raise PermissionDenied(_("One or more posts to delete could not be found."))

        return posts


class MergePostsSerializer(serializers.Serializer):
    error_empty_or_required = gettext_lazy(
        "You have to select at least two posts to merge."
    )

    posts = serializers.ListField(
        child=serializers.IntegerField(
            error_messages={
                "invalid": gettext_lazy("One or more post ids received were invalid.")
            }
        ),
        error_messages={
            "null": error_empty_or_required,
            "required": error_empty_or_required,
        },
    )

    def validate_posts(self, data):
        limit = get_posts_limit(self.context["settings"])
        data = list(set(data))

        if len(data) < 2:
            raise serializers.ValidationError(self.error_empty_or_required)
        if len(data) > limit:
            message = ngettext(
                "No more than %(limit)s post can be merged at a single time.",
                "No more than %(limit)s posts can be merged at a single time.",
                limit,
            )
            raise serializers.ValidationError(message % {"limit": limit})

        user_acl = self.context["user_acl"]
        thread = self.context["thread"]

        posts_queryset = exclude_invisible_posts(
            user_acl, thread.category, thread.post_set
        )
        posts_queryset = posts_queryset.filter(id__in=data).order_by("id")

        posts = []
        for post in posts_queryset:
            post.category = thread.category
            post.thread = thread

            try:
                allow_merge_post(user_acl, post)
            except PermissionDenied as e:
                raise serializers.ValidationError(e)

            if not posts:
                posts.append(post)
                continue

            authorship_error = _("Posts made by different users can't be merged.")
            if post.poster_id != posts[0].poster_id:
                raise serializers.ValidationError(authorship_error)
            elif (
                post.poster_id is None
                and posts[0].poster_id is None
                and post.poster_name != posts[0].poster_name
            ):
                raise serializers.ValidationError(authorship_error)

            if posts[0].is_first_post and post.is_best_answer:
                raise serializers.ValidationError(
                    _(
                        "Post marked as best answer can't be merged with "
                        "thread's first post."
                    )
                )

            if not posts[0].is_first_post:
                if (
                    posts[0].is_hidden != post.is_hidden
                    or posts[0].is_unapproved != post.is_unapproved
                ):
                    raise serializers.ValidationError(
                        _("Posts with different visibility can't be merged.")
                    )

            posts.append(post)

        if len(posts) != len(data):
            raise serializers.ValidationError(
                _("One or more posts to merge could not be found.")
            )

        return posts


class MovePostsSerializer(serializers.Serializer):
    error_empty_or_required = gettext_lazy(
        "You have to specify at least one post to move."
    )

    new_thread = serializers.CharField(
        error_messages={"required": gettext_lazy("Enter link to new thread.")}
    )
    posts = serializers.ListField(
        allow_empty=False,
        child=serializers.IntegerField(
            error_messages={
                "invalid": gettext_lazy("One or more post ids received were invalid.")
            }
        ),
        error_messages={
            "empty": error_empty_or_required,
            "null": error_empty_or_required,
            "required": error_empty_or_required,
        },
    )

    def validate_new_thread(self, data):
        request = self.context["request"]
        thread = self.context["thread"]
        viewmodel = self.context["viewmodel"]

        new_thread_id = get_thread_id_from_url(request, data)
        if not new_thread_id:
            raise serializers.ValidationError(_("This is not a valid thread link."))
        if new_thread_id == thread.pk:
            raise serializers.ValidationError(
                _("Thread to move posts to is same as current one.")
            )

        try:
            new_thread = viewmodel(request, new_thread_id).unwrap()
        except Http404:
            raise serializers.ValidationError(
                _(
                    "The thread you have entered link to doesn't "
                    "exist or you don't have permission to see it."
                )
            )

        if not new_thread.acl["can_reply"]:
            raise serializers.ValidationError(
                _("You can't move posts to threads you can't reply.")
            )

        return new_thread

    def validate_posts(self, data):
        limit = get_posts_limit(self.context["settings"])
        data = list(set(data))
        if len(data) > limit:
            message = ngettext(
                "No more than %(limit)s post can be moved at a single time.",
                "No more than %(limit)s posts can be moved at a single time.",
                limit,
            )
            raise serializers.ValidationError(message % {"limit": limit})

        request = self.context["request"]
        thread = self.context["thread"]

        posts_queryset = exclude_invisible_posts(
            request.user_acl, thread.category, thread.post_set
        )
        posts_queryset = posts_queryset.filter(id__in=data).order_by("id")

        posts = []
        for post in posts_queryset:
            post.category = thread.category
            post.thread = thread

            try:
                allow_move_post(request.user_acl, post)
                posts.append(post)
            except PermissionDenied as e:
                raise serializers.ValidationError(e)

        if len(posts) != len(data):
            raise serializers.ValidationError(
                _("One or more posts to move could not be found.")
            )

        return posts


class NewThreadSerializer(serializers.Serializer):
    title = serializers.CharField()
    category = serializers.IntegerField()
    weight = serializers.IntegerField(
        required=False,
        allow_null=True,
        max_value=Thread.WEIGHT_GLOBAL,
        min_value=Thread.WEIGHT_DEFAULT,
    )
    is_hidden = serializers.NullBooleanField(required=False)
    is_closed = serializers.NullBooleanField(required=False)

    def validate_title(self, title):
        settings = self.context["settings"]
        validate_thread_title(settings, title)
        return title

    def validate_category(self, category_id):
        user_acl = self.context["user_acl"]
        self.category = validate_category(user_acl, category_id)
        if not can_start_thread(user_acl, self.category):
            raise ValidationError(
                _("You can't create new threads in selected category.")
            )
        return self.category

    def validate_weight(self, weight):
        try:
            add_acl_to_obj(self.context["user_acl"], self.category)
        except AttributeError:
            return weight  # don't validate weight further if category failed

        if weight > self.category.acl.get("can_pin_threads", 0):
            if weight == 2:
                raise ValidationError(
                    _(
                        "You don't have permission to pin threads globally "
                        "in this category."
                    )
                )
            else:
                raise ValidationError(
                    _("You don't have permission to pin threads in this category.")
                )
        return weight

    def validate_is_hidden(self, is_hidden):
        try:
            add_acl_to_obj(self.context["user_acl"], self.category)
        except AttributeError:
            return is_hidden  # don't validate hidden further if category failed

        if is_hidden and not self.category.acl.get("can_hide_threads"):
            raise ValidationError(
                _("You don't have permission to hide threads in this category.")
            )
        return is_hidden

    def validate_is_closed(self, is_closed):
        try:
            add_acl_to_obj(self.context["user_acl"], self.category)
        except AttributeError:
            return is_closed  # don't validate closed further if category failed

        if is_closed and not self.category.acl.get("can_close_threads"):
            raise ValidationError(
                _("You don't have permission to close threads in this category.")
            )
        return is_closed


class SplitPostsSerializer(NewThreadSerializer):
    error_empty_or_required = gettext_lazy(
        "You have to specify at least one post to split."
    )

    posts = serializers.ListField(
        allow_empty=False,
        child=serializers.IntegerField(
            error_messages={
                "invalid": gettext_lazy("One or more post ids received were invalid.")
            }
        ),
        error_messages={
            "empty": error_empty_or_required,
            "null": error_empty_or_required,
            "required": error_empty_or_required,
        },
    )

    def validate_posts(self, data):
        limit = get_posts_limit(self.context["settings"])
        if len(data) > limit:
            message = ngettext(
                "No more than %(limit)s post can be split at a single time.",
                "No more than %(limit)s posts can be split at a single time.",
                limit,
            )
            raise ValidationError(message % {"limit": limit})

        thread = self.context["thread"]
        user_acl = self.context["user_acl"]

        posts_queryset = exclude_invisible_posts(
            user_acl, thread.category, thread.post_set
        )
        posts_queryset = posts_queryset.filter(id__in=data).order_by("id")

        posts = []
        for post in posts_queryset:
            post.category = thread.category
            post.thread = thread

            try:
                allow_split_post(user_acl, post)
            except PermissionDenied as e:
                raise ValidationError(str(e))

            posts.append(post)

        if len(posts) != len(data):
            raise ValidationError(_("One or more posts to split could not be found."))

        return posts


class DeleteThreadsSerializer(serializers.Serializer):
    error_empty_or_required = gettext_lazy(
        "You have to specify at least one thread to delete."
    )

    threads = serializers.ListField(
        allow_empty=False,
        child=serializers.IntegerField(
            error_messages={
                "invalid": gettext_lazy("One or more thread ids received were invalid.")
            }
        ),
        error_messages={
            "required": error_empty_or_required,
            "null": error_empty_or_required,
            "empty": error_empty_or_required,
        },
    )

    def validate_threads(self, data):
        limit = self.context["settings"].threads_per_page
        if len(data) > limit:
            message = ngettext(
                "No more than %(limit)s thread can be deleted at a single time.",
                "No more than %(limit)s threads can be deleted at a single time.",
                limit,
            )
            raise ValidationError(message % {"limit": limit})

        request = self.context["request"]
        viewmodel = self.context["viewmodel"]

        threads = []
        errors = []

        for thread_id in data:
            try:
                thread = viewmodel(request, thread_id).unwrap()
                allow_delete_thread(request.user_acl, thread)
                threads.append(thread)
            except PermissionDenied as e:
                errors.append(
                    {
                        "thread": {"id": thread.id, "title": thread.title},
                        "error": str(e),
                    }
                )
            except Http404 as e:
                pass  # skip invisible threads

        if errors:
            raise serializers.ValidationError({"details": errors})

        if len(threads) != len(data):
            raise ValidationError(
                _("One or more threads to delete could not be found.")
            )

        return threads


class MergeThreadSerializer(serializers.Serializer):
    other_thread = serializers.CharField(
        error_messages={"required": gettext_lazy("Enter link to new thread.")}
    )
    best_answer = serializers.IntegerField(
        required=False, error_messages={"invalid": gettext_lazy("Invalid choice.")}
    )
    poll = serializers.IntegerField(
        required=False, error_messages={"invalid": gettext_lazy("Invalid choice.")}
    )

    def validate_other_thread(self, data):
        request = self.context["request"]
        thread = self.context["thread"]
        viewmodel = self.context["viewmodel"]

        other_thread_id = get_thread_id_from_url(request, data)
        if not other_thread_id:
            raise ValidationError(_("This is not a valid thread link."))
        if other_thread_id == thread.pk:
            raise ValidationError(_("You can't merge thread with itself."))

        try:
            other_thread = viewmodel(request, other_thread_id).unwrap()
            allow_merge_thread(request.user_acl, other_thread, otherthread=True)
        except PermissionDenied as e:
            raise serializers.ValidationError(e)
        except Http404:
            raise ValidationError(
                _(
                    "The thread you have entered link to doesn't "
                    "exist or you don't have permission to see it."
                )
            )

        if not can_reply_thread(request.user_acl, other_thread):
            raise ValidationError(
                _("You can't merge this thread into thread you can't reply.")
            )

        return other_thread

    def validate(self, data):
        thread = self.context["thread"]
        other_thread = data["other_thread"]

        merge_conflict = MergeConflict(data, [thread, other_thread])
        merge_conflict.is_valid(raise_exception=True)
        data.update(merge_conflict.get_resolution())
        self.merge_conflict = merge_conflict.get_conflicting_fields()

        return data


class MergeThreadsSerializer(NewThreadSerializer):
    error_empty_or_required = gettext_lazy(
        "You have to select at least two threads to merge."
    )

    threads = serializers.ListField(
        allow_empty=False,
        min_length=2,
        child=serializers.IntegerField(
            error_messages={
                "invalid": gettext_lazy("One or more thread ids received were invalid.")
            }
        ),
        error_messages={
            "empty": error_empty_or_required,
            "null": error_empty_or_required,
            "required": error_empty_or_required,
            "min_length": error_empty_or_required,
        },
    )
    best_answer = serializers.IntegerField(
        required=False, error_messages={"invalid": gettext_lazy("Invalid choice.")}
    )
    poll = serializers.IntegerField(
        required=False, error_messages={"invalid": gettext_lazy("Invalid choice.")}
    )

    def validate_threads(self, data):
        limit = self.context["settings"].threads_per_page
        if len(data) > limit:
            message = ngettext(
                "No more than %(limit)s thread can be merged at a single time.",
                "No more than %(limit)s threads can be merged at a single time.",
                limit,
            )
            raise ValidationError(message % {"limit": limit})

        threads_tree_id = trees_map.get_tree_id_for_root(THREADS_ROOT_NAME)

        threads_queryset = (
            Thread.objects.filter(id__in=data, category__tree_id=threads_tree_id)
            .select_related("category")
            .order_by("-id")
        )

        user_acl = self.context["user_acl"]

        threads = []
        for thread in threads_queryset:
            add_acl_to_obj(user_acl, thread)
            if can_see_thread(user_acl, thread):
                threads.append(thread)

        if len(threads) != len(data):
            raise ValidationError(_("One or more threads to merge could not be found."))

        return threads
