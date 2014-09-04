from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy, ugettext as _

from misago.core.shortcuts import paginate
from misago.forums.lists import get_forums_list, get_forum_path

from misago.threads.posting import (PostingInterrupt, EditorFormset,
                                    START, REPLY, EDIT)
from misago.threads.models import ANNOUNCEMENT, Thread, Prefix
from misago.threads.views.generic.threads import OrderThreadsMixin, ThreadsView


__all__ = ['FilterThreadsMixin', 'ForumView']


class FilterThreadsMixin(object):
    def get_filter_dict(self, filters, filter_by):
        if filters:
            if filter_by:
                for filtering in filters:
                    if filtering['type'] == filter_by:
                        return filtering
            else:
                return {
                    'name': _("All threads"),
                    'is_label': False,
                }
        else:
            return None

    def get_filters_dicts(self, filters, exclude_filter, links_params):
        url_kwargs = links_params.copy()
        dicts = []

        if exclude_filter:
            url_kwargs.pop('show', None)
            dicts.append({
                'url': reverse(self.link_name, kwargs=url_kwargs),
                'name': _("All threads"),
                'is_label': False,
            })

        for filtering in filters:
            if filtering['type'] != exclude_filter:
                filter_dict = filtering.copy()
                url_kwargs['show'] = filtering['type']
                filter_dict['url'] = reverse(self.link_name, kwargs=url_kwargs)
                dicts.append(filter_dict)

        return dicts

    def get_available_filters(self, request, forum):
        filters = []
        if request.user.is_authenticated():
            if forum.acl['can_see_all_threads']:
                filters.append({
                    'type': 'my-threads',
                    'name': _("My threads"),
                    'is_label': False,
                })
            if forum.acl['can_see_reports']:
                filters.append({
                    'type': 'reported',
                    'name': _("With reported posts"),
                    'is_label': False,
                })
            if forum.acl['can_review_moderated_content']:
                filters.extend(({
                    'type': 'moderated-threads',
                    'name': _("Moderated threads"),
                    'is_label': False,
                },
                {
                    'type': 'moderated-posts',
                    'name': _("With moderated posts"),
                    'is_label': False,
                }))
        for prefix in forum.prefixes:
            filters.append({
                'type': prefix.slug,
                'name': prefix.name,
                'is_label': True,
                'css_class': prefix.css_class,
            })
        return filters

    def set_custom_filter(self, request, forum, queryset, filter_by):
        if filter_by == 'my-threads':
            return queryset.filter(starter_id=request.user.id)
        elif filter_by == 'reported':
            return queryset.filter(has_reported_posts=True)
        elif filter_by == 'moderated-threads':
            return queryset.filter(is_moderated=True)
        elif filter_by == 'moderated-posts':
            return queryset.filter(has_moderated_posts=True)
        else:
            for prefix in forum.prefixes:
                if prefix.slug == filter_by:
                    return queryset.filter(prefix_id=prefix.pk)
            else:
                return queryset


class ForumView(FilterThreadsMixin, OrderThreadsMixin, ThreadsView):
    """
    Basic view for threads lists
    """
    template = 'misago/threads/forum.html'

    def get_threads(self, request, forum, kwargs,
                    order_by=None, filter_by=None):
        org_queryset = self.get_threads_queryset(request, forum)
        queryset = self.filter_all_querysets(request, forum, org_queryset)
        queryset = self.set_custom_filter(request, forum, queryset, filter_by)

        announcements_qs = queryset.filter(weight=ANNOUNCEMENT)
        threads_qs = queryset.filter(weight__lt=ANNOUNCEMENT)

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

    def set_custom_filter(self, request, forum, queryset, filter_by):
        return queryset

    def get_threads_queryset(self, request, forum):
        return forum.thread_set.all().order_by('-last_post_id')

    def get_default_link_params(self, forum):
        message = "forum views have to define get_default_link_params"
        raise NotImplementedError(message)

    def dispatch(self, request, *args, **kwargs):
        forum = self.get_forum(request, **kwargs)
        forum.prefixes = Prefix.objects.get_forum_prefixes(forum)
        links_params = self.get_default_link_params(forum)

        if forum.lft + 1 < forum.rght:
            forum.subforums = get_forums_list(request.user, forum)
        else:
            forum.subforums = []

        if request.user.is_anonymous():
            if kwargs.get('sort') or kwargs.get('show'):
                """we don't allow sort/filter for guests"""
                kwargs.pop('sort', None)
                kwargs.pop('show', None)
                return redirect('misago:forum', **kwargs)

        order_by = self.get_ordering(kwargs)
        if self.is_ordering_default(kwargs.get('sort')):
            kwargs.pop('sort')
            return redirect('misago:forum', **kwargs)
        elif not self.is_ordering_default(order_by):
            links_params['sort'] = order_by

        available_filters = self.get_available_filters(request, forum)
        if available_filters and kwargs.get('show'):
            filter_methods = [f['type'] for f in available_filters]
            if kwargs.get('show') not in filter_methods:
                kwargs.pop('show')
                return redirect('misago:forum', **kwargs)
            else:
                filter_by = kwargs.get('show')
                links_params['show'] = filter_by
        else:
            filter_by = None

        page, threads = self.get_threads(
            request, forum, kwargs, order_by, filter_by)
        self.add_threads_reads(request, threads)

        return self.render(request, {
            'forum': forum,
            'path': get_forum_path(forum),
            'page': page,
            'paginator': page.paginator,
            'threads': threads,
            'link_name': self.link_name,
            'links_params': links_params,
            'is_filtering': bool(filter_by),
            'filter_by': self.get_filter_dict(available_filters, filter_by),
            'filters': self.get_filters_dicts(
                available_filters, filter_by, links_params),
            'order_name': self.get_ordering_name(order_by),
            'order_by': self.get_orderings_dicts(order_by, links_params),
        })
