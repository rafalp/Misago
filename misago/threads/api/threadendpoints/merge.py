from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404
from django.utils.translation import gettext as _, ungettext

from rest_framework import serializers
from rest_framework.response import Response

from misago.acl import add_acl
from misago.categories.models import THREADS_ROOT_NAME, Category
from misago.categories.permissions import can_browse_category, can_see_category

from ...events import record_event
from ...models import THREAD_WEIGHT_DEFAULT, THREAD_WEIGHT_GLOBAL, Thread
from ...moderation import threads as moderation
from ...permissions import allow_start_thread, can_see_thread
from ...serializers import ThreadsListSerializer
from ...threadtypes import trees_map
from ...validators import validate_title
from ...utils import add_categories_to_threads, get_thread_id_from_url


MERGE_LIMIT = 20 # no more than 20 threads can be merged in single action


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
        other_thread = viewmodel(request, other_thread_id, select_for_update=True).model
    except PermissionDenied as e:
        return Response({
            'detail': e.args[0]
        }, status=400)
    except Http404:
        return Response({
            'detail': _("The thread you have entered link to doesn't exist or you don't have permission to see it.")
        }, status=400)

    if not other_thread.acl['can_merge']:
        return Response({
            'detail': _("You don't have permission to merge this thread with current one.")
        }, status=400)

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
        'url': other_thread.get_absolute_url()
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
                'errors': [
                    _("You don't have permission to merge this thread with others.")
                ]
            })

    if invalid_threads:
        return Response(invalid_threads, status=403)

    serializer = MergeThreadsSerializer(context=request.user, data=request.data)
    if serializer.is_valid():
        new_thread = merge_threads(request, serializer.validated_data, threads)
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
            MERGE_LIMIT)
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


def merge_threads(request, validated_data, threads):
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

        record_event(request, new_thread, 'merged', {
            'merged_thread': thread.title,
        }, commit=False)

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
            id__in=request.user.acl['visible_categories']
        ))
        add_categories_to_threads(validated_data['top_category'], categories, [new_thread])
    else:
        new_thread.top_category = None

    new_thread.save()

    add_acl(request.user, new_thread)
    return new_thread


def validate_category(user, category_id, allow_root=False):
    try:
        threads_tree_id = trees_map.get_tree_id_for_root(THREADS_ROOT_NAME)
        category = Category.objects.get(
            tree_id=threads_tree_id,
            id=category_id,
        )
    except Category.DoesNotExist:
        category = None

    # Skip ACL validation for root category?
    if allow_root and category and not category.level:
        return category

    if not category or not can_see_category(user, category):
        raise ValidationError(_("Requested category could not be found."))

    if not can_browse_category(user, category):
        raise ValidationError(_("You don't have permission to access this category."))
    return category


class MergeThreadsSerializer(serializers.Serializer):
    title = serializers.CharField()
    category = serializers.IntegerField()
    top_category = serializers.IntegerField(required=False, allow_null=True)
    weight = serializers.IntegerField(
        required=False,
        allow_null=True,
        max_value=THREAD_WEIGHT_GLOBAL,
        min_value=THREAD_WEIGHT_DEFAULT,
    )
    is_closed = serializers.NullBooleanField(required=False)

    def validate_title(self, title):
        return validate_title(title)

    def validate_top_category(self, category_id):
        return validate_category(self.context, category_id, allow_root=True)

    def validate_category(self, category_id):
        self.category = validate_category(self.context, category_id)
        return self.category

    def validate_weight(self, weight):
        try:
            add_acl(self.context, self.category)
        except AttributeError:
            return weight # don't validate weight further if category failed

        if weight > self.category.acl.get('can_pin_threads', 0):
            if weight == 2:
                raise ValidationError(_("You don't have permission to pin threads globally in this category."))
            else:
                raise ValidationError(_("You don't have permission to pin threads in this category."))
        return weight

    def validate_is_closed(self, is_closed):
        try:
            add_acl(self.context, self.category)
        except AttributeError:
            return is_closed # don't validate closed further if category failed

        if is_closed and not self.category.acl.get('can_close_threads'):
            raise ValidationError(_("You don't have permission to close threads in this category."))
        return is_closed
