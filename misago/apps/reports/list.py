from itertools import chain
from django.core.urlresolvers import reverse
from django.db.models import F
from django.http import Http404
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from misago.apps.threadtype.list import ThreadsListBaseView, ThreadsListModeration
from misago.conf import settings
from misago.messages import Message
from misago.models import Forum, Thread, Post
from misago.monitor import monitor, UpdatingMonitor
from misago.readstrackers import ThreadsTracker
from misago.utils.pagination import make_pagination
from misago.apps.reports.mixins import TypeMixin

class ThreadsListView(ThreadsListBaseView, ThreadsListModeration, TypeMixin):
    def fetch_forum(self):
        self.forum = Forum.objects.get(special='reports')

    def threads_queryset(self):
        announcements = self.forum.thread_set.filter(weight=2).prefetch_related('report_for').order_by('-pk')
        threads = self.forum.thread_set.filter(weight__lt=2).prefetch_related('report_for').order_by('-weight', '-last')

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
        unresolved_count = 0
        for thread in list(chain(qs_announcements, qs_threads[self.pagination['start']:self.pagination['stop']])):
            thread.original_weight = thread.weight
            if thread.weight == 2:
                unresolved_count += 1
            thread.is_read = tracker_forum.is_read(thread)
            thread.report_forum = None
            if thread.report_for_id:
                thread.report_forum = Forum.objects.forums_tree.get(thread.report_for.forum_id)
            self.threads.append(thread)

        if monitor['reported_posts'] != unresolved_count:
            with UpdatingMonitor() as cm:
                monitor['reported_posts'] = unresolved_count

    def threads_actions(self):
        acl = self.request.acl.threads.get_role(self.forum)
        actions = []
        try:
            actions.append(('sticky', _('Change to resolved')))
            actions.append(('normal', _('Change to bogus')))
            if acl['can_delete_threads']:
                actions.append(('undelete', _('Restore reports')))
                actions.append(('soft', _('Hide reports')))
            if acl['can_delete_threads'] == 2:
                actions.append(('hard', _('Delete reports')))
        except KeyError:
            pass
        return actions

    def mass_resolve(self, ids):
        reported_posts = []
        reported_threads = []
        for thread in self.threads:
            if thread.pk in ids:
                if thread.original_weight != thread.weight:
                    if thread.weight == 1:
                        thread.set_checkpoint(self.request, 'resolved')
                    if thread.weight == 0:
                        thread.set_checkpoint(self.request, 'bogus')
                if thread.original_weight == 2 and thread.report_for_id:
                    reported_posts.append(thread.report_for.pk)
                    reported_threads.append(thread.report_for.thread_id)
        if reported_threads:
            Thread.objects.filter(id__in=reported_threads).update(replies_reported=F('replies_reported') - 1)
            Post.objects.filter(id__in=reported_posts).update(reported=False, reports=None)
            with UpdatingMonitor() as cm:
                monitor.decrease('reported_posts', len(reported_threads))

    def action_sticky(self, ids):
        if self._action_sticky(ids):
            self.mass_resolve(ids)
            self.request.messages.set_flash(Message(_('Selected reports were set as resolved.')), 'success', 'threads')
        else:
            self.request.messages.set_flash(Message(_('No reports were set as resolved.')), 'info', 'threads')

    def action_normal(self, ids):
        if self._action_normal(ids):
            self.mass_resolve(ids)
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
            self.mass_resolve(ids)
            self.request.messages.set_flash(Message(_('Selected reports have been hidden.')), 'success', 'threads')
        else:
            self.request.messages.set_flash(Message(_('No reports were hidden.')), 'info', 'threads')

    def action_hard(self, ids):
        if self._action_hard(ids):
            self.request.messages.set_flash(Message(_('Selected reports have been deleted.')), 'success', 'threads')
        else:
            self.request.messages.set_flash(Message(_('No reports were deleted.')), 'info', 'threads')
