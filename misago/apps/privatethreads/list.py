from itertools import chain
from django.http import Http404
from django.utils.translation import ugettext as _
from misago.apps.threadtype.list import ThreadsListBaseView, ThreadsListModeration
from misago.conf import settings
from misago import messages
from misago.models import Forum, Thread, User
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
        if settings.avatars_on_threads_list:
            qs_threads = qs_threads.prefetch_related('start_poster', 'last_poster')

        self.count = qs_threads.count()
        try:
            self.pagination = make_pagination(self.kwargs.get('page', 0), self.count, settings.threads_per_page)
        except Http404:
            return self.threads_list_redirect()

        tracker_forum = ThreadsTracker(self.request, self.forum)
        for thread in qs_threads[self.pagination['start']:self.pagination['stop']]:
            thread.is_read = tracker_forum.is_read(thread)
            self.threads.append(thread)

    def threads_actions(self):
        return (('leave', _("Leave threads")),)

    def action_leave(self, ids):
        left = 0
        for thread in self.threads:
            if thread.pk in ids:
                try:
                    user = thread.participants.get(id=self.request.user.pk)
                    thread.participants.remove(user)
                    thread.threadread_set.filter(id=user.pk).delete()
                    thread.watchedthread_set.filter(id=user.pk).delete()
                    user.sync_pds = True
                    user.save(force_update=True)
                    left +=1
                    # If there are no more participants in thread, remove it
                    if thread.participants.count() == 0:
                        thread.delete()
                    # Nope, see if we removed ourselves
                    else:
                        self.thread.set_checkpoint(self.request, 'left')
                except User.DoesNotExist:
                    pass
        if left:
            messages.success(self.request, _('You have left selected private threads.'), 'threads')
        else:
            messages.info(self.request, _('You have left no private threads.'), 'threads')
