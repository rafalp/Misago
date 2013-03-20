from django.utils.translation import ugettext as _
from itertools import chain
from misago.apps.forumbase.list import ThreadsListBaseView, ThreadsListModeration
from misago.models import Forum, Thread
from misago.readstrackers import ThreadsTracker
from misago.utils.pagination import make_pagination
from misago.apps.threads.mixins import TypeMixin

class ThreadsListView(ThreadsListBaseView, ThreadsListModeration, TypeMixin):
    def fetch_forum(self):
        self.forum = Forum.objects.get(pk=self.kwargs.get('forum'), type='forum')

    def threads_queryset(self):
        announcements = Forum.objects.special_model('announcements')
        annos_global = announcements.thread_set.filter(deleted=False).filter(moderated=False)
        annos_forum = self.request.acl.threads.filter_threads(self.request, self.forum, self.forum.thread_set).filter(weight=2)
        rest = self.request.acl.threads.filter_threads(self.request, self.forum, self.forum.thread_set).filter(weight__lt=2)

        # Dont display threads by ignored users (unless they are important)
        if self.request.user.is_authenticated():
            ignored_users = self.request.user.ignored_users()
            if ignored_users:
                rest = rest.extra(where=["`threads_thread`.`start_poster_id` IS NULL OR `threads_thread`.`start_poster_id` NOT IN (%s)" % ','.join([str(i) for i in ignored_users])])

        # Add in first and last poster
        if self.request.settings.avatars_on_threads_list:
            annos_global = annos_global.prefetch_related('start_poster', 'last_poster')
            annos_forum = annos_forum.prefetch_related('start_poster', 'last_poster')
            rest = rest.prefetch_related('start_poster', 'last_poster')

        return annos_global, annos_forum, rest

    def fetch_threads(self):
        qs_global, qs_forum, qs_rest = self.threads_queryset()
        self.count = qs_rest.count()
        self.pagination = make_pagination(self.kwargs.get('page', 0), self.count, self.request.settings.threads_per_page)

        tracker_annos = ThreadsTracker(self.request, Forum.objects.special_model('announcements'))
        tracker_forum = ThreadsTracker(self.request, self.forum)

        for thread in list(chain(qs_global, qs_forum, qs_rest[self.pagination['start']:self.pagination['stop']])):
            if thread.forum_id == self.forum.pk:
                thread.is_read = tracker_forum.is_read(thread)
            else:
                thread.weight = 2
                thread.is_read = tracker_annos.is_read(thread)
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
                actions.append(('undelete', _('Undelete threads')))
                actions.append(('soft', _('Soft delete threads')))
            if acl['can_delete_threads'] == 2:
                actions.append(('hard', _('Hard delete threads')))
        except KeyError:
            pass
        return actions