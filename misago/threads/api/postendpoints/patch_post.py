from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _

from misago.acl import add_acl
from misago.conf import settings
from misago.core.apipatch import ApiPatch
from misago.threads.models import PostLike
from misago.threads.moderation import posts as moderation
from misago.threads.permissions import (
    allow_approve_post, allow_hide_post, allow_protect_post, allow_unhide_post)
from misago.threads.permissions import exclude_invisible_posts


PATCH_LIMIT = settings.MISAGO_POSTS_PER_PAGE + settings.MISAGO_POSTS_TAIL

post_patch_dispatcher = ApiPatch()


def patch_acl(request, post, value):
    """useful little op that updates post acl to current state"""
    if value:
        add_acl(request.user, post)
        return {'acl': post.acl}
    else:
        return {'acl': None}


post_patch_dispatcher.add('acl', patch_acl)


def patch_is_liked(request, post, value):
    if not post.acl['can_like']:
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
            'likes': post.likes,
            'last_likes': post.last_likes or [],
            'is_liked': value,
        }

    # like
    if value:
        post.postlike_set.create(
            category=post.category,
            thread=post.thread,
            liker=request.user,
            liker_name=request.user.username,
            liker_slug=request.user.slug,
            liker_ip=request.user_ip,
        )
        post.likes += 1

    # unlike
    if not value:
        user_like.delete()
        post.likes -= 1

    post.last_likes = []
    for like in post.postlike_set.all()[:4]:
        post.last_likes.append({
            'id': like.liker_id,
            'username': like.liker_name,
        })

    post.save(update_fields=['likes', 'last_likes'])

    return {
        'likes': post.likes,
        'last_likes': post.last_likes or [],
        'is_liked': value,
    }


post_patch_dispatcher.replace('is-liked', patch_is_liked)


def patch_is_protected(request, post, value):
    allow_protect_post(request.user, post)
    if value:
        moderation.protect_post(request.user, post)
    else:
        moderation.unprotect_post(request.user, post)
    return {'is_protected': post.is_protected}


post_patch_dispatcher.replace('is-protected', patch_is_protected)


def patch_is_unapproved(request, post, value):
    allow_approve_post(request.user, post)

    if value:
        raise PermissionDenied(_("Content approval can't be reversed."))

    moderation.approve_post(request.user, post)

    return {'is_unapproved': post.is_unapproved}


post_patch_dispatcher.replace('is-unapproved', patch_is_unapproved)


def patch_is_hidden(request, post, value):
    if value is True:
        allow_hide_post(request.user, post)
        moderation.hide_post(request.user, post)
    elif value is False:
        allow_unhide_post(request.user, post)
        moderation.unhide_post(request.user, post)

    return {'is_hidden': post.is_hidden}


post_patch_dispatcher.replace('is-hidden', patch_is_hidden)


def post_patch_endpoint(request, post):
    old_is_hidden = post.is_hidden
    old_is_unapproved = post.is_unapproved
    old_thread = post.thread
    old_category = post.category

    response = post_patch_dispatcher.dispatch(request, post)

    # diff posts's state against pre-patch and resync category if necessary
    hidden_changed = old_is_hidden != post.is_hidden
    unapproved_changed = old_is_unapproved != post.is_unapproved
    thread_changed = old_thread != post.thread
    category_changed = old_category != post.category

    if hidden_changed or unapproved_changed or thread_changed or category_changed:
        post.thread.synchronize()
        post.thread.save()

        post.category.synchronize()
        post.category.save()

        if thread_changed:
            old_thread.synchronize()
            old_thread.save()

        if category_changed:
            old_category.synchronize()
            old_category.save()
    return response


def bulk_patch_endpoint(request, thread):
    posts = clean_posts_for_patch(request, thread)

    hidden_posts = 0
    revealed_posts = 0
    moved_posts = 0

    response = post_patch_dispatcher.dispatch_bulk(request, posts)


def clean_posts_for_patch(request, thread):
    if not isinstance(request.data, dict):
        raise PermissionDenied(_("Bulk PATCH request should be a dict with ids and ops keys."))

    # todo: move this ids list cleanup step to utility

    try:
        posts_ids = list(map(int, request.data.get('ids', [])))
    except (ValueError, TypeError):
        raise PermissionDenied(_("One or more post ids received were invalid."))

    if not posts_ids:
        raise PermissionDenied(_("You have to specify at least one post to update."))
    elif len(posts_ids) > PATCH_LIMIT:
        message = ungettext(
            "No more than %(limit)s post can be updated at single time.",
            "No more than %(limit)s posts can be updated at single time.",
            PATCH_LIMIT,
        )
        raise PermissionDenied(message % {'limit': PATCH_LIMIT})

    posts_queryset = exclude_invisible_posts(request.user, thread.category, thread.post_set)
    posts_queryset = posts_queryset.filter(id__in=posts_ids).order_by('id')

    posts = []
    for post in posts_queryset:
        post.category = thread.category
        post.thread = thread
        posts.append(post)

    if len(posts) != len(posts_ids):
        raise PermissionDenied(_("One or more posts to update could not be found."))

    return posts
