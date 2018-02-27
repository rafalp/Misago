from rest_framework.response import Response

from django.core.exceptions import PermissionDenied
from django.utils.six import text_type
from django.utils.translation import ugettext as _

from misago.acl import add_acl
from misago.threads.events import record_event
from misago.threads.models import Thread
from misago.threads.moderation import threads as moderation
from misago.threads.permissions import allow_merge_thread
from misago.threads.pollmergehandler import PollMergeHandler
from misago.threads.serializers import (
    MergeThreadSerializer, MergeThreadsSerializer, ThreadsListSerializer)


def thread_merge_endpoint(request, thread, viewmodel):
    allow_merge_thread(request.user, thread)

    serializer = MergeThreadSerializer(
        data=request.data,
        context={
            'request': request,
            'thread': thread,
            'viewmodel': viewmodel,
        },
    )

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    # interrupt merge with request for poll resolution?
    if serializer.validated_data.get('polls'):
        return Response({'polls': serializer.validated_data['polls']}, status=400)

    # merge polls
    other_thread = serializer.validated_data['other_thread']
    poll = serializer.validated_data.get('poll')

    if len(serializer.polls_handler.polls) == 1:
        poll.move(other_thread)
    elif serializer.polls_handler.is_merge_conflict():
        if poll and poll.thread_id != other_thread.id:
            other_thread.poll.delete()
            poll.move(other_thread)
        elif not poll:
            other_thread.poll.delete()

    # merge thread contents
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
    serializer = MergeThreadsSerializer(
        data=request.data,
        context={
            'user': request.user
        },
    )

    serializer.is_valid(raise_exception=True)

    new_thread = merge_threads(request, serializer.validated_data)
    return Response(ThreadsListSerializer(new_thread).data)


def merge_threads(request, validated_data):
    threads = validated_data['threads']
    poll = validated_data.get('poll')

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
