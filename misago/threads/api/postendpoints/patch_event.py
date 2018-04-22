from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _

from misago.acl import add_acl
from misago.api.patch import ApiPatch
from misago.threads import moderation
from misago.threads.permissions import allow_hide_event, allow_unhide_event


event_patch_dispatcher = ApiPatch()


def patch_acl(request, event, value):
    """useful little op that updates event acl to current state"""
    if value:
        add_acl(request.user, event)
        return {'acl': event.acl}
    else:
        return {'acl': None}


event_patch_dispatcher.add('acl', patch_acl)


def patch_is_hidden(request, event, value):
    if value:
        allow_hide_event(request.user, event)
        moderation.hide_post(request.user, event)
    else:
        allow_unhide_event(request.user, event)
        moderation.unhide_post(request.user, event)

    return {'is_hidden': event.is_hidden}


event_patch_dispatcher.replace('is-hidden', patch_is_hidden)


def event_patch_endpoint(request, event):
    old_is_hidden = event.is_hidden

    response = event_patch_dispatcher.dispatch(request, event)

    if old_is_hidden != event.is_hidden:
        event.thread.synchronize()
        event.thread.save()

        event.category.synchronize()
        event.category.save()
    return response
