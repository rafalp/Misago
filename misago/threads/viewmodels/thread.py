from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _

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

        thread.path = self.get_thread_path(thread.category)

        add_acl(request.user, thread.category)
        add_acl(request.user, thread)

        make_read_aware(request.user, thread)
        make_subscription_aware(request.user, thread)

        self.thread = thread
        self.category = thread.category
        self.path = thread.path

    def get_thread(self, request, pk, slug=None):
        raise NotImplementedError('Thread view model has to implement get_thread(request, pk, slug=None)')

    def get_thread_path(self, category):
        thread_path = []

        if category.level:
            categories = Category.objects.filter(
                tree_id=category.tree_id,
                lft__lte=category.lft,
                rght__gte=category.rght
            ).order_by('level')
            thread_path = list(categories)
        else:
            thread_path = [category]

        thread_path[0].name = self.get_root_name()
        return thread_path

    def get_root_name(self):
        raise NotImplementedError('Thread view model has to implement get_root_name()')

    def get_frontend_context(self):
        return {
            'THREAD': ThreadSerializer(self.thread).data
        }

    def get_template_context(self):
        return {
            'thread': self.thread,
            'category': self.category,
            'breadcrumbs': self.path
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

    def get_root_name(self):
        return _("Threads")
