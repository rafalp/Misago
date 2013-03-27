from itertools import chain
from django.utils.translation import ugettext as _
from misago.apps.threadtype.list import ThreadsListBaseView, ThreadsListModeration
from misago.models import Forum, Thread
from misago.readstrackers import ThreadsTracker
from misago.utils.pagination import make_pagination
from misago.apps.privatethreads.mixins import TypeMixin

class AllThreadsListView(ThreadsListBaseView, ThreadsListModeration, TypeMixin):
    def fetch_forum(self):
        self.forum = Forum.objects.get(special='private_threads')

    def threads_queryset(self):
        return self.forum.thread_set.filter(participants__id=self.request.user.pk).order_by('-last')

    def fetch_threads(self):
        qs_threads = self.threads_queryset()

        # Add in first and last poster
        if self.request.settings.avatars_on_threads_list:
            qs_threads = qs_threads.prefetch_related('start_poster', 'last_poster')

        self.count = qs_threads.count()
        self.pagination = make_pagination(self.kwargs.get('page', 0), self.count, self.request.settings.threads_per_page)

        tracker_forum = ThreadsTracker(self.request, self.forum)
        for thread in qs_threads[self.pagination['start']:self.pagination['stop']]:
            thread.is_read = tracker_forum.is_read(thread)
            self.threads.append(thread)

    def template_vars(self, context):
        context['tab'] = 'all'
        return context


class MyThreadsListView(AllThreadsListView, ThreadsListModeration, TypeMixin):
    def threads_queryset(self):
        return self.forum.thread_set.filter(start_poster_id=self.request.user.pk).order_by('-last')

    def template_vars(self, context):
        context['tab'] = 'my'
        return context