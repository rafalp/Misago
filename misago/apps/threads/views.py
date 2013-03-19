from misago.apps.forumbase.list import ThreadsListBaseView
from misago.models import Forum, Thread
from misago.utils.pagination import make_pagination
from misago.apps.threads.mixins import TypeMixin

class ThreadsListView(ThreadsListBaseView, TypeMixin):
    def fetch_forum(self):
        self.forum = Forum.objects.get(pk=self.kwargs.get('forum'), type='forum')

    def threads_queryset(self):
        announcements = Forum.objects.special_model('announcements')
        annos_global = self.request.acl.threads.filter_threads(self.request, announcements, announcements.thread_set).order_by('-weight')
        annos_forum = self.request.acl.threads.filter_threads(self.request, self.forum, self.forum.thread_set).filter(weight=2)
        rest = self.request.acl.threads.filter_threads(self.request, self.forum, self.forum.thread_set).filter(weight=2)

        # Dont display threads by ignored users (unless they are important)
        if self.request.user.is_authenticated():
            ignored_users = self.request.user.ignored_users()
            if ignored_users:
                rest = rest.extra(where=["`threads_thread`.`start_poster_id` IS NULL OR `threads_thread`.`start_poster_id` NOT IN (%s)" % ','.join([str(i) for i in ignored_users])])

        # Return two 
        if self.request.settings.avatars_on_threads_list:
            return ((annos_global | annos_forum | rest).prefetch_related('start_poster', 'last_poster'),
                    rest.prefetch_related('start_poster', 'last_poster'))
        return (annos_global | annos_forum | rest), rest

    def fetch_threads(self):
        self.threads = []
        ignored_users = []
        queryset, threads = self.threads_queryset()
        for thread in queryset:
            self.threads.append(thread)
        self.count =threads.count()
        self.pagination = make_pagination(self.kwargs.get('page', 0), self.count, self.request.settings.threads_per_page)
        """
        queryset_anno = Thread.objects.filter(Q(forum=Forum.objects.token_to_pk('announcements')) | (Q(forum=self.forum) & Q(weight=2)))
        queryset_threads = self.request.acl.threads.filter_threads(self.request, self.forum, Thread.objects.filter(forum=self.forum).filter(weight__lt=2)).order_by('-weight', '-last')
        if self.request.user.is_authenticated():
            ignored_users = self.request.user.ignored_users()
            if ignored_users:
                queryset_threads = queryset_threads.extra(where=["`threads_thread`.`start_poster_id` IS NULL OR `threads_thread`.`start_poster_id` NOT IN (%s)" % ','.join([str(i) for i in ignored_users])])
        if self.request.settings.avatars_on_threads_list:
            queryset_anno = queryset_anno.prefetch_related('start_poster', 'last_post')
            queryset_threads = queryset_threads.prefetch_related('start_poster', 'last_poster')
        for thread in queryset_anno:
            self.threads.append(thread)
        for thread in queryset_threads:
            self.threads.append(thread)
        if self.request.settings.threads_per_page < self.count:
            self.threads = self.threads[self.pagination['start']:self.pagination['stop']]
        for thread in self.threads:
            if thread.forum_id == self.forum.pk:
                thread.is_read = self.tracker.is_read(thread)
            thread.last_poster_ignored = thread.last_poster_id in ignored_users
        """