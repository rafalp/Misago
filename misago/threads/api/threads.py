from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.utils.translation import gettext as _

from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from misago.acl import add_acl
from misago.categories.models import CATEGORIES_TREE_ID, Category
from misago.categories.permissions import (
    allow_see_category, allow_browse_category)
from misago.core.shortcuts import get_int_or_404, get_object_or_404
from misago.readtracker.categoriestracker import read_category
from misago.users.rest_permissions import IsAuthenticatedOrReadOnly

from misago.threads.api.threadendpoints.list import threads_list_endpoint
from misago.threads.api.threadendpoints.patch import thread_patch_endpoint
from misago.threads.models import Thread, Subscription
from misago.threads.moderation import threads as moderation
from misago.threads.permissions.threads import allow_see_thread
from misago.threads.serializers import ThreadSerializer
from misago.threads.subscriptions import make_subscription_aware


class ThreadViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    parser_classes=(JSONParser, )

    TREE_ID = CATEGORIES_TREE_ID

    def validate_thread_visible(self, user, thread):
        allow_see_thread(user, thread)

    def get_thread(self, user, thread_id):
        thread = get_object_or_404(Thread.objects.select_related('category'),
            id=get_int_or_404(thread_id),
            category__tree_id=self.TREE_ID,
        )

        add_acl(user, thread.category)
        add_acl(user, thread)

        self.validate_thread_visible(user, thread)

        return thread

    def list(self, request):
        return threads_list_endpoint(request)

    def retrieve(self, request, pk=None):
        thread = self.get_thread(request.user, pk)
        make_subscription_aware(request.user, thread)
        return Response(ThreadSerializer(thread).data)

    def partial_update(self, request, pk=None):
        thread = self.get_thread(request.user, pk)
        return thread_patch_endpoint.dispatch(request, thread)

    def destroy(self, request, pk=None):
        thread = self.get_thread(request.user, pk)

        if thread.acl.get('can_hide') == 2:
            moderation.delete_thread(request.user, thread)
            return Response({'detail': 'ok'})
        else:
            raise PermissionDenied(
                _("You don't have permission to delete this thread."))

    @list_route(methods=['post'])
    def read(self, request):
        if request.query_params.get('category'):
            category_id = get_int_or_404(request.query_params.get('category'))
            category = get_object_or_404(Category.objects,
                id=category_id,
                tree_id=self.TREE_ID,
            )

            allow_see_category(request.user, category)
            allow_browse_category(request.user, category)
        else:
            category = Category.objects.root_category()

        read_category(request.user, category)
        return Response({'detail': 'ok'})
