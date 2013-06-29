from itertools import chain
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from misago.apps.threadtype.list import ThreadsListBaseView, ThreadsListModeration
from misago.conf import settings
from misago.models import Forum, Thread
from misago.readstrackers import ThreadsTracker
from misago.utils.pagination import make_pagination
from misago.apps.threads.mixins import TypeMixin

class ThreadsListView(ThreadsListBaseView, ThreadsListModeration, TypeMixin):
    def fetch_forum(self):
        self.forum = Forum.objects.get(pk=self.kwargs.get('forum'), type='forum')

    def threads_queryset(self):
        announcements = self.request.acl.threads.filter_threads(self.request, self.forum, self.forum.thread_set).filter(weight=2).order_by('-pk')
        threads = self.request.acl.threads.filter_threads(self.request, self.forum, self.forum.thread_set).filter(weight__lt=2).order_by('-weight', '-last')

        # Dont display threads by ignored users (unless they are important)
        if self.request.user.is_authenticated():
            ignored_users = self.request.user.ignored_users()
            if ignored_users:
                threads = threads.extra(where=["`threads_thread`.`start_poster_id` IS NULL OR `threads_thread`.`start_poster_id` NOT IN (%s)" % ','.join([str(i) for i in ignored_users])])

        # Add in first and last poster
        if settings.avatars_on_threads_list:
            announcements = announcements.prefetch_related('start_poster', 'last_poster')
            threads = threads.prefetch_related('start_poster', 'last_poster')

        return announcements, threads

    def fetch_threads(self):
        qs_announcements, qs_threads = self.threads_queryset()
        self.count = qs_threads.count()

        try:
            self.pagination = make_pagination(self.kwargs.get('page', 0), self.count, settings.threads_per_page)
        except Http404:
            return self.threads_list_redirect()

        tracker_forum = ThreadsTracker(self.request, self.forum)
        for thread in list(chain(qs_announcements, qs_threads[self.pagination['start']:self.pagination['stop']])):
            thread.is_read = tracker_forum.is_read(thread)
            self.threads.append(thread)

    def threads_actions(self):
        acl = self.request.acl.threads.get_role(self.forum)
        actions = []
        try:
            if acl['can_approve']:
                actions.append(('accept', _('Accept threads')))
            if acl['can_pin_threads'] == 2:
                actions.append(('annouce', _('Change to announcements')))
            if acl['can_pin_threads'] > 0:
                actions.append(('sticky', _('Change to sticky threads')))
            if acl['can_pin_threads'] > 0:
                actions.append(('normal', _('Change to standard thread')))
            if acl['can_move_threads_posts']:
                actions.append(('move', _('Move threads')))
                actions.append(('merge', _('Merge threads')))
            if acl['can_close_threads']:
                actions.append(('open', _('Open threads')))
                actions.append(('close', _('Close threads')))
            if acl['can_delete_threads']:
                actions.append(('undelete', _('Restore threads')))
                actions.append(('soft', _('Hide threads')))
            if acl['can_delete_threads'] == 2:
                actions.append(('hard', _('Delete threads')))
        except KeyError:
            pass
        return actions