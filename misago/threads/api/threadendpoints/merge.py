from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.utils.translation import gettext as _, ungettext

from rest_framework.response import Response

from misago.acl import add_acl
from misago.categories.models import CATEGORIES_TREE_ID, Category
from misago.categories.permissions import can_see_category, can_browse_category

from misago.threads.models import Thread
from misago.threads.permissions import can_see_thread
from misago.threads.serializers import (
    ThreadListSerializer, MergeThreadsSerializer)
from misago.threads.utils import add_categories_to_threads


MERGE_LIMIT = 20 # no more than 20 threads can be merged in single action


class MergeError(Exception):
    def __init__(self, msg):
        self.msg = msg


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
                'errors': [
                    _("You don't have permission to merge this thread with others.")
                ]
            })

    if invalid_threads:
        return Response(invalid_threads, status=403)

    serializer = MergeThreadsSerializer(context=request.user, data=request.data)
    if serializer.is_valid():
        new_thread = merge_threads(
            request.user, serializer.validated_data, threads)
        return Response(ThreadListSerializer(new_thread).data)
    else:
        return Response(serializer.errors, status=400)


def clean_threads_for_merge(request):
    try:
        threads_ids = map(int, request.data.get('threads', []))
    except (ValueError, TypeError):
        raise MergeError(_("One or more thread ids received were invalid."))

    if len(threads_ids) < 2:
        raise MergeError(_("You have to select at least two threads to merge."))
    elif len(threads_ids) > MERGE_LIMIT:
        message = ungettext(
            "No more than %(limit)s thread can be merged at single time.",
            "No more than %(limit)s threads can be merged at single time.",
            MERGE_LIMIT)
        raise MergeError(message % {'limit': settings.thread_title_length_max})

    threads_queryset = Thread.objects.filter(
        id__in=threads_ids,
        category__tree_id=CATEGORIES_TREE_ID,
    ).select_related('category').order_by('-id')

    threads = []
    for thread in threads_queryset:
        add_acl(request.user, thread)
        if can_see_thread(request.user, thread):
            threads.append(thread)

    if len(threads) != len(threads_ids):
        raise MergeError(_("One or more threads to merge could not be found."))

    return threads


@transaction.atomic
def merge_threads(user, validated_data, threads):
    new_thread = Thread(
        category=validated_data['category'],
        weight=validated_data.get('weight', 0),
        is_closed=validated_data.get('is_closed', False),
        started_on=threads[0].started_on,
        last_post_on=threads[0].last_post_on,
    )

    new_thread.set_title(validated_data['title'])
    new_thread.save()

    categories = []
    for thread in threads:
        categories.append(thread.category)
        new_thread.merge(thread)
        thread.delete()

    new_thread.synchronize()
    new_thread.save()

    if new_thread.category not in categories:
        categories.append(new_thread.category)

    for category in categories:
        category.synchronize()
        category.save()

    # set extra attrs on thread for UI
    new_thread.is_read = False
    new_thread.subscription = None

    # add top category to thread
    if validated_data.get('top_category'):
        categories = list(Category.objects.all_categories().filter(
            id__in=user.acl['visible_categories']
        ))
        add_categories_to_threads(
            validated_data['top_category'], categories, [new_thread])
    else:
        new_thread.top_category = None

    new_thread.save()

    add_acl(user, new_thread)
    return new_thread
