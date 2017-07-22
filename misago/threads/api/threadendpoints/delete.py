from rest_framework.response import Response

from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import Http404
from django.utils.six import text_type
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext

from misago.conf import settings
from misago.threads.permissions import allow_delete_thread
from misago.threads.moderation import threads as moderation


DELETE_LIMIT = settings.MISAGO_THREADS_PER_PAGE + settings.MISAGO_THREADS_TAIL


@transaction.atomic
def delete_thread(request, thread):
    allow_delete_thread(request.user, thread)
    moderation.delete_thread(request.user, thread)
    return Response({})


def delete_bulk(request, viewmodel):
    threads_ids = clean_threads_ids(request)

    errors = []
    for thread_id in threads_ids:
        try:
            thread = viewmodel(request, thread_id).unwrap()
            delete_thread(request, thread)
        except PermissionDenied as e:
            errors.append({
                'thread': {
                    'id': thread.id,
                    'title': thread.title
                },
                'error': text_type(e)
            })
        except Http404:
            pass # skip invisible threads

    if errors:
        return Response(errors, status=400)
    return Response([])


def clean_threads_ids(request):
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

    return set(threads_ids)
