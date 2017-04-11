from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from misago.acl import add_acl
from misago.categories import PRIVATE_THREADS_ROOT_NAME, THREADS_ROOT_NAME
from misago.categories.models import Category
from misago.core.shortcuts import validate_slug
from misago.core.viewmodel import ViewModel as BaseViewModel
from misago.readtracker.threadstracker import make_read_aware
from misago.threads.models import Poll, Thread
from misago.threads.participants import make_participants_aware
from misago.threads.permissions import (
    allow_see_private_thread, allow_see_thread, allow_use_private_threads)
from misago.threads.serializers import PrivateThreadSerializer, ThreadSerializer
from misago.threads.subscriptions import make_subscription_aware
from misago.threads.threadtypes import trees_map


__all__ = ['ForumThread', 'PrivateThread']

BASE_RELATIONS = [
    'category',
    'poll',
    'starter',
    'starter__rank',
    'starter__ban_cache',
    'starter__online_tracker',
]


class ViewModel(BaseViewModel):
    def __init__(
            self,
            request,
            pk,
            slug=None,
            read_aware=False,
            subscription_aware=False,
            poll_votes_aware=False,
            select_for_update=False
    ):
        model = self.get_thread(request, pk, slug, select_for_update)

        model.path = self.get_thread_path(model.category)

        add_acl(request.user, model.category)
        add_acl(request.user, model)

        if read_aware:
            make_read_aware(request.user, model)
        if subscription_aware:
            make_subscription_aware(request.user, model)

        self._model = model

        try:
            self._poll = model.poll
            add_acl(request.user, self._poll)

            if poll_votes_aware:
                self._poll.make_choices_votes_aware(request.user)
        except Poll.DoesNotExist:
            self._poll = None

    @property
    def poll(self):
        return self._poll

    def get_thread(self, request, pk, slug=None, select_for_update=False):
        raise NotImplementedError(
            'Thread view model has to implement get_thread(request, pk, slug=None)'
        )

    def get_thread_path(self, category):
        thread_path = []

        if category.level:
            categories = Category.objects.filter(
                tree_id=category.tree_id, lft__lte=category.lft, rght__gte=category.rght
            ).order_by('level')
            thread_path = list(categories)
        else:
            thread_path = [category]

        thread_path[0].name = self.get_root_name()
        return thread_path

    def get_root_name(self):
        raise NotImplementedError("Thread view model has to implement get_root_name()")

    def get_frontend_context(self):
        raise NotImplementedError("Thread view model has to implement get_frontend_context()")

    def get_template_context(self):
        return {
            'thread': self._model,
            'poll': self._poll,
            'category': self._model.category,
            'breadcrumbs': self._model.path,
        }


class ForumThread(ViewModel):
    def get_thread(self, request, pk, slug=None, select_for_update=False):
        if select_for_update:
            queryset = Thread.objects.select_for_update()
        else:
            queryset = Thread.objects.select_related(*BASE_RELATIONS)

        thread = get_object_or_404(
            queryset,
            pk=pk,
            category__tree_id=trees_map.get_tree_id_for_root(THREADS_ROOT_NAME),
        )

        allow_see_thread(request.user, thread)
        if slug:
            validate_slug(thread, slug)
        return thread

    def get_root_name(self):
        return _("Threads")

    def get_frontend_context(self):
        return ThreadSerializer(self._model).data


class PrivateThread(ViewModel):
    def get_thread(self, request, pk, slug=None, select_for_update=False):
        allow_use_private_threads(request.user)

        if select_for_update:
            queryset = Thread.objects.select_for_update()
        else:
            queryset = Thread.objects.select_related(*BASE_RELATIONS)

        thread = get_object_or_404(
            queryset,
            pk=pk,
            category__tree_id=trees_map.get_tree_id_for_root(PRIVATE_THREADS_ROOT_NAME),
        )

        make_participants_aware(request.user, thread)
        allow_see_private_thread(request.user, thread)

        if slug:
            validate_slug(thread, slug)

        return thread

    def get_root_name(self):
        return _("Private threads")

    def get_frontend_context(self):
        return PrivateThreadSerializer(self._model).data
