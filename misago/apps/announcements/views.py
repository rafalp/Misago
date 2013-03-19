from misago.apps.forumbase.list import ThreadsListBaseView
from misago.models import Forum, Thread
from misago.readstrackers import ThreadsTracker
from misago.utils.pagination import make_pagination
from misago.apps.announcements.mixins import TypeMixin

class ThreadsListView(ThreadsListBaseView, TypeMixin):
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