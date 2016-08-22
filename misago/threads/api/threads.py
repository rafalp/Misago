from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.utils.translation import gettext as _

from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from misago.acl import add_acl
from misago.categories.models import THREADS_ROOT_NAME, Category
from misago.categories.permissions import allow_browse_category, allow_see_category
from misago.core.shortcuts import get_int_or_404, get_object_or_404
from misago.readtracker.categoriestracker import read_category

from ..models import Post, Subscription, Thread
from ..moderation import threads as moderation
from ..permissions.threads import can_start_thread
from ..subscriptions import make_subscription_aware
from ..threadtypes import trees_map
from ..viewmodels.thread import ForumThread
from .postingendpoint import PostingEndpoint
from .threadendpoints.editor import thread_start_editor
from .threadendpoints.list import threads_list_endpoint
from .threadendpoints.merge import thread_merge_endpoint, threads_merge_endpoint
from .threadendpoints.patch import thread_patch_endpoint


class ViewSet(viewsets.ViewSet):
    thread = None
    TREE_ID = None

    def get_thread(self, request, pk, read_aware=True, subscription_aware=True, select_for_update=False):
        return self.thread(
            request,
            get_int_or_404(pk),
            None,
            read_aware,
            subscription_aware,
            select_for_update
        )

    def get_thread_for_update(self, request, pk):
        return self.get_thread(
            request, pk,
            read_aware=False,
            subscription_aware=False,
            select_for_update=True
        )

    def list(self, request):
        return threads_list_endpoint(request)

    def retrieve(self, request, pk):
        thread = self.get_thread(request, pk)
        return Response(thread.get_frontend_context())

    @transaction.atomic
    def partial_update(self, request, pk):
        thread = self.get_thread_for_update(request, pk).thread
        return thread_patch_endpoint(request, thread)

    @transaction.atomic
    def destroy(self, request, pk):
        thread = self.get_thread_for_update(request, pk).thread

        if thread.acl.get('can_hide') == 2:
            moderation.delete_thread(request.user, thread)
            return Response({'detail': 'ok'})
        else:
            raise PermissionDenied(_("You don't have permission to delete this thread."))


class ThreadViewSet(ViewSet):
    thread = ForumThread

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
            post=post
        )

        if posting.is_valid():
            posting.save()

            return Response({
                'id': thread.pk,
                'title': thread.title,
                'url': thread.get_absolute_url()
            })
        else:
            return Response(posting.errors, status=400)

    @detail_route(methods=['post'], url_path='merge')
    @transaction.atomic
    def thread_merge(self, request, pk):
        thread = self.get_thread_for_update(request, pk).thread
        return thread_merge_endpoint(request, thread, self.thread)

    @list_route(methods=['post'], url_path='merge')
    @transaction.atomic
    def threads_merge(self, request):
        return threads_merge_endpoint(request)

    @list_route(methods=['post'])
    def read(self, request):
        if request.query_params.get('category'):
            threads_tree_id = trees_map.get_tree_id_for_root(THREADS_ROOT_NAME)

            category_id = get_int_or_404(request.query_params.get('category'))
            category = get_object_or_404(Category,
                id=category_id,
                tree_id=threads_tree_id,
            )

            allow_see_category(request.user, category)
            allow_browse_category(request.user, category)
        else:
            category = Category.objects.root_category()

        read_category(request.user, category)
        return Response({'detail': 'ok'})

    @list_route(methods=['get'])
    def editor(self, request):
        return thread_start_editor(request)
