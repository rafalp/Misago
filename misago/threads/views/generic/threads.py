from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy, ugettext as _

from misago.core.shortcuts import paginate

from misago.threads.views.generic.base import ViewBase


__all__ = ['OrderThreadsMixin', 'ThreadsView']


class OrderThreadsMixin(object):
    order_by = (
        ('recently-replied', ugettext_lazy("Recently replied")),
        ('last-replied', ugettext_lazy("Last replied")),
        ('most-replied', ugettext_lazy("Most replied")),
        ('least-replied', ugettext_lazy("Least replied")),
        ('newest', ugettext_lazy("Newest")),
        ('oldest', ugettext_lazy("Oldest")),
    )

    def get_ordering(self, kwargs):
        if kwargs.get('sort') in [o[0] for o in self.order_by]:
            return kwargs.get('sort')
        else:
            return self.order_by[0][0]

    def is_ordering_default(self, order_by):
        return self.order_by[0][0] == order_by

    def get_ordering_name(self, order_by):
        for ordering in self.order_by:
            if ordering[0] == order_by:
                return ordering[1]

    def get_orderings_dicts(self, exclude_ordering, links_params):
        url_kwargs = links_params.copy()
        dicts = []

        for ordering in self.order_by:
            if not dicts:
                url_kwargs.pop('sort', None)
            else:
                url_kwargs['sort'] = ordering[0]

            if ordering[0] != exclude_ordering:
                dicts.append({
                    'url': reverse(self.link_name, kwargs=url_kwargs),
                    'name': ordering[1],
                })

        return dicts


class ThreadsView(ViewBase):
    def get_threads(self, request, kwargs):
        queryset = self.get_threads_queryset(request, forum)
        queryset = threads_qs.order_by('-last_post_id')

        page = paginate(threads_qs, kwargs.get('page', 0), 30, 10)
        threads = [thread for thread in page.object_list]

        return page, threads

    def get_threads_queryset(self, request):
        return forum.thread_set.all().order_by('-last_post_id')

    def add_threads_reads(self, request, threads):
        for thread in threads:
            thread.is_new = False

        import random
        for thread in threads:
            thread.is_new = random.choice((True, False))
