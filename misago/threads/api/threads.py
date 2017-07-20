from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.utils.translation import ugettext as _

from misago.categories import PRIVATE_THREADS_ROOT_NAME, THREADS_ROOT_NAME
from misago.core.shortcuts import get_int_or_404
from misago.threads.models import Post, Thread
from misago.threads.moderation import threads as moderation
from misago.threads.permissions import allow_use_private_threads
from misago.threads.viewmodels import (ForumThread, PrivateThread,
    ThreadsRootCategory, PrivateThreadsCategory)

from .postingendpoint import PostingEndpoint
from .threadendpoints.delete import delete_bulk, delete_thread
from .threadendpoints.editor import thread_start_editor
from .threadendpoints.list import private_threads_list_endpoint, threads_list_endpoint
from .threadendpoints.merge import thread_merge_endpoint, threads_merge_endpoint
from .threadendpoints.patch import thread_patch_endpoint
from .threadendpoints.read import read_private_threads, read_threads


class ViewSet(viewsets.ViewSet):
    thread = None

    def get_thread(self, request, pk, path_aware=False, read_aware=False, subscription_aware=False):
        return self.thread(
            request,
            get_int_or_404(pk),
            path_aware=path_aware,
            read_aware=read_aware,
            subscription_aware=subscription_aware,
        )

    def retrieve(self, request, pk):
        thread = self.get_thread(
            request,
            pk,
            path_aware=True,
            read_aware=True,
            subscription_aware=True,
        )

        return Response(thread.get_frontend_context())

    @transaction.atomic
    def partial_update(self, request, pk=None):
        request.user.lock()
        thread = self.get_thread(request, pk).unwrap()
        return thread_patch_endpoint(request, thread)

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

        if posting.is_valid():
            posting.save()

            return Response({
                'id': thread.pk,
                'title': thread.title,
                'url': thread.get_absolute_url(),
            })
        else:
            return Response(posting.errors, status=400)

    @detail_route(methods=['post'], url_path='merge')
    @transaction.atomic
    def thread_merge(self, request, pk=None):
        thread = self.get_thread(request, pk).unwrap()
        return thread_merge_endpoint(request, thread, self.thread)

    @list_route(methods=['post'], url_path='merge')
    @transaction.atomic
    def threads_merge(self, request):
        return threads_merge_endpoint(request)

    @list_route(methods=['get'])
    def editor(self, request):
        return thread_start_editor(request)

    @list_route(methods=['post'])
    @transaction.atomic
    def read(self, request):
        read_threads(request.user, request.GET.get('category'))
        return Response({})


class PrivateThreadViewSet(ViewSet):
    category = PrivateThreadsCategory
    thread = PrivateThread

    def list(self, request):
        return private_threads_list_endpoint(request)

    @transaction.atomic
    def create(self, request):
        allow_use_private_threads(request.user)
        if not request.user.acl_cache['can_start_private_threads']:
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

        if posting.is_valid():
            posting.save()

            return Response({
                'id': thread.pk,
                'title': thread.title,
                'url': thread.get_absolute_url(),
            })
        else:
            return Response(posting.errors, status=400)

    @list_route(methods=['post'])
    @transaction.atomic
    def read(self, request):
        allow_use_private_threads(request.user)
        read_private_threads(request.user)
        return Response({})
