from itertools import chain
from django.http import Http404
from django.utils.translation import ugettext as _
from misago.apps.threadtype.list import ThreadsListBaseView, ThreadsListModeration
from misago.models import Forum, Thread
from misago.readstrackers import ThreadsTracker
from misago.utils.pagination import make_pagination
from misago.apps.privatethreads.mixins import TypeMixin

class ThreadsListView(ThreadsListBaseView, ThreadsListModeration, TypeMixin):
    def fetch_forum(self):
        self.forum = Forum.objects.get(special='private_threads')

    def threads_queryset(self):
        qs_threads = self.forum.thread_set.filter(participants__id=self.request.user.pk).order_by('-last')
        if self.request.acl.private_threads.is_mod():
            qs_reported = self.forum.thread_set.filter(replies_reported__gt=0)
            qs_threads = qs_threads | qs_reported
            qs_threads = qs_threads.distinct()
        return qs_threads

    def fetch_threads(self):
        qs_threads = self.threads_queryset()

        # Add in first and last poster
        if self.request.settings.avatars_on_threads_list:
            qs_threads = qs_threads.prefetch_related('start_poster', 'last_poster')

        self.count = qs_threads.count()
        try:
            self.pagination = make_pagination(self.kwargs.get('page', 0), self.count, self.request.settings.threads_per_page)
        except Http404:
            return self.threads_list_redirect()

        tracker_forum = ThreadsTracker(self.request, self.forum)
        for thread in qs_threads[self.pagination['start']:self.pagination['stop']]:
            thread.is_read = tracker_forum.is_read(thread)
            self.threads.append(thread)
