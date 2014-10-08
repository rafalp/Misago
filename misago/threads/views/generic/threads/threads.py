from misago.readtracker import threadstracker

from misago.threads.models import Label


__all__ = ['Threads']


class Threads(object):
    def __init__(self, user):
        self.user = user

    def sort(self, sort_by):
        self.queryset = self.queryset.order_by(sort_by)

    def label_threads(self, threads, labels=None):
        if labels:
            labels_dict = dict([(label.pk, label) for label in labels])
        else:
            labels_dict = Label.objects.get_cached_labels_dict()

        for thread in threads:
            thread.label = labels_dict.get(thread.label_id)

    def make_threads_read_aware(self, threads):
        threadstracker.make_read_aware(self.user, threads)
