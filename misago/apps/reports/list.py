from itertools import chain
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from misago.apps.threadtype.list import ThreadsListBaseView, ThreadsListModeration
from misago.messages import Message
from misago.models import Forum, Thread
from misago.readstrackers import ThreadsTracker
from misago.utils.pagination import make_pagination
from misago.apps.reports.mixins import TypeMixin

class ThreadsListView(ThreadsListBaseView, ThreadsListModeration, TypeMixin):
    def fetch_forum(self):
        self.forum = Forum.objects.get(special='reports')

    def threads_queryset(self):
        announcements = self.forum.thread_set.filter(weight=2).order_by('-pk')
        threads = self.forum.thread_set.filter(weight__lt=2).order_by('-weight', '-last')

        # Add in first and last poster
        if self.request.settings.avatars_on_threads_list:
            announcements = announcements.prefetch_related('start_poster', 'last_poster')
            threads = threads.prefetch_related('start_poster', 'last_poster')

        return announcements, threads

    def fetch_threads(self):
        qs_announcements, qs_threads = self.threads_queryset()
        self.count = qs_threads.count()

        try:
            self.pagination = make_pagination(self.kwargs.get('page', 0), self.count, self.request.settings.threads_per_page)
        except Http404:
            return self.threads_list_redirect()

        tracker_forum = ThreadsTracker(self.request, self.forum)
        unresolved_count = 0
        for thread in list(chain(qs_announcements, qs_threads[self.pagination['start']:self.pagination['stop']])):
            if thread.weight == 2:
                unresolved_count += 1
            thread.is_read = tracker_forum.is_read(thread)
            self.threads.append(thread)

        if int(self.request.monitor['reported_posts']) != unresolved_count:
            self.request.monitor['reported_posts'] = unresolved_count

    def threads_actions(self):
        acl = self.request.acl.threads.get_role(self.forum)
        actions = []
        try:
            actions.append(('sticky', _('Change to resolved')))
            actions.append(('normal', _('Change to bogus')))
            if acl['can_delete_threads']:
                actions.append(('undelete', _('Restore threads')))
                actions.append(('soft', _('Hide threads')))
            if acl['can_delete_threads'] == 2:
                actions.append(('hard', _('Delete threads')))
        except KeyError:
            pass
        return actions

    def action_sticky(self, ids):
        if self._action_sticky(ids):
            self.request.messages.set_flash(Message(_('Selected reports were set as resolved.')), 'success', 'threads')
        else:
            self.request.messages.set_flash(Message(_('No reports were set as resolved.')), 'info', 'threads')

    def action_normal(self, ids):
        if self._action_normal(ids):
            self.request.messages.set_flash(Message(_('Selected reports were set as bogus.')), 'success', 'threads')
        else:
            self.request.messages.set_flash(Message(_('No reports were set as bogus.')), 'info', 'threads')

    def action_undelete(self, ids):
        if self._action_undelete(ids):
            self.request.messages.set_flash(Message(_('Selected reports have been restored.')), 'success', 'threads')
        else:
            self.request.messages.set_flash(Message(_('No reports were restored.')), 'info', 'threads')

    def action_soft(self, ids):
        if self._action_soft(ids):
            self.request.messages.set_flash(Message(_('Selected reports have been hidden.')), 'success', 'threads')
        else:
            self.request.messages.set_flash(Message(_('No reports were hidden.')), 'info', 'threads')

    def action_hard(self, ids):
        if self._action_hard(ids):
            self.request.messages.set_flash(Message(_('Selected reports have been deleted.')), 'success', 'threads')
        else:
            self.request.messages.set_flash(Message(_('No reports were deleted.')), 'info', 'threads')
