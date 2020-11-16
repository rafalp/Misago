from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.utils.translation import gettext as _
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ...categories import PRIVATE_THREADS_ROOT_NAME, THREADS_ROOT_NAME
from ...core.shortcuts import get_int_or_404
from ..models import Post, Thread
from ..permissions import allow_use_private_threads
from ..viewmodels import (
    ForumThread,
    PrivateThread,
    PrivateThreadsCategory,
    ThreadsRootCategory,
)
from .postingendpoint import PostingEndpoint
from .threadendpoints.delete import delete_bulk, delete_thread
from .threadendpoints.editor import thread_start_editor
from .threadendpoints.list import private_threads_list_endpoint, threads_list_endpoint
from .threadendpoints.merge import thread_merge_endpoint, threads_merge_endpoint
from .threadendpoints.patch import bulk_patch_endpoint, thread_patch_endpoint


class ViewSet(viewsets.ViewSet):
    thread = None

    def get_thread(
        self, request, pk, path_aware=False, read_aware=False, subscription_aware=False
    ):
        return self.thread(  # pylint: disable=not-callable
            request,
            get_int_or_404(pk),
            path_aware=path_aware,
            read_aware=read_aware,
            subscription_aware=subscription_aware,
        )

    def retrieve(self, request, pk):
        thread = self.get_thread(
            request, pk, path_aware=True, read_aware=True, subscription_aware=True
        )

        return Response(thread.get_frontend_context())

    @transaction.atomic
    def partial_update(self, request, pk=None):
        thread = self.get_thread(request, pk).unwrap()
        return thread_patch_endpoint(request, thread)

    def patch(self, request):
        return bulk_patch_endpoint(request, self.thread)

    def delete(self, request, pk=None):
        if pk:
            thread = self.get_thread(request, pk).unwrap()
            return delete_thread(request, thread)
        return delete_bulk(request, self.thread)


class ThreadViewSet(ViewSet):
    category = ThreadsRootCategory
    thread = ForumThread

    def list(self, request):
        return threads_list_endpoint(request)

    @transaction.atomic
    def create(self, request):
        # Initialize empty instances for new thread
        thread = Thread()
        post = Post(thread=thread)

        # Put them through posting pipeline
        posting = PostingEndpoint(
            request,
            PostingEndpoint.START,
            tree_name=THREADS_ROOT_NAME,
            thread=thread,
            post=post,
        )

        if not posting.is_valid():
            return Response(posting.errors, status=400)

        posting.save()

        return Response(
            {"id": thread.pk, "title": thread.title, "url": thread.get_absolute_url()}
        )

    @action(detail=True, methods=["post"], url_path="merge", url_name="merge")
    @transaction.atomic
    def thread_merge(self, request, pk=None):
        thread = self.get_thread(request, pk).unwrap()
        return thread_merge_endpoint(request, thread, self.thread)

    @action(detail=False, methods=["post"], url_path="merge", url_name="merge")
    @transaction.atomic
    def threads_merge(self, request):
        return threads_merge_endpoint(request)

    @action(detail=False, methods=["get"])
    def editor(self, request):
        return thread_start_editor(request)


class PrivateThreadViewSet(ViewSet):
    category = PrivateThreadsCategory
    thread = PrivateThread

    def list(self, request):
        return private_threads_list_endpoint(request)

    @transaction.atomic
    def create(self, request):
        allow_use_private_threads(request.user_acl)
        if not request.user_acl["can_start_private_threads"]:
            raise PermissionDenied(_("You can't start private threads."))

        request.user.lock()

        # Initialize empty instances for new thread
        thread = Thread()
        post = Post(thread=thread)

        # Put them through posting pipeline
        posting = PostingEndpoint(
            request,
            PostingEndpoint.START,
            tree_name=PRIVATE_THREADS_ROOT_NAME,
            thread=thread,
            post=post,
        )

        if not posting.is_valid():
            return Response(posting.errors, status=400)

        posting.save()

        return Response(
            {"id": thread.pk, "title": thread.title, "url": thread.get_absolute_url()}
        )
