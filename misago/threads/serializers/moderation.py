from rest_framework import serializers

from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404
from django.utils.translation import ugettext as _, ugettext_lazy, ungettext

from misago.acl import add_acl
from misago.conf import settings
from misago.threads.models import Thread
from misago.threads.permissions import (
    allow_merge_post, allow_move_post, allow_split_post,
    can_start_thread, exclude_invisible_posts)
from misago.threads.utils import get_thread_id_from_url
from misago.threads.validators import validate_category, validate_title


POSTS_LIMIT = settings.MISAGO_POSTS_PER_PAGE + settings.MISAGO_POSTS_TAIL


__all__ = [
    'MergePostsSerializer',
    'MovePostsSerializer',
    'NewThreadSerializer',
    'SplitPostsSerializer',
]


class MergePostsSerializer(serializers.Serializer):
    error_empty_or_required = ugettext_lazy("You have to select at least two posts to merge.")

    posts = serializers.ListField(
        child=serializers.IntegerField(
            error_messages={
                'invalid': ugettext_lazy("One or more post ids received were invalid."),
            },
        ),
        error_messages={
            'required': error_empty_or_required,
        },
    )

    def validate_posts(self, data):
        data = list(set(data))

        if len(data) < 2:
            raise serializers.ValidationError(self.error_empty_or_required)
        if len(data) > POSTS_LIMIT:
            message = ungettext(
                "No more than %(limit)s post can be merged at single time.",
                "No more than %(limit)s posts can be merged at single time.",
                POSTS_LIMIT,
            )
            raise serializers.ValidationError(message % {'limit': POSTS_LIMIT})

        user = self.context['user']
        thread = self.context['thread']

        posts_queryset = exclude_invisible_posts(user, thread.category, thread.post_set)
        posts_queryset = posts_queryset.filter(id__in=data).order_by('id')

        posts = []
        for post in posts_queryset:
            post.category = thread.category
            post.thread = thread

            try:
                allow_merge_post(user, post)
            except PermissionDenied as e:
                raise serializers.ValidationError(e)

            if not posts:
                posts.append(post)
            else:
                authorship_error = _("Posts made by different users can't be merged.")
                if posts[0].poster_id:
                    if post.poster_id != posts[0].poster_id:
                        raise serializers.ValidationError(authorship_error)
                else:
                    if post.poster_id or post.poster_name != posts[0].poster_name:
                        raise serializers.ValidationError(authorship_error)

                if posts[0].pk != thread.first_post_id:
                    if (posts[0].is_hidden != post.is_hidden or
                            posts[0].is_unapproved != post.is_unapproved):
                        raise serializers.ValidationError(
                            _("Posts with different visibility can't be merged.")
                        )

                posts.append(post)

        if len(posts) != len(data):
            raise serializers.ValidationError(_("One or more posts to merge could not be found."))

        self.posts_cache = posts

        return data


