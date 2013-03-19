from django.utils.translation import ugettext as _
from misago.apps.forumbase.list import ThreadsListBaseView, ThreadsListModeration
from misago.models import Forum, Thread
from misago.readstrackers import ThreadsTracker
from misago.utils.pagination import make_pagination
from misago.apps.announcements.mixins import TypeMixin

class ThreadsListView(ThreadsListBaseView, ThreadsListModeration, TypeMixin):
    def fetch_forum(self):
        self.forum = Forum.objects.get(special='announcements')

    def fetch_threads(self):
        queryset = self.request.acl.threads.filter_threads(self.request, self.forum, Thread.objects.filter(forum=self.forum))
        self.count = queryset.count()
        self.pagination = make_pagination(self.kwargs.get('page', 0), self.count, self.request.settings.threads_per_page)
        
        if self.request.settings.avatars_on_threads_list:
            queryset = queryset.prefetch_related('start_poster', 'last_poster')

        tracker = ThreadsTracker(self.request, self.forum)
        for thread in queryset[self.pagination['start']:self.pagination['stop']]:
            thread.is_read = tracker.is_read(thread)
            self.threads.append(thread)

    def threads_actions(self):
        acl = self.request.acl.threads.get_role(self.forum)
        actions = []
        try:
            if acl['can_approve']:
                actions.append(('accept', _('Accept threads')))
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