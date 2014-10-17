from misago.core.shortcuts import paginate
from misago.readtracker import threadstracker

from misago.threads.permissions import exclude_invisible_threads
from misago.threads.views.generic.threads import Threads


__all__ = ['ForumThreads']


class ForumThreads(Threads):
    def __init__(self, user, forum):
        self.pinned_count = 0

        self.user = user
        self.forum = forum

        self.filter_by = None
        self.sort_by = '-last_post_on'

    def list(self, page=0):
        queryset = self.get_queryset()
        queryset = queryset.order_by(self.sort_by)

        pinned_qs = queryset.filter(is_pinned=True)
        threads_qs = queryset.filter(is_pinned=False)

        self._page = paginate(threads_qs, page, 20, 10)
        self._paginator = self._page.paginator

        threads = []
        for thread in pinned_qs:
            threads.append(thread)
            self.pinned_count += 1
        for thread in self._page.object_list:
            threads.append(thread)

        for thread in threads:
            thread.forum = self.forum

        self.label_threads(threads, self.forum.labels)
        self.make_threads_read_aware(threads)

        return threads

    def get_queryset(self):
        queryset = exclude_invisible_threads(
            self.forum.thread_set, self.user, self.forum)
        return self.filter_threads(queryset)

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

    def make_threads_read_aware(self, threads):
        threadstracker.make_threads_read_aware(self.user, threads, self.forum)
