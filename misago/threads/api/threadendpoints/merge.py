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

    serializer.is_valid(raise_exception=True)

    # merge polls
    other_thread = serializer.validated_data['other_thread']
    poll = serializer.validated_data['poll']

    if poll:
        if hasattr(other_thread, 'poll') and poll != other_thread.poll:
            other_thread.poll.delete()
        poll.move(other_thread)
    else:
        if hasattr(thread, 'poll'):
            thread.poll.delete()
        if hasattr(other_thread, 'poll'):
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

    data = serializer.validated_data
    
    threads = data['threads']
    poll = data['poll']

    new_thread = Thread(
        category=data['category'],
        started_on=threads[0].started_on,
        last_post_on=threads[0].last_post_on,
    )

    new_thread.set_title(data['title'])
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
                'merged_thread': thread.title
            },
            commit=False,
        )

    new_thread.synchronize()
    new_thread.save()

    if data.get('weight') == Thread.WEIGHT_GLOBAL:
        moderation.pin_thread_globally(request, new_thread)
    elif data.get('weight'):
        moderation.pin_thread_locally(request, new_thread)
    if data.get('is_hidden', False):
        moderation.hide_thread(request, new_thread)
    if data.get('is_closed', False):
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

    return Response(ThreadsListSerializer(new_thread).data)
