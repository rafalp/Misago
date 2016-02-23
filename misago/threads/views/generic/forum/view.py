from django.shortcuts import redirect

from misago.categories.lists import get_categories_list, get_category_path
from misago.core.shortcuts import validate_slug
from misago.readtracker import categoriestracker

from misago.threads.models import Label
from misago.threads.views.generic.category.actions import ForumActions
from misago.threads.views.generic.category.filtering import ForumFiltering
from misago.threads.views.generic.category.threads import ForumThreads
from misago.threads.views.generic.threads import Sorting, ThreadsView


__all__ = ['ForumView']


class ForumView(ThreadsView):
    """
    Basic view for category threads lists
    """
    template = 'misago/threads/category.html'

    Threads = ForumThreads
    Sorting = Sorting
    Filtering = ForumFiltering
    Actions = ForumActions

    def dispatch(self, request, *args, **kwargs):
        category = self.get_category(request, **kwargs)
        validate_slug(category, kwargs['category_slug'])

        category.labels = Label.objects.get_category_labels(category)

        if category.lft + 1 < category.rght:
            category.subcategories = get_categories_list(request.user, category)
        else:
            category.subcategories = []

        page_number = kwargs.pop('page', None)
        cleaned_kwargs = self.clean_kwargs(request, kwargs)

        link_name = request.resolver_match.view_name

        sorting = self.Sorting(link_name, cleaned_kwargs)
        cleaned_kwargs = sorting.clean_kwargs(cleaned_kwargs)

        filtering = self.Filtering(category, link_name, cleaned_kwargs)
        cleaned_kwargs = filtering.clean_kwargs(cleaned_kwargs)

        if cleaned_kwargs != kwargs:
            return redirect(link_name, **cleaned_kwargs)

        threads = self.Threads(request.user, category)
        sorting.sort(threads)
        filtering.filter(threads)

        actions = self.Actions(user=request.user, category=category)
        if request.method == 'POST':
            response = actions.handle_post(request, threads.get_queryset())
            if response:
                return response

        return self.render(request, {
            'link_name': link_name,
            'links_params': cleaned_kwargs,

            'category': category,
            'path': get_category_path(category),

            'threads': threads.list(page_number),
            'threads_count': threads.count(),
            'page': threads.page,
            'paginator': threads.paginator,

            'threads_actions': actions,
            'selected_threads': actions.get_selected_ids(),

            'sorting': sorting,
            'filtering': filtering,
        })
