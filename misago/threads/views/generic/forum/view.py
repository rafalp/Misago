from django.shortcuts import redirect

from misago.core.shortcuts import validate_slug
from misago.forums.lists import get_forums_list, get_forum_path
from misago.readtracker import forumstracker

from misago.threads.models import Label
from misago.threads.views.generic.forum.actions import ForumActions
from misago.threads.views.generic.forum.filtering import ForumFiltering
from misago.threads.views.generic.forum.threads import ForumThreads
from misago.threads.views.generic.threads import Sorting, ThreadsView


__all__ = ['ForumView']


class ForumView(ThreadsView):
    """
    Basic view for forum threads lists
    """
    template = 'misago/threads/forum.html'

    Threads = ForumThreads
    Sorting = Sorting
    Filtering = ForumFiltering
    Actions = ForumActions

    def dispatch(self, request, *args, **kwargs):
        forum = self.get_forum(request, **kwargs)
        validate_slug(forum, kwargs['forum_slug'])

        forum.labels = Label.objects.get_forum_labels(forum)

        if forum.lft + 1 < forum.rght:
            forum.subforums = get_forums_list(request.user, forum)
        else:
            forum.subforums = []

        page_number = kwargs.pop('page', None)
        cleaned_kwargs = self.clean_kwargs(request, kwargs)

        link_name = request.resolver_match.view_name

        sorting = self.Sorting(link_name, cleaned_kwargs)
        cleaned_kwargs = sorting.clean_kwargs(cleaned_kwargs)

        filtering = self.Filtering(forum, link_name, cleaned_kwargs)
        cleaned_kwargs = filtering.clean_kwargs(cleaned_kwargs)

        if cleaned_kwargs != kwargs:
            return redirect(link_name, **cleaned_kwargs)

        threads = self.Threads(request.user, forum)
        sorting.sort(threads)
        filtering.filter(threads)

        actions = self.Actions(user=request.user, forum=forum)
        if request.method == 'POST':
            response = actions.handle_post(request, threads.get_queryset())
            if response:
                return response

        return self.render(request, {
            'link_name': link_name,
            'links_params': cleaned_kwargs,

            'forum': forum,
            'path': get_forum_path(forum),

            'threads': threads.list(page_number),
            'threads_count': threads.count(),
            'page': threads.page,
            'paginator': threads.paginator,

            'threads_actions': actions,
            'selected_threads': actions.get_selected_ids(),

            'sorting': sorting,
            'filtering': filtering,
        })
