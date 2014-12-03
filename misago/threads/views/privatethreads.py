from django.utils.translation import ugettext as _

from misago.acl import add_acl
from misago.forums.models import Forum

from misago.threads.permissions import (allow_use_private_threads,
                                        exclude_invisible_private_threads)
from misago.threads.views import generic
from misago.threads.views.posting import PostingView as BasePostingView


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


def private_threads_view(klass):
    def get_forum(self, request, lock=False, **kwargs):
        forum = Forum.objects.private_threads()
        add_acl(request.user, forum)
        return forum

    def dispatch(self, request, *args, **kwargs):
        allow_use_private_threads(request.user)

        return super(self.__class__, self).dispatch(
            request, *args, **kwargs)

    klass.get_forum = get_forum
    klass.dispatch = dispatch

    return klass


@private_threads_view
class ThreadsView(generic.ThreadsView):
    link_name = 'misago:private_threads'
    template = 'misago/privatethreads/list.html'

    Threads = PrivateThreads
    Filtering = PrivateThreadsFiltering


@private_threads_view
class ThreadView(generic.ThreadView):
    pass


@private_threads_view
class GotoLastView(generic.GotoLastView):
    pass


@private_threads_view
class GotoNewView(generic.GotoNewView):
    pass


@private_threads_view
class GotoPostView(generic.GotoPostView):
    pass


@private_threads_view
class PostingView(BasePostingView):
    pass
