from rest_framework.response import Response

from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.utils.six import text_type
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext

from misago.conf import settings
from misago.threads.moderation import threads as moderation


DELETE_LIMIT = settings.MISAGO_THREADS_PER_PAGE + settings.MISAGO_THREADS_TAIL


@transaction.atomic
def delete_thread(request, thread):
    allow_delete_thread(request.user, thread)
    moderation.delete_thread(request.user, thread)

    return Response({})


def delete_bulk(request, viewmodel):
    threads = clean_threads_for_delete(request, viewmodel)
    raise Exception(threads)

    errors = []
    for thread in threads:
        try:
            allow_delete_thread(request.user, thread)
        except PermissionDenied as e:
            errors.append({
                'thread': {
                    'id': thread.id,
                    'title': thread.title
                },
                'error': text_type(e)
            })

    if errors:
        return Response(errors, status_code=403)

    for thread in delete:
        with transaction.atomic():
            moderation.delete_thread(request.user, thread)

    return Response({})


def clean_threads_for_delete(request, viewmodel):
    try:
        threads_ids = list(map(int, request.data or []))
    except (ValueError, TypeError):
        raise PermissionDenied(_("One or more thread ids received were invalid."))

    if not threads_ids:
        raise PermissionDenied(_("You have to specify at least one thread to delete."))
    elif len(threads_ids) > DELETE_LIMIT:
        message = ungettext(
            "No more than %(limit)s thread can be deleted at single time.",
            "No more than %(limit)s threads can be deleted at single time.",
            DELETE_LIMIT,
        )
        raise PermissionDenied(message % {'limit': DELETE_LIMIT})

    threads = [viewmodel(request, pk) for pk in threads_ids]
    if len(threads) != len(threads_ids):
        raise PermissionDenied(_("One or more threads to delete could not be found."))

    return threads


def allow_delete_thread(user, thread):
    if thread.acl.get('can_delete') != 2:
        raise PermissionDenied(_("You don't have permission to delete this thread."))
