from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _

from misago.acl import add_acl
from misago.categories.models import THREADS_ROOT_NAME, Category
from misago.core.shortcuts import validate_slug
from misago.readtracker.threadstracker import make_read_aware

from ..models import Thread
from ..permissions.threads import allow_see_thread
from ..serializers import ThreadSerializer
from ..subscriptions import make_subscription_aware
from ..threadtypes import trees_map


BASE_RELATIONS = ('category', 'starter', 'starter__rank', 'starter__ban_cache', 'starter__online_tracker')


class ViewModel(object):
    def __init__(self, request, pk, slug=None, read_aware=False, subscription_aware=False, select_for_update=False):
        model = self.get_thread(request, pk, slug, select_for_update)

        model.path = self.get_thread_path(model.category)

        add_acl(request.user, model.category)
        add_acl(request.user, model)

        if read_aware:
            make_read_aware(request.user, model)
        if subscription_aware:
            make_subscription_aware(request.user, model)

        self._model = model
        self._category = model.category
        self._path = model.path

    @property
    def model(self):
        return self._model

    @property
    def category(self):
        return self._category

    @property
    def path(self):
        return self._path

    def get_thread(self, request, pk, slug=None, select_for_update=False):
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
        return ThreadSerializer(self._model).data

    def get_template_context(self):
        return {
            'thread': self._model,
            'category': self._category,
            'breadcrumbs': self._path
        }


class ForumThread(ViewModel):
    def get_thread(self, request, pk, slug=None, select_for_update=False):
        if select_for_update:
            queryset = Thread.objects.select_for_update().select_related('category')
        else:
            queryset = Thread.objects.select_related(*BASE_RELATIONS)

        thread = get_object_or_404(
            queryset,
            pk=pk,
            category__tree_id=trees_map.get_tree_id_for_root(THREADS_ROOT_NAME)
        )

        allow_see_thread(request.user, thread)
        if slug:
            validate_slug(thread, slug)
        return thread

    def get_root_name(self):
        return _("Threads")