class MovePostsSerializer(serializers.Serializer):
    error_empty_or_required = ugettext_lazy("You have to specify at least one post to move.")

    thread_url = serializers.CharField(
        error_messages={
            'required': ugettext_lazy("Enter link to new thread."),
        },
    )
    posts = serializers.ListField(
        allow_empty=False,
        child=serializers.IntegerField(
            error_messages={
                'invalid': ugettext_lazy("One or more post ids received were invalid."),
            },
        ),
        error_messages={
            'required': error_empty_or_required,
            'empty': error_empty_or_required,
        },
    )

    def validate_thread_url(self, data):
        request = self.context['request']
        thread = self.context['thread']
        viewmodel = self.context['viewmodel']

        new_thread_id = get_thread_id_from_url(request, data)
        if not new_thread_id:
            raise serializers.ValidationError(_("This is not a valid thread link."))
        if new_thread_id == thread.pk:
            raise serializers.ValidationError(_("Thread to move posts to is same as current one."))

        try:
            new_thread = viewmodel(request, new_thread_id).unwrap()
        except Http404:
            raise serializers.ValidationError(
                _(
                    "The thread you have entered link to doesn't "
                    "exist or you don't have permission to see it."
                )
            )

        if not new_thread.acl['can_reply']:
            raise serializers.ValidationError(_("You can't move posts to threads you can't reply."))

        self.new_thread = new_thread

        return data

    def validate_posts(self, data):
        data = list(set(data))
        if len(data) > POSTS_LIMIT:
            message = ungettext(
                "No more than %(limit)s post can be moved at single time.",
                "No more than %(limit)s posts can be moved at single time.",
                POSTS_LIMIT,
            )
            raise serializers.ValidationError(message % {'limit': POSTS_LIMIT})

        request = self.context['request']
        thread = self.context['thread']

        posts_queryset = exclude_invisible_posts(request.user, thread.category, thread.post_set)
        posts_queryset = posts_queryset.filter(id__in=data).order_by('id')

        posts = []
        for post in posts_queryset:
            post.category = thread.category
            post.thread = thread

            try:
                allow_move_post(request.user, post)
                posts.append(post)
            except PermissionDenied as e:
                raise serializers.ValidationError(e)

        if len(posts) != len(data):
            raise serializers.ValidationError(_("One or more posts to move could not be found."))

        self.posts_cache = posts

        return data


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
        return validate_title(title)

    def validate_category(self, category_id):
        self.category = validate_category(self.context['user'], category_id)
        if not can_start_thread(self.context['user'], self.category):
            raise ValidationError(_("You can't create new threads in selected category."))
        return self.category

    def validate_weight(self, weight):
        try:
            add_acl(self.context['user'], self.category)
        except AttributeError:
            return weight  # don't validate weight further if category failed

        if weight > self.category.acl.get('can_pin_threads', 0):
            if weight == 2:
                raise ValidationError(
                    _("You don't have permission to pin threads globally in this category.")
                )
            else:
                raise ValidationError(
                    _("You don't have permission to pin threads in this category.")
                )
        return weight

    def validate_is_hidden(self, is_hidden):
        try:
            add_acl(self.context['user'], self.category)
        except AttributeError:
            return is_hidden  # don't validate hidden further if category failed

        if is_hidden and not self.category.acl.get('can_hide_threads'):
            raise ValidationError(_("You don't have permission to hide threads in this category."))
        return is_hidden

    def validate_is_closed(self, is_closed):
        try:
            add_acl(self.context['user'], self.category)
        except AttributeError:
            return is_closed  # don't validate closed further if category failed

        if is_closed and not self.category.acl.get('can_close_threads'):
            raise ValidationError(
                _("You don't have permission to close threads in this category.")
            )
        return is_closed


class SplitPostsSerializer(NewThreadSerializer):
    error_empty_or_required = ugettext_lazy("You have to specify at least one post to split.")

    posts = serializers.ListField(
        allow_empty=False,
        child=serializers.IntegerField(
            error_messages={
                'invalid': ugettext_lazy("One or more post ids received were invalid."),
            },
        ),
        error_messages={
            'required': error_empty_or_required,
            'empty': error_empty_or_required,
        },
    )

    def validate_posts(self, data):
        if len(data) > POSTS_LIMIT:
            message = ungettext(
                "No more than %(limit)s post can be split at single time.",
                "No more than %(limit)s posts can be split at single time.",
                POSTS_LIMIT,
            )
            raise ValidationError(message % {'limit': POSTS_LIMIT})

        thread = self.context['thread']
        user = self.context['user']

        posts_queryset = exclude_invisible_posts(user, thread.category, thread.post_set)
        posts_queryset = posts_queryset.filter(id__in=data).order_by('id')

        posts = []
        for post in posts_queryset:
            post.category = thread.category
            post.thread = thread

            try:
                allow_split_post(user, post)
            except PermissionDenied as e:
                raise ValidationError(e)

            posts.append(post)

        if len(posts) != len(data):
            raise ValidationError(_("One or more posts to split could not be found."))

        self.posts_cache = posts

        return data
