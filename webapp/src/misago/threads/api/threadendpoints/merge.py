from django.core.exceptions import PermissionDenied
from rest_framework.response import Response

from ....acl.objectacl import add_acl_to_obj
from ...events import record_event
from ...mergeconflict import MergeConflict
from ...models import Thread
from ...moderation import threads as moderation
from ...permissions import allow_merge_thread
from ...serializers import (
    MergeThreadSerializer,
    MergeThreadsSerializer,
    ThreadsListSerializer,
)


def thread_merge_endpoint(
    request, thread, viewmodel
):  # pylint: disable=too-many-branches
    allow_merge_thread(request.user_acl, thread)

    serializer = MergeThreadSerializer(
        data=request.data,
        context={"request": request, "thread": thread, "viewmodel": viewmodel},
    )

    if not serializer.is_valid():
        if "other_thread" in serializer.errors:
            errors = serializer.errors["other_thread"]
        elif "best_answer" in serializer.errors:
            errors = serializer.errors["best_answer"]
        elif "best_answers" in serializer.errors:
            return Response(
                {"best_answers": serializer.errors["best_answers"]}, status=400
            )
        elif "poll" in serializer.errors:
            errors = serializer.errors["poll"]
        elif "polls" in serializer.errors:
            return Response({"polls": serializer.errors["polls"]}, status=400)
        else:
            errors = list(serializer.errors.values())[0]
        return Response({"detail": errors[0]}, status=400)

    # merge conflict
    other_thread = serializer.validated_data["other_thread"]

    best_answer = serializer.validated_data.get("best_answer")
    if "best_answer" in serializer.merge_conflict and not best_answer:
        other_thread.clear_best_answer()
    if best_answer and best_answer != other_thread:
        other_thread.best_answer_id = thread.best_answer_id
        other_thread.best_answer_is_protected = thread.best_answer_is_protected
        other_thread.best_answer_marked_on = thread.best_answer_marked_on
        other_thread.best_answer_marked_by_id = thread.best_answer_marked_by_id
        other_thread.best_answer_marked_by_name = thread.best_answer_marked_by_name
        other_thread.best_answer_marked_by_slug = thread.best_answer_marked_by_slug

    poll = serializer.validated_data.get("poll")
    if "poll" in serializer.merge_conflict:
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

    return Response(
        {
            "id": other_thread.pk,
            "title": other_thread.title,
            "url": other_thread.get_absolute_url(),
        }
    )


def threads_merge_endpoint(request):
    serializer = MergeThreadsSerializer(
        data=request.data,
        context={"settings": request.settings, "user_acl": request.user_acl},
    )

    if not serializer.is_valid():
        if "threads" in serializer.errors:
            errors = {"detail": serializer.errors["threads"][0]}
            return Response(errors, status=403)
        if "non_field_errors" in serializer.errors:
            errors = {"detail": serializer.errors["non_field_errors"][0]}
            return Response(errors, status=403)
        return Response(serializer.errors, status=400)

    threads = serializer.validated_data["threads"]
    invalid_threads = []

    for thread in threads:
        try:
            allow_merge_thread(request.user_acl, thread)
        except PermissionDenied as e:
            invalid_threads.append(
                {"id": thread.pk, "title": thread.title, "errors": [str(e)]}
            )

    if invalid_threads:
        return Response(invalid_threads, status=403)

    # handle merge conflict
    merge_conflict = MergeConflict(serializer.validated_data, threads)
    merge_conflict.is_valid(raise_exception=True)

    new_thread = merge_threads(
        request, serializer.validated_data, threads, merge_conflict
    )
    return Response(ThreadsListSerializer(new_thread).data)


def merge_threads(request, validated_data, threads, merge_conflict):
    new_thread = Thread(
        category=validated_data["category"],
        started_on=threads[0].started_on,
        last_post_on=threads[0].last_post_on,
    )

    new_thread.set_title(validated_data["title"])
    new_thread.save()

    resolution = merge_conflict.get_resolution()

    best_answer = resolution.get("best_answer")
    if best_answer:
        new_thread.best_answer_id = best_answer.best_answer_id
        new_thread.best_answer_is_protected = best_answer.best_answer_is_protected
        new_thread.best_answer_marked_on = best_answer.best_answer_marked_on
        new_thread.best_answer_marked_by_id = best_answer.best_answer_marked_by_id
        new_thread.best_answer_marked_by_name = best_answer.best_answer_marked_by_name
        new_thread.best_answer_marked_by_slug = best_answer.best_answer_marked_by_slug

    poll = resolution.get("poll")
    if poll:
        poll.move(new_thread)

    categories = []
    for thread in threads:
        categories.append(thread.category)
        new_thread.merge(thread)
        thread.delete()

        record_event(
            request, new_thread, "merged", {"merged_thread": thread.title}, commit=False
        )

    new_thread.synchronize()
    new_thread.save()

    if validated_data.get("weight") == Thread.WEIGHT_GLOBAL:
        moderation.pin_thread_globally(request, new_thread)
    elif validated_data.get("weight"):
        moderation.pin_thread_locally(request, new_thread)
    if validated_data.get("is_hidden", False):
        moderation.hide_thread(request, new_thread)
    if validated_data.get("is_closed", False):
        moderation.close_thread(request, new_thread)

    if new_thread.category not in categories:
        categories.append(new_thread.category)

    for category in categories:
        category.synchronize()
        category.save()

    # set extra attrs on thread for UI
    new_thread.is_read = False
    new_thread.subscription = None

    add_acl_to_obj(request.user_acl, new_thread)
    return new_thread
