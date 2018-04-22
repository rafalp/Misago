from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from django.core.exceptions import PermissionDenied
from django.utils.six import text_type
from django.utils.translation import ugettext as _

from misago.acl import add_acl
from misago.threads import moderation
from misago.threads.events import record_event
from misago.threads.models import Thread
from misago.threads.permissions import allow_merge_thread
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

    # merge conflict
    other_thread = serializer.validated_data['other_thread']

    best_answer = serializer.validated_data.get('best_answer')
    if 'best_answer' in serializer.merge_conflict and not best_answer:
        other_thread.clear_best_answer()
    if best_answer and best_answer != other_thread:
        other_thread.best_answer_id = thread.best_answer_id
        other_thread.best_answer_is_protected = thread.best_answer_is_protected
        other_thread.best_answer_marked_on = thread.best_answer_marked_on
        other_thread.best_answer_marked_by_id = thread.best_answer_marked_by_id
        other_thread.best_answer_marked_by_name = thread.best_answer_marked_by_name
        other_thread.best_answer_marked_by_slug = thread.best_answer_marked_by_slug

    poll = serializer.validated_data.get('poll')
    if 'poll' in serializer.merge_conflict:
        if poll and poll.thread_id != other_thread.id:
            other_thread.poll.delete()
            poll.move(other_thread)
        elif not poll:
            other_thread.poll.delete()
    elif poll:
        poll.move(other_thread)

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

    threads = serializer.validated_data['threads']

    data = serializer.validated_data
    threads = data['threads']

    new_thread = Thread(
        category=data['category'],
        started_on=threads[0].started_on,
        last_post_on=threads[0].last_post_on,
    )

    new_thread.set_title(data['title'])
    new_thread.save()

    # handle merge conflict
    best_answer = data.get('best_answer')
    if best_answer:
        new_thread.best_answer_id = best_answer.best_answer_id
        new_thread.best_answer_is_protected = best_answer.best_answer_is_protected
        new_thread.best_answer_marked_on = best_answer.best_answer_marked_on
        new_thread.best_answer_marked_by_id = best_answer.best_answer_marked_by_id
        new_thread.best_answer_marked_by_name = best_answer.best_answer_marked_by_name
        new_thread.best_answer_marked_by_slug = best_answer.best_answer_marked_by_slug

    poll = data.get('poll')
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
