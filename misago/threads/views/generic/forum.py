from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy, ugettext as _, ungettext

from misago.core.shortcuts import paginate
from misago.forums.lists import get_forums_list, get_forum_path

from misago.threads import moderation
from misago.threads.models import ANNOUNCEMENT, Thread, Label
from misago.threads.permissions import exclude_invisible_threads
from misago.threads.views.generic.threads import (Actions, Sorting, Threads,
                                                  ThreadsView)


__all__ = ['ForumFiltering', 'ForumThreads', 'ForumView']


class ForumActions(Actions):
    def get_available_actions(self, kwargs):
        forum = kwargs['forum']

        actions = []

        if forum.acl['can_change_threads_weight'] == 2:
            actions.append({
                'action': 'announce',
                'icon': 'star',
                'name': _("Change to announcements")
            })
        if forum.acl['can_change_threads_weight']:
            actions.append({
                'action': 'pin',
                'icon': 'bookmark',
                'name': _("Change to pinned")
            })
            actions.append({
                'action': 'reset',
                'icon': 'circle',
                'name': _("Reset weight")
            })
        return actions

    def action_announce(self, request, threads):
        changed_threads = 0
        for thread in threads:
            if moderation.announce_thread(request.user, thread):
                changed_threads += 1

        if changed_threads:
            message = ungettext(
                '%(changed)d thread was changed to announcement.',
                '%(changed)d threads were changed to announcements.',
            changed_threads)
            messages.success(request, message % {'changed': changed_threads})
        else:
            message = ("No threads were changed to announcements.")
            messages.info(request, message)

    def action_pin(self, request, threads):
        changed_threads = 0
        for thread in threads:
            if moderation.pin_thread(request.user, thread):
                changed_threads += 1

        if changed_threads:
            message = ungettext(
                '%(changed)d thread was pinned.',
                '%(changed)d threads were pinned.',
            changed_threads)
            messages.success(request, message % {'changed': changed_threads})
        else:
            message = ("No threads were pinned.")
            messages.info(request, message)

    def action_reset(self, request, threads):
        changed_threads = 0
        for thread in threads:
            if moderation.reset_thread(request.user, thread):
                changed_threads += 1

        if changed_threads:
            message = ungettext(
                '%(changed)d thread weight was reset.',
                '%(changed)d threads weight was reset.',
            changed_threads)
            messages.success(request, message % {'changed': changed_threads})
        else:
            message = ("No threads weight was reset.")
            messages.info(request, message)


class ForumFiltering(object):
    def __init__(self, forum, link_name, link_params):
        self.forum = forum
        self.link_name = link_name
        self.link_params = link_params.copy()

        self.filters = self.get_available_filters()

    def get_available_filters(self):
        filters = []

        if self.forum.acl['can_see_all_threads']:
            filters.append({
                'type': 'my-threads',
                'name': _("My threads"),
                'is_label': False,
            })

        if self.forum.acl['can_see_reports']:
            filters.append({
                'type': 'reported',
                'name': _("With reported posts"),
                'is_label': False,
            })

        if self.forum.acl['can_review_moderated_content']:
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

        for label in self.forum.labels:
            filters.append({
                'type': label.slug,
                'name': label.name,
                'is_label': True,
                'css_class': label.css_class,
            })

        return filters

    def clean_kwargs(self, kwargs):
        show = kwargs.get('show')
        if show:
            available_filters = [method['type'] for method in self.filters]
            if show in available_filters:
                self.show = show
            else:
                kwargs.pop('show')
        else:
            self.show = None

        return kwargs

    def filter(self, threads):
        threads.filter(self.show)

    def get_filtering_dics(self):
        try:
            return self._dicts
        except AttributeError:
            self._dicts = self.create_dicts()
            return self._dicts

    def create_dicts(self):
        dicts = []

        if self.forum.acl['can_see_all_threads']:
            default_name = _("All threads")
        else:
            default_name = _("Your threads")

        self.link_params.pop('show', None)
        dicts.append({
            'type': None,
            'url': reverse(self.link_name, kwargs=self.link_params),
            'name': default_name,
            'is_label': False,
        })

        for filtering in self.filters:
            self.link_params['show'] = filtering['type']
            filtering['url'] = reverse(self.link_name, kwargs=self.link_params)
            dicts.append(filtering)

        return dicts

    @property
    def is_active(self):
        return bool(self.show)

    @property
    def current(self):
        try:
            return self._current
        except AttributeError:
            for filtering in self.get_filtering_dics():
                if filtering['type'] == self.show:
                    self._current = filtering
                    return filtering

    def choices(self):
        if self.show:
            choices = []
            for filtering in self.get_filtering_dics():
                if filtering['type'] != self.show:
                    choices.append(filtering)
            return choices
        else:
            return self.get_filtering_dics()[1:]


