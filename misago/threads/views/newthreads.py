from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.transaction import atomic
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from misago.core.decorators import require_POST
from misago.core.uiviews import uiview
from misago.users.decorators import deny_guests

from misago.threads.models import Thread
from misago.threads.permissions import exclude_invisible_threads
from misago.threads.views.generic.threads import Threads, ThreadsView


class NewThreads(Threads):
    def get_queryset(self):
        cutoff_days = settings.MISAGO_FRESH_CONTENT_PERIOD
        cutoff_date = timezone.now() - timedelta(days=cutoff_days)
        if cutoff_date < self.user.reads_cutoff:
            cutoff_date = self.user.reads_cutoff
        if cutoff_date < self.user.new_threads_cutoff:
            cutoff_date = self.user.new_threads_cutoff

        queryset = Thread.objects.filter(started_on__gte=cutoff_date)
        queryset = queryset.select_related('forum')

        tracked_threads = self.user.threadread_set.all()
        queryset = queryset.exclude(id__in=tracked_threads.values('thread_id'))
        queryset = exclude_invisible_threads(queryset, self.user)
        return queryset


class NewThreadsView(ThreadsView):
    link_name = 'misago:new_threads'
    template = 'misago/threads/new.html'

    Threads = NewThreads

    def process_context(self, request, context):
        context['show_threads_locations'] = True
        context['fresh_period'] = settings.MISAGO_FRESH_CONTENT_PERIOD

        if request.user.new_threads != context['threads_count']:
            request.user.new_threads.set(context['threads_count'])
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            message = _("You have to sign in to see your list of new threads.")
            raise PermissionDenied(message)

        return super(NewThreadsView, self).dispatch(
            request, *args, **kwargs)


@deny_guests
@require_POST
@csrf_protect
@never_cache
@atomic
def clear_new_threads(request):
    request.user.new_threads_cutoff = timezone.now()
    request.user.save(update_fields=['new_threads_cutoff'])

    request.user.new_threads.set(0)

    messages.success(request, _("New threads list has been cleared."))
    return redirect('misago:new_threads')


@uiview("new_threads")
@deny_guests
def event_sender(request, resolver_match):
    return int(request.user.new_threads)
