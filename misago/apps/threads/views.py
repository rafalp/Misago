from itertools import chain
from misago.apps.forumbase.list import ThreadsListBaseView
from misago.models import Forum, Thread
from misago.readstrackers import ThreadsTracker
from misago.utils.pagination import make_pagination
from misago.apps.threads.mixins import TypeMixin

class ThreadsListView(ThreadsListBaseView, TypeMixin):
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