from misago.acl import add_acl
from misago.core.shortcuts import paginate
from misago.readtracker import threadstracker

from misago.threads.models import Label


__all__ = ['Threads']


class Threads(object):
    def __init__(self, user):
        self.pinned_count = 0

        self.user = user

        self.filter_by = None
        self.sort_by = '-last_post_on'

    def filter(self, filter_by):
        self.filter_by = filter_by

    def sort(self, sort_by):
        self.sort_by = sort_by

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

        self.label_threads(threads, Label.objects.get_cached_labels())
        self.make_threads_read_aware(threads)

        return threads

    def get_queryset(self):
        queryset = exclude_invisible_threads(self.forum.thread_set, self.user)
        return self.filter_threads(queryset)

    def filter_threads(self, queryset):
        return queryset

    def label_threads(self, threads, labels=None):
        if labels:
            labels_dict = dict([(label.pk, label) for label in labels])
        else:
            labels_dict = Label.objects.get_cached_labels_dict()

        for thread in threads:
            thread.label = labels_dict.get(thread.label_id)

    def make_threads_read_aware(self, threads):
        threadstracker.make_read_aware(self.user, threads)

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

    def count(self):
        return self.pinned_count + self.paginator.count