class ForumThreads(Threads):
    def __init__(self, user, forum):
        self.user = user
        self.forum = forum

        self.filter_by = None
        self.sort_by = ('-weight', '-last_post_on')

    def filter(self, filter_by):
        self.filter_by = filter_by

    def sort(self, sort_by):
        if sort_by[0] == '-':
            weight = '-weight'
        else:
            weight = 'weight'
        self.sort_by = (weight, sort_by)

    def list(self, page=0):
        queryset = self.get_queryset()
        queryset = queryset.order_by(*self.sort_by)

        announcements_qs = queryset.filter(weight=ANNOUNCEMENT)
        threads_qs = queryset.filter(weight__lt=ANNOUNCEMENT)

        self._page = paginate(threads_qs, page, 20, 10)
        self._paginator = self._page.paginator

        threads = []
        for announcement in announcements_qs:
            threads.append(announcement)
        for thread in self._page.object_list:
            threads.append(thread)

        for thread in threads:
            thread.forum = self.forum

        self.label_threads(threads, self.forum.labels)
        self.make_threads_read_aware(threads)

        return threads

    def filter_threads(self, queryset):
        if self.filter_by == 'my-threads':
            return queryset.filter(starter_id=self.user.id)
        else:
            if self.forum.acl['can_see_own_threads']:
                if self.user.is_authenticated():
                    queryset = queryset.filter(starter_id=self.user.id)
                else:
                    queryset = queryset.filter(starter_id=0)
            if self.filter_by == 'reported':
                return queryset.filter(has_reported_posts=True)
            elif self.filter_by == 'moderated-threads':
                return queryset.filter(is_moderated=True)
            elif self.filter_by == 'moderated-posts':
                return queryset.filter(has_moderated_posts=True)
            else:
                for label in self.forum.labels:
                    if label.slug == self.filter_by:
                        return queryset.filter(label_id=label.pk)
                else:
                    return queryset

    def get_queryset(self):
        queryset = exclude_invisible_threads(
            self.user, self.forum, self.forum.thread_set)
        return self.filter_threads(queryset)

    error_message = ("threads list has to be loaded via call to list() before "
                     "pagination data will be available")

    @property
    def paginator(self):
        try:
            return self._paginator
        except AttributeError:
            raise AttributeError(self.error_message)

    @property
    def page(self):
        try:
            return self._page
        except AttributeError:
            raise AttributeError(self.error_message)


class ForumView(ThreadsView):
    """
    Basic view for forum threads lists
    """
    template = 'misago/threads/forum.html'

    Threads = ForumThreads
    Sorting = Sorting
    Filtering = ForumFiltering
    Actions = ForumActions

    def dispatch(self, request, *args, **kwargs):
        forum = self.get_forum(request, **kwargs)
        forum.labels = Label.objects.get_forum_labels(forum)

        if forum.lft + 1 < forum.rght:
            forum.subforums = get_forums_list(request.user, forum)
        else:
            forum.subforums = []

        page_number = kwargs.pop('page', None)
        cleaned_kwargs = self.clean_kwargs(request, kwargs)

        sorting = self.Sorting(self.link_name, cleaned_kwargs)
        cleaned_kwargs = sorting.clean_kwargs(cleaned_kwargs)

        filtering = self.Filtering(forum, self.link_name, cleaned_kwargs)
        cleaned_kwargs = filtering.clean_kwargs(cleaned_kwargs)

        if cleaned_kwargs != kwargs:
            return redirect('misago:forum', **cleaned_kwargs)

        threads = self.Threads(request.user, forum)
        sorting.sort(threads)
        filtering.filter(threads)

        actions = self.Actions(user=request.user, forum=forum)
        if request.method == 'POST':
            # see if we can delegate anything to actions manager
            response = actions.handle_post(request, threads.get_queryset())
            if response:
                return response

        return self.render(request, {
            'link_name': self.link_name,
            'links_params': cleaned_kwargs,

            'forum': forum,
            'path': get_forum_path(forum),

            'threads': threads.list(page_number),
            'page': threads.page,
            'paginator': threads.paginator,

            'list_actions': actions.get_list(),
            'selected_threads': actions.get_selected_ids(),

            'sorting': sorting,
            'filtering': filtering,
        })
