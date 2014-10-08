from misago.core.shortcuts import paginate

from misago.threads.models import ANNOUNCEMENT
from misago.threads.permissions import exclude_invisible_threads
from misago.threads.views.generic.threads import Threads


__all__ = ['ForumThreads']


class ForumThreads(Threads):
    def __init__(self, user, forum):
        self.user = user
        self.forum = forum

        self.filter_by = None
        self.sort_by = ('-weight', '-last_post_on')

    def filter(self, filter_by):
        self.filter_by = filter_by

    def sort(self, sort_by):
        if sort_by[0] == '-':
            weight = '-weight'
        else:
            weight = 'weight'
        self.sort_by = (weight, sort_by)

    def list(self, page=0):
        queryset = self.get_queryset()
        queryset = queryset.order_by(*self.sort_by)

        announcements_qs = queryset.filter(weight=ANNOUNCEMENT)
        threads_qs = queryset.filter(weight__lt=ANNOUNCEMENT)

        self._page = paginate(threads_qs, page, 20, 10)
        self._paginator = self._page.paginator

        threads = []
        for announcement in announcements_qs:
            threads.append(announcement)
        for thread in self._page.object_list:
            threads.append(thread)

        for thread in threads:
            thread.forum = self.forum

        self.label_threads(threads, self.forum.labels)
        self.make_threads_read_aware(threads)

        return threads

    def filter_threads(self, queryset):
        if self.filter_by == 'my-threads':
            return queryset.filter(starter_id=self.user.id)
        else:
            if self.forum.acl['can_see_own_threads']:
                if self.user.is_authenticated():
                    queryset = queryset.filter(starter_id=self.user.id)
                else:
                    queryset = queryset.filter(starter_id=0)
            if self.filter_by == 'reported':
                return queryset.filter(has_reported_posts=True)
            elif self.filter_by == 'moderated-threads':
                return queryset.filter(is_moderated=True)
            elif self.filter_by == 'moderated-posts':
                return queryset.filter(has_moderated_posts=True)
            else:
                for label in self.forum.labels:
                    if label.slug == self.filter_by:
                        return queryset.filter(label_id=label.pk)
                else:
                    return queryset

    def get_queryset(self):
        queryset = exclude_invisible_threads(
            self.user, self.forum, self.forum.thread_set)
        return self.filter_threads(queryset)

    error_message = ("threads list has to be loaded via call to list() before "
                     "pagination data will be available")

    @property
    def paginator(self):
        try:
            return self._paginator
        except AttributeError:
            raise AttributeError(self.error_message)

    @property
    def page(self):
        try:
            return self._page
        except AttributeError:
            raise AttributeError(self.error_message)
