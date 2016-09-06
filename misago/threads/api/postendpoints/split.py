from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _, ungettext

from rest_framework import serializers
from rest_framework.response import Response

from ...models import THREAD_WEIGHT_DEFAULT, THREAD_WEIGHT_GLOBAL
from ...permissions.threads import exclude_invisible_posts


SPLIT_LIMIT = settings.MISAGO_POSTS_PER_PAGE + settings.MISAGO_POSTS_TAIL


class SplitError(Exception):
    def __init__(self, msg):
        self.msg = msg


def posts_split_endpoint(request, thread):
    try:
        posts = clean_posts_for_split(request, thread)
    except SplitError as e:
        return Response({'detail': e.msg}, status=400)

    # HERE run serializer to validate if split thread stuff

    # create thread
    # move posts to it
    # moderate new thread

    # sync old and new thread/categories


def clean_posts_for_split(request, thread):
    try:
        posts_ids = list(map(int, request.data.get('posts', [])))
    except (ValueError, TypeError):
        raise SplitError(_("One or more post ids received were invalid."))

    if not posts_ids:
        raise SplitError(_("You have to specify at least one post to split."))
    elif len(posts_ids) > SPLIT_LIMIT:
        message = ungettext(
            "No more than %(limit)s post can be split at single time.",
            "No more than %(limit)s posts can be split at single time.",
            SPLIT_LIMIT)
        raise SplitError(message % {'limit': SPLIT_LIMIT})

    posts_queryset = exclude_invisible_posts(request.user, thread.category, thread.post_set)
    posts_queryset = posts_queryset.select_for_update().filter(id__in=posts_ids).order_by('id')

    posts = []
    for post in posts_queryset:
        if post.is_event:
            raise SplitError(_("Events can't be split."))
        if post.pk == thread.first_post_id:
            raise SplitError(_("You can't split thread's first post."))
        if post.is_hidden and not thread.category.acl['can_hide_posts']:
            raise SplitError(_("You can't split posts the content you can't see."))

        posts.append(post)

    if len(posts) != len(posts_ids):
        raise SplitError(_("One or more posts to split could not be found."))

    return posts


class SplitPostsSerializer(serializers.Serializer):
    title = serializers.CharField()
    category = serializers.IntegerField()
    weight = serializers.IntegerField(
        required=False,
        allow_null=True,
        max_value=THREAD_WEIGHT_GLOBAL,
        min_value=THREAD_WEIGHT_DEFAULT,
    )
    is_hidden = serializers.NullBooleanField(required=False)
    is_closed = serializers.NullBooleanField(required=False)

    def validate_title(self, title):
        return validate_title(title)

    def validate_category(self, category_id):
        self.category = validate_category(self.context, category_id)
        return self.category

    def validate_weight(self, weight):
        try:
            add_acl(self.context, self.category)
        except AttributeError:
            return weight # don't validate weight further if category failed

        if weight > self.category.acl.get('can_pin_threads', 0):
            if weight == 2:
                raise ValidationError(_("You don't have permission to pin threads globally in this category."))
            else:
                raise ValidationError(_("You don't have permission to pin threads in this category."))
        return weight

    def validate_is_hidden(self, is_hidden):
        try:
            add_acl(self.context, self.category)
        except AttributeError:
            return is_hidden # don't validate closed further if category failed

        if is_hidden and not self.category.acl.get('can_hide_threads'):
            raise ValidationError(_("You don't have permission to hide threads in this category."))
        return is_hidden

    def validate_is_closed(self, is_closed):
        try:
            add_acl(self.context, self.category)
        except AttributeError:
            return is_closed # don't validate closed further if category failed

        if is_closed and not self.category.acl.get('can_close_threads'):
            raise ValidationError(_("You don't have permission to close threads in this category."))
        return is_closed

