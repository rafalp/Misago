from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext as _

from misago.acl import add_acl
from misago.core.apipatch import ApiPatch
from ...moderation import posts as moderation
from ...permissions.threads import allow_approve_post, allow_hide_post, allow_protect_post, allow_unhide_post


post_patch_dispatcher = ApiPatch()


def patch_acl(request, post, value):
    """useful little op that updates post acl to current state"""
    if value:
        add_acl(request.user, post)
        return {'acl': post.acl}
    else:
        return {'acl': None}
post_patch_dispatcher.add('acl', patch_acl)


def patch_is_protected(request, post, value):
    allow_protect_post(request.user, post)
    if value:
        moderation.protect_post(request.user, post)
    else:
        moderation.unprotect_post(request.user, post)
    return {'is_protected': post.is_protected}
post_patch_dispatcher.replace('is-protected', patch_is_protected)


def patch_is_unapproved(request, post, value):
    if value is False:
        allow_approve_post(request.user, post)
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
