from django.utils.translation import ugettext as _

from misago.forums.models import Forum

from misago.threads.permissions import (allow_use_private_threads,
                                        exclude_invisible_private_threads)
from misago.threads.views import generic


class PrivateThreads(generic.Threads):
    def get_queryset(self):
        threads_qs = Forum.objects.private_threads().thread_set
        return exclude_invisible_private_threads(threads_qs, self.user)


class PrivateThreadsFiltering(generic.ThreadsFiltering):
    def get_available_filters(self):
        filters = super(PrivateThreadsFiltering, self).get_available_filters()

        if self.user.acl['can_moderate_private_threads']:
            filters.append({
                'type': 'reported',
                'name': _("With reported posts"),
                'is_label': False,
            })

        return filters


class PrivateThreadsView(generic.ThreadsView):
    link_name = 'misago:private_threads'
    template = 'misago/privatethreads/list.html'
    Threads = PrivateThreads
    Filtering = PrivateThreadsFiltering

    def dispatch(self, request, *args, **kwargs):
        allow_use_private_threads(request.user)

        return super(PrivateThreadsView, self).dispatch(
            request, *args, **kwargs)
