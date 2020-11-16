from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext as _, ngettext
from rest_framework import serializers
from rest_framework.response import Response

from ....acl.objectacl import add_acl_to_obj
from ....conf import settings
from ....core.apipatch import ApiPatch
from ...models import PostLike
from ...moderation import posts as moderation
from ...permissions import (
    allow_approve_post,
    allow_hide_best_answer,
    allow_hide_post,
    allow_protect_post,
    allow_unhide_post,
    exclude_invisible_posts,
)

post_patch_dispatcher = ApiPatch()


def patch_acl(request, post, value):
    """useful little op that updates post acl to current state"""
    if value:
        add_acl_to_obj(request.user_acl, post)
        return {"acl": post.acl}
    return {"acl": None}


post_patch_dispatcher.add("acl", patch_acl)


def patch_is_liked(request, post, value):
    if not post.acl["can_like"]:
        raise PermissionDenied(_("You can't like posts in this category."))

    # lock user to protect us from likes flood
    request.user.lock()

    # grab like state for this post and user
    try:
        user_like = post.postlike_set.get(liker=request.user)
    except PostLike.DoesNotExist:
        user_like = None

    # no change
    if (value and user_like) or (not value and not user_like):
        return {
            "likes": post.likes,
            "last_likes": post.last_likes or [],
            "is_liked": value,
        }

    # like
    if value:
        post.postlike_set.create(
            category=post.category,
            thread=post.thread,
            liker=request.user,
            liker_name=request.user.username,
            liker_slug=request.user.slug,
        )
        post.likes += 1

    # unlike
    if not value:
        user_like.delete()
        post.likes -= 1

    post.last_likes = []
    for like in post.postlike_set.all()[:4]:
        post.last_likes.append({"id": like.liker_id, "username": like.liker_name})

    post.save(update_fields=["likes", "last_likes"])

    return {"likes": post.likes, "last_likes": post.last_likes or [], "is_liked": value}


post_patch_dispatcher.replace("is-liked", patch_is_liked)


def patch_is_protected(request, post, value):
    allow_protect_post(request.user_acl, post)
    if value:
        moderation.protect_post(request.user, post)
    else:
        moderation.unprotect_post(request.user, post)
    return {"is_protected": post.is_protected}


post_patch_dispatcher.replace("is-protected", patch_is_protected)


def patch_is_unapproved(request, post, value):
    allow_approve_post(request.user_acl, post)

    if value:
        raise PermissionDenied(_("Content approval can't be reversed."))

    moderation.approve_post(request.user, post)

    return {"is_unapproved": post.is_unapproved}


post_patch_dispatcher.replace("is-unapproved", patch_is_unapproved)


def patch_is_hidden(request, post, value):
    if value is True:
        allow_hide_post(request.user_acl, post)
        allow_hide_best_answer(request.user_acl, post)
        moderation.hide_post(request.user, post)
    elif value is False:
        allow_unhide_post(request.user_acl, post)
        moderation.unhide_post(request.user, post)

    return {"is_hidden": post.is_hidden}


post_patch_dispatcher.replace("is-hidden", patch_is_hidden)


def post_patch_endpoint(request, post):
    old_is_unapproved = post.is_unapproved

    response = post_patch_dispatcher.dispatch(request, post)

    # diff posts's state against pre-patch and resync thread/category if necessarys
    if old_is_unapproved != post.is_unapproved:
        post.thread.synchronize()
        post.thread.save()

        post.category.synchronize()
        post.category.save()

    return response


def bulk_patch_endpoint(request, thread):
    serializer = BulkPatchSerializer(
        data=request.data, context={"settings": request.settings}
    )
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    posts = clean_posts_for_patch(request, thread, serializer.data["ids"])

    old_unapproved_posts = [p.is_unapproved for p in posts].count(True)

    response = post_patch_dispatcher.dispatch_bulk(request, posts)

    new_unapproved_posts = [p.is_unapproved for p in posts].count(True)

    if old_unapproved_posts != new_unapproved_posts:
        thread.synchronize()
        thread.save()

        thread.category.synchronize()
        thread.category.save()

    return response


def clean_posts_for_patch(request, thread, posts_ids):
    posts_queryset = exclude_invisible_posts(
        request.user_acl, thread.category, thread.post_set
    )
    posts_queryset = posts_queryset.filter(id__in=posts_ids, is_event=False).order_by(
        "id"
    )

    posts = []
    for post in posts_queryset:
        post.category = thread.category
        post.thread = thread
        posts.append(post)

    if len(posts) != len(posts_ids):
        raise PermissionDenied(_("One or more posts to update could not be found."))

    return posts


class BulkPatchSerializer(serializers.Serializer):
    ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1), min_length=1
    )
    ops = serializers.ListField(
        child=serializers.DictField(), min_length=1, max_length=10
    )

    def validate_ids(self, data):
        settings = self.context["settings"]
        limit = settings.posts_per_page + settings.posts_per_page_orphans
        if len(data) > limit:
            message = ngettext(
                "No more than %(limit)s post can be updated at a single time.",
                "No more than %(limit)s posts can be updated at a single time.",
                limit,
            )
            raise serializers.ValidationError(message % {"limit": limit})
        return data
