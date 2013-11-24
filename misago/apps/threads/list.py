from itertools import chain
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from misago import messages
from misago.acl.exceptions import ACLError403, ACLError404
from misago.apps.errors import error403, error404
from misago.apps.threadtype.list import ThreadsListBaseView, ThreadsListModeration
from misago.conf import settings
from misago.decorators import check_csrf
from misago.models import Forum, Thread, ThreadPrefix
from misago.readstrackers import ThreadsTracker
from misago.utils.pagination import make_pagination
from misago.apps.threads.mixins import TypeMixin

class ThreadsListView(ThreadsListBaseView, ThreadsListModeration, TypeMixin):
    def fetch_forum(self):
        self.forum = Forum.objects.get(pk=self.kwargs.get('forum'), type='forum')

        self.prefixes = ThreadPrefix.objects.forum_prefixes(self.forum)
        self.active_prefix = self.kwargs.get('prefix', None)
        if self.active_prefix:
            for prefix in self.prefixes.values():
                if self.active_prefix == prefix.slug:
                    self.active_prefix = prefix
                    break
            else:
                raise ACLError404()

    def template_vars(self, context):
        context['prefixes'] = self.prefixes
        context['active_prefix'] = self.active_prefix
        return context

    def threads_queryset(self):
        announcements = self.request.acl.threads.filter_threads(self.request, self.forum, self.forum.thread_set).filter(weight=2).order_by('-pk')
        threads = self.request.acl.threads.filter_threads(self.request, self.forum, self.forum.thread_set).filter(weight__lt=2).order_by('-weight', '-last')

        if self.active_prefix:
            threads = threads.filter(prefix=self.active_prefix)

        # Dont display threads by ignored users (unless they are important)
        if self.request.user.is_authenticated():
            ignored_users = self.request.user.ignored_users()
            if ignored_users:
                threads = threads.exclude(start_poster_id__in=ignored_users)

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
            if acl['can_change_prefixes']:
                actions.append(('prefix:0', _('Remove prefix')))
                for prefix in self.prefixes.values():
                    actions.append(('prefix:%s' % prefix.pk, _('Change prefix to: %(prefix)s') % {'prefix': _(prefix.name)}))
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

    def action_prefix(self, ids, prefix):
        prefixes = self.prefixes
        try:
            prefix = int(prefix)
        except TypeError:
            prefix = 0
        prefix = prefix or None

        if prefix:
            if self._action_set_prefix(ids, prefixes[prefix]):
                messages.success(self.request, _('Selected threads prefix has been changed to "%(name)s".') % {'name': _(prefixes[prefix].name)}, 'threads')
            else:
                messages.info(self.request, _('No threads prefix was changed.'), 'threads')
        else:
            if self._action_remove_prefix(ids):
                messages.success(self.request, _('Selected threads prefix has been removed.'), 'threads')
            else:
                messages.info(self.request, _('No threads prefixes were removed.'), 'threads')

    def _action_set_prefix(self, ids, prefix):
        changed = []
        for thread in self.threads:
            if thread.pk in ids and prefix.pk != thread.prefix_id:
                changed.append(thread.pk)
                thread.prefix = prefix
                thread.set_checkpoint(self.request, 'changed_prefix', self.request.user, self.forum, extra=prefix.name)
                thread.save(force_update=True)
        return changed

    def _action_remove_prefix(self, ids):
        changed = []
        for thread in self.threads:
            if thread.pk in ids and not thread.prefix_id:
                changed.append(thread.pk)
                thread.prefix_id = None
                thread.set_checkpoint(self.request, 'removed_prefix', self.request.user, self.forum)
                thread.save(force_update=True)
        return changed