from django.shortcuts import get_object_or_404

from misago.acl import add_acl
from misago.categories.models import Category
from misago.core.shortcuts import validate_slug
from misago.readtracker.threadstracker import make_read_aware

from misago.threads.models import Thread
from misago.threads.permissions.threads import allow_see_thread
from misago.threads.serializers import ThreadSerializer
from misago.threads.subscriptions import make_subscription_aware


BASE_QUERYSET = Thread.objects.select_related(
    'category', 'starter', 'starter__rank', 'starter__ban_cache', 'starter__online_tracker')


class ViewModel(object):
    def __init__(self, request, slug, pk):
        thread = self.get_thread(request, pk, slug)

        add_acl(request.user, thread.category)
        add_acl(request.user, thread)

        make_read_aware(request.user, thread)
        make_subscription_aware(request.user, thread)

        self.thread = thread
        self.category = thread.category

    def get_thread(self, request, pk, slug=None):
        raise NotImplementedError('Thread view model has to implement get_Thread(request, pk, slug=None)')

    def get_frontend_context(self):
        return {
            'THREAD': ThreadSerializer(self.thread).data
        }

    def get_template_context(self):
        return {
            'thread': self.thread,
            'category': self.category
        }


class ForumThread(ViewModel):
    def get_thread(self, request, pk, slug=None):
        thread = get_object_or_404(
            BASE_QUERYSET,
            pk=pk,
            category__tree_id=Category.objects.root_category().tree_id,
        )

        allow_see_thread(request.user, thread)
        if slug:
            validate_slug(thread, slug)
        return thread
