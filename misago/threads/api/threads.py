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
from .threadendpoints.list import threads_list_endpoint
from .threadendpoints.merge import threads_merge_endpoint
from .threadendpoints.patch import thread_patch_endpoint


class ViewSet(viewsets.ViewSet):
    thread = None
    TREE_ID = None

    def get_thread(self, request, pk):
        return self.thread(request, get_int_or_404(pk), read_aware=True, subscription_aware=True)

    def list(self, request):
        return threads_list_endpoint(request)

    def retrieve(self, request, pk):
        thread = self.get_thread(request, pk)
        return Response(thread.get_frontend_context())

    def partial_update(self, request, pk):
        thread = self.get_thread(request, pk)
        return thread_patch_endpoint.dispatch(request, thread.thread)

    def destroy(self, request, pk):
        thread = self.get_thread(request, pk).thread

        if thread.acl.get('can_hide') == 2:
            moderation.delete_thread(request.user, thread)
            return Response({'detail': 'ok'})
        else:
            raise PermissionDenied(_("You don't have permission to delete this thread."))


class ThreadViewSet(ViewSet):
    thread = ForumThread

    def create(self, request):
        if request.user.is_anonymous():
            raise PermissionDenied(_("You need to be signed in to start threads."))

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

    @list_route(methods=['post'])
    def merge(self, request):
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
        if request.user.is_anonymous():
            raise PermissionDenied(_("You need to be signed in to start threads."))

        # list of categories that allow or contain subcategories that allow new threads
        available = []

        categories = []
        for category in Category.objects.filter(pk__in=request.user.acl['browseable_categories']).order_by('-lft'):
            add_acl(request.user, category)

            post = False
            if can_start_thread(request.user, category):
                post = {
                    'close': bool(category.acl['can_close_threads']),
                    'hide': bool(category.acl['can_hide_threads']),
                    'pin': category.acl['can_pin_threads']
                }

                available.append(category.pk)
                available.append(category.parent_id)
            elif category.pk in available:
                available.append(category.parent_id)

            categories.append({
                'id': category.pk,
                'name': category.name,
                'level': category.level - 1,
                'post': post
            })

        # list only categories that allow new threads, or contains subcategory that allows one
        cleaned_categories = []
        for category in reversed(categories):
            if category['id'] in available:
                cleaned_categories.append(category)

        if not cleaned_categories:
            raise PermissionDenied(_("No categories that allow new threads are available to you at the moment."))

        return Response(cleaned_categories)
