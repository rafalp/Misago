from django.http import Http404
from django.shortcuts import get_object_or_404

from misago.acl import add_acl
from misago.categories.models import CATEGORIES_TREE_ID

from misago.threads.permissions.threads import allow_see_thread
from misago.threads.models import Thread


class ThreadMixin(object):
    def get_thread(self, request, pk):
        thread = get_object_or_404(Thread.objects.select_related('category', 'starter'), pk=pk)
        if thread.category.tree_id != CATEGORIES_TREE_ID:
            raise Http404()

        add_acl(request.user, thread)
        add_acl(request.user, thread.category)

        allow_see_thread(request.user, thread)

        return thread


class PrivateThreadMixin(object):
    pass
