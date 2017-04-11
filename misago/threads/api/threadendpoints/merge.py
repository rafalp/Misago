from rest_framework.response import Response

from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext

from misago.acl import add_acl
from misago.categories import THREADS_ROOT_NAME
from misago.threads.events import record_event
from misago.threads.models import Thread
from misago.threads.moderation import threads as moderation
from misago.threads.permissions import can_reply_thread, can_see_thread
from misago.threads.serializers import NewThreadSerializer, ThreadsListSerializer
from misago.threads.threadtypes import trees_map
from misago.threads.utils import get_thread_id_from_url

from .pollmergehandler import PollMergeHandler


MERGE_LIMIT = 20  # no more than 20 threads can be merged in single action


class MergeError(Exception):
    def __init__(self, msg):
        self.msg = msg


def thread_merge_endpoint(request, thread, viewmodel):
    if not thread.acl['can_merge']:
        raise PermissionDenied(_("You don't have permission to merge this thread with others."))

    other_thread_id = get_thread_id_from_url(request, request.data.get('thread_url', None))
    if not other_thread_id:
        return Response({'detail': _("This is not a valid thread link.")}, status=400)
    if other_thread_id == thread.pk:
        return Response({'detail': _("You can't merge thread with itself.")}, status=400)

    try:
        other_thread = viewmodel(request, other_thread_id, select_for_update=True).unwrap()
        if not can_reply_thread(request.user, other_thread):
            raise PermissionDenied(_("You can't merge this thread into thread you can't reply."))
        if not other_thread.acl['can_merge']:
            raise PermissionDenied(
                _("You don't have permission to merge this thread with current one.")
            )
    except PermissionDenied as e:
        return Response({'detail': e.args[0]}, status=400)
    except Http404:
        return Response(
            {
                'detail': _(
                    "The thread you have entered link to doesn't "
                    "exist or you don't have permission to see it."
                )
            },
            status=400,
        )

    polls_handler = PollMergeHandler([thread, other_thread])
    if len(polls_handler.polls) == 1:
        poll = polls_handler.polls[0]
        poll.move(other_thread)
    elif polls_handler.is_merge_conflict():
        if 'poll' in request.data:
            polls_handler.set_resolution(request.data.get('poll'))
            if polls_handler.is_valid():
                poll = polls_handler.get_resolution()
                if poll and poll.thread_id != other_thread.id:
                    other_thread.poll.delete()
                    poll.move(other_thread)
                elif not poll:
                    other_thread.poll.delete()
            else:
                return Response({'detail': _("Invalid choice.")}, status=400)
        else:
            return Response({'polls': polls_handler.get_available_resolutions()}, status=400)

    moderation.merge_thread(request, other_thread, thread)

    other_thread.synchronize()
    other_thread.save()

    other_thread.category.synchronize()
    other_thread.category.save()

    if thread.category != other_thread.category:
        thread.category.synchronize()
        thread.category.save()

    return Response({
        'id': other_thread.pk,
        'title': other_thread.title,
        'url': other_thread.get_absolute_url(),
    })


def threads_merge_endpoint(request):
    try:
        threads = clean_threads_for_merge(request)
    except MergeError as e:
        return Response({'detail': e.msg}, status=403)

    invalid_threads = []
    for thread in threads:
        if not thread.acl['can_merge']:
            invalid_threads.append({
                'id': thread.pk,
                'title': thread.title,
                'errors': [_("You don't have permission to merge this thread with others.")]
            })

    if invalid_threads:
        return Response(invalid_threads, status=403)

    serializer = NewThreadSerializer(context=request.user, data=request.data)
    if serializer.is_valid():
        polls_handler = PollMergeHandler(threads)
        if len(polls_handler.polls) == 1:
            poll = polls_handler.polls[0]
        elif polls_handler.is_merge_conflict():
            if 'poll' in request.data:
                polls_handler.set_resolution(request.data.get('poll'))
                if polls_handler.is_valid():
                    poll = polls_handler.get_resolution()
                else:
                    return Response({'detail': _("Invalid choice.")}, status=400)
            else:
                return Response({'polls': polls_handler.get_available_resolutions()}, status=400)
        else:
            poll = None

        new_thread = merge_threads(request, serializer.validated_data, threads, poll)
        return Response(ThreadsListSerializer(new_thread).data)
    else:
        return Response(serializer.errors, status=400)


def clean_threads_for_merge(request):
    try:
        threads_ids = list(map(int, request.data.get('threads', [])))
    except (ValueError, TypeError):
        raise MergeError(_("One or more thread ids received were invalid."))

    if len(threads_ids) < 2:
        raise MergeError(_("You have to select at least two threads to merge."))
    elif len(threads_ids) > MERGE_LIMIT:
        message = ungettext(
            "No more than %(limit)s thread can be merged at single time.",
            "No more than %(limit)s threads can be merged at single time.",
            MERGE_LIMIT,
        )
        raise MergeError(message % {'limit': MERGE_LIMIT})

    threads_tree_id = trees_map.get_tree_id_for_root(THREADS_ROOT_NAME)

    threads_queryset = Thread.objects.filter(
        id__in=threads_ids,
        category__tree_id=threads_tree_id,
    ).select_for_update().select_related('category').order_by('-id')

    threads = []
    for thread in threads_queryset:
        add_acl(request.user, thread)
        if can_see_thread(request.user, thread):
            threads.append(thread)

    if len(threads) != len(threads_ids):
        raise MergeError(_("One or more threads to merge could not be found."))

    return threads


def merge_threads(request, validated_data, threads, poll):
    new_thread = Thread(
        category=validated_data['category'],
        started_on=threads[0].started_on,
        last_post_on=threads[0].last_post_on,
    )

    new_thread.set_title(validated_data['title'])
    new_thread.save()

    if poll:
        poll.move(new_thread)

    categories = []
    for thread in threads:
        categories.append(thread.category)
        new_thread.merge(thread)
        thread.delete()

        record_event(
            request,
            new_thread,
            'merged',
            {
                'merged_thread': thread.title,
            },
            commit=False,
        )

    new_thread.synchronize()
    new_thread.save()

    if validated_data.get('weight') == Thread.WEIGHT_GLOBAL:
        moderation.pin_thread_globally(request, new_thread)
    elif validated_data.get('weight'):
        moderation.pin_thread_locally(request, new_thread)
    if validated_data.get('is_hidden', False):
        moderation.hide_thread(request, new_thread)
    if validated_data.get('is_closed', False):
        moderation.close_thread(request, new_thread)

    if new_thread.category not in categories:
        categories.append(new_thread.category)

    for category in categories:
        category.synchronize()
        category.save()

    # set extra attrs on thread for UI
    new_thread.is_read = False
    new_thread.subscription = None

    add_acl(request.user, new_thread)
    return new_thread
