from django.http import HttpRequest, JsonResponse, Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.decorators import api_view

from ...categories.models import Category
from ...notifications.models import WatchedThread
from ...notifications.threads import ThreadNotifications, get_watched_thread
from ...threads.models import Thread
from ...threads.participants import make_thread_participants_aware
from ...threads.permissions import (
    allow_see_private_thread,
    allow_see_thread,
    allow_use_private_threads,
)
from ..decorators import require_auth


class ThreadWatchSerializer(serializers.Serializer):
    notifications = serializers.ChoiceField(
        choices=ThreadNotifications.choices,
    )


@api_view(["POST"])
@require_auth
def watch_thread(request: HttpRequest, thread_id: int) -> JsonResponse:
    thread = get_object_or_404(Thread.objects.select_related("category"), id=thread_id)
    if not Category.objects.root_category().has_child(thread.category):
        raise Http404()

    allow_see_thread(request.user_acl, thread)
    return watch_thread_shared_logic(request, thread)


@api_view(["POST"])
@require_auth
def watch_private_thread(request: HttpRequest, thread_id: int) -> JsonResponse:
    allow_use_private_threads(request.user_acl)

    thread = get_object_or_404(Thread, id=thread_id)
    if Category.objects.private_threads().id != thread.category_id:
        raise Http404()

    make_thread_participants_aware(request.user, thread)
    allow_see_private_thread(request.user_acl, thread)

    return watch_thread_shared_logic(request, thread)


def watch_thread_shared_logic(request: HttpRequest, thread: Thread) -> JsonResponse:
    serializer = ThreadWatchSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    notifications = serializer.data["notifications"]

    if not notifications:
        WatchedThread.objects.filter(user=request.user, thread=thread).delete()
        return JsonResponse(serializer.data)

    send_emails = notifications == ThreadNotifications.SITE_AND_EMAIL

    watched_thread = get_watched_thread(request.user, thread)
    if watched_thread:
        if watched_thread.send_emails != send_emails:
            watched_thread.send_emails = send_emails
            watched_thread.save(update_fields=["send_emails"])
    else:
        WatchedThread.objects.create(
            user=request.user,
            category_id=thread.category_id,
            thread=thread,
            send_emails=send_emails,
        )

    return JsonResponse(serializer.data)
