from misago.core.shortcuts import paginate

from misago.threads.views.generic.base import ViewBase
from misago.threads.views.generic.threads.sorting import Sorting


__all__ = ['ThreadsView']


class ThreadsView(ViewBase):
    """
    Basic view for generic threads lists
    """

    Threads = None
    Sorting = Sorting
    Filtering = None
    Actions = None

    def clean_kwargs(self, request, kwargs):
        cleaned_kwargs = kwargs.copy()
        if request.user.is_anonymous():
            """we don't allow sort/filter for guests"""
            cleaned_kwargs.pop('sort', None)
            cleaned_kwargs.pop('show', None)
        return cleaned_kwargs

    def dispatch(self, request, *args, **kwargs):
        link_name = request.resolver_match.view_name
        page_number = kwargs.pop('page', None)
        cleaned_kwargs = self.clean_kwargs(request, kwargs)

        if self.Sorting:
            sorting = self.Sorting(link_name, cleaned_kwargs)
            cleaned_kwargs = sorting.clean_kwargs(cleaned_kwargs)

        if self.Filtering:
            filtering = self.Filtering(
                request.user, link_name, cleaned_kwargs)
            cleaned_kwargs = filtering.clean_kwargs(cleaned_kwargs)

        if cleaned_kwargs != kwargs:
            return redirect(link_name, **cleaned_kwargs)

        threads = self.Threads(request.user)

        if self.Sorting:
            sorting.sort(threads)
        if self.Filtering:
            filtering.filter(threads)

        actions = None
        if self.Actions:
            actions = self.Actions(user=request.user)
            if request.method == 'POST':
                # see if we can delegate anything to actions manager
                response = actions.handle_post(request, threads.get_queryset())
                if response:
                    return response

        # build template context
        context = {
            'link_name': link_name,
            'links_params': cleaned_kwargs,

            'threads': threads.list(page_number),
            'threads_count': threads.count(),
            'page': threads.page,
            'paginator': threads.paginator,
        }

        if self.Sorting:
            context.update({'sorting': sorting})

        if self.Filtering:
            context.update({'filtering': filtering})

        if self.Actions:
            context.update({
                'threads_actions': actions,
                'selected_threads': actions.get_selected_ids(),
            })

        return self.render(request, context)
