from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy, ugettext as _

from misago.core.shortcuts import paginate
from misago.forums.lists import get_forums_list, get_forum_path

from misago.threads.posting import (PostingInterrupt, EditorFormset,
                                    START, REPLY, EDIT)
from misago.threads.models import ANNOUNCEMENT, Thread
from misago.threads.views.generic.base import ViewBase


__all__ = ['OrderThreadsMixin', 'ThreadsView', 'ForumView']


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

        threads_qs = queryset.filter(weight__lt=ANNOUNCEMENT)
        threads_qs = threads_qs.order_by('-weight', '-last_post_id')

        page = paginate(threads_qs, kwargs.get('page', 0), 30, 10)
        threads = []

        for announcement in queryset.filter(weight=ANNOUNCEMENT):
            threads.append(announcement)
        for thread in page.object_list:
            threads.append(thread)

        for thread in threads:
            thread.forum = forum

        return page, threads

    def get_threads_queryset(self, request):
        return forum.thread_set.all().order_by('-last_post_id')

    def add_threads_reads(self, request, threads):
        for thread in threads:
            thread.is_new = False

        import random
        for thread in threads:
            thread.is_new = random.choice((True, False))


class ForumView(OrderThreadsMixin, ThreadsView):
    """
    Basic view for threads lists
    """
    template = 'list.html'

    def get_threads(self, request, forum, kwargs, order_by=None, limit=None):
        queryset = self.get_threads_queryset(request, forum)
        queryset = self.filter_all_querysets(request, forum, queryset)

        announcements_qs = queryset.filter(weight=ANNOUNCEMENT)
        threads_qs = queryset.filter(weight__lt=ANNOUNCEMENT)

        announcements_qs = self.filter_announcements_queryset(
            request, forum, announcements_qs)
        threads_qs = self.filter_threads_queryset(request, forum, threads_qs)

        threads_qs, announcements_qs = self.order_querysets(
            order_by, threads_qs, announcements_qs)

        page = paginate(threads_qs, kwargs.get('page', 0), 20, 10)
        threads = []

        for announcement in announcements_qs:
            threads.append(announcement)
        for thread in page.object_list:
            threads.append(thread)

        for thread in threads:
            thread.forum = forum

        return page, threads

    def order_querysets(self, order_by, threads, announcements):
        if order_by == 'recently-replied':
            threads = threads.order_by('-weight', '-last_post')
            announcements = announcements.order_by('-last_post')
        if order_by == 'last-replied':
            threads = threads.order_by('weight', 'last_post')
            announcements = announcements.order_by('last_post')
        if order_by == 'most-replied':
            threads = threads.order_by('-weight', '-replies')
            announcements = announcements.order_by('-replies')
        if order_by == 'least-replied':
            threads = threads.order_by('weight', 'replies')
            announcements = announcements.order_by('replies')
        if order_by == 'newest':
            threads = threads.order_by('-weight', '-id')
            announcements = announcements.order_by('-id')
        if order_by == 'oldest':
            threads = threads.order_by('weight', 'id')
            announcements = announcements.order_by('id')

        return threads, announcements

    def filter_all_querysets(self, request, forum, queryset):
        if request.user.is_authenticated():
            condition_author = Q(starter_id=request.user.id)

            can_mod = forum.acl['can_review_moderated_content']
            can_hide = forum.acl['can_hide_threads']

            if not can_mod and not can_hide:
                condition = Q(is_moderated=False) & Q(is_hidden=False)
                queryset = queryset.filter(condition_author | condition)
            elif not can_mod:
                condition = Q(is_moderated=False)
                queryset = queryset.filter(condition_author | condition)
            elif not can_hide:
                condition = Q(is_hidden=False)
                queryset = queryset.filter(condition_author | condition)
        else:
            if not forum.acl['can_review_moderated_content']:
                queryset = queryset.filter(is_moderated=False)
            if not forum.acl['can_hide_threads']:
                queryset = queryset.filter(is_hidden=False)

        return queryset

    def filter_threads_queryset(self, request, forum, queryset):
        if forum.acl['can_see_own_threads']:
            if request.user.is_authenticated():
                queryset = queryset.filter(starter_id=request.user.id)
            else:
                queryset = queryset.filter(starter_id=0)

        return queryset

    def filter_announcements_queryset(self, request, forum, queryset):
        return queryset

    def get_threads_queryset(self, request, forum):
        return forum.thread_set.all().order_by('-last_post_id')

    def get_default_link_params(self, forum):
        message = "forum views have to define get_default_link_params"
        raise NotImplementedError()

    def dispatch(self, request, *args, **kwargs):
        forum = self.get_forum(request, **kwargs)
        links_params = self.get_default_link_params(forum)

        if forum.lft + 1 < forum.rght:
            forum.subforums = get_forums_list(request.user, forum)
        else:
            forum.subforums = []

        order_by = self.get_ordering(kwargs)
        if self.is_ordering_default(kwargs.get('sort')):
            kwargs.pop('sort')
            return redirect('misago:forum', **kwargs)
        elif not self.is_ordering_default(order_by):
            links_params['sort'] = order_by

        page, threads = self.get_threads(request, forum, kwargs, order_by)
        self.add_threads_reads(request, threads)

        return self.render(request, {
            'forum': forum,
            'path': get_forum_path(forum),
            'page': page,
            'paginator': page.paginator,
            'threads': threads,
            'link_name': self.link_name,
            'links_params': links_params,
            'order_name': self.get_ordering_name(order_by),
            'order_by': self.get_orderings_dicts(order_by, links_params),
        })
