from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render
from django.views.generic import View
from django.utils.translation import ugettext as _, ugettext_lazy

from misago.categories.models import CATEGORIES_TREE_ID, Category
from misago.categories.permissions import (
    allow_see_category, allow_browse_category)
from misago.core.shortcuts import (
    get_object_or_404, paginate, pagination_dict, validate_slug)
from misago.readtracker import threadstracker

from misago.threads.models import Thread
from misago.threads.permissions import exclude_invisible_threads
from misago.threads.utils import add_categories_to_threads


LISTS_NAMES = {
    'my': ugettext_lazy("Your threads"),
    'new': ugettext_lazy("New threads"),
    'unread': ugettext_lazy("Unread threads"),
    'subscribed': ugettext_lazy("subscribed threads"),
}


def get_threads_queryset(user, categories, list_type):
    queryset = Thread.objects.all()
    return exclude_invisible_threads(user, categories, queryset)


class BaseList(View):
    template_name = 'misago/threadslist/threads.html'
    preloaded_data_prefix = ''

    def allow_see_list(self, request, category, list_type):
        if request.user.is_anonymous():
            if list_type == 'my':
                raise PermissionDenied( _("You have to sign in to see list of "
                                          "threads that you have started."))

            if list_type == 'new':
                raise PermissionDenied(_("You have to sign in to see list of "
                                         "threads you haven't read."))

            if list_type == 'unread':
                raise PermissionDenied(_("You have to sign in to see list of "
                                         "threads with new replies."))

            if list_type == 'subscribed':
                raise PermissionDenied(_("You have to sign in to see list of "
                                         "threads you are subscribing."))

    def get_category(self, request, **kwargs):
        return Category.objects.root_category()

    def get_queryset(self, request, categories, list_type):
        return get_threads_queryset(request.user, categories, list_type)

    def get_subcategories(self, request, category):
        if category.is_leaf_node():
            return []

        visible_categories = request.user.acl['visible_categories']
        queryset = category.get_descendants().filter(id__in=visible_categories)
        return list(queryset.order_by('lft'))

    def get_extra_context(self, request, category, subcategories, list_type):
        return {}

    def get(self, request, **kwargs):
        try:
            page = int(request.GET.get('page', 0))
            if page == 1:
                page = None
        except ValueError:
            raise Http404()

        list_type = kwargs['list_type']
        category = self.get_category(request, **kwargs)

        self.allow_see_list(request, category, list_type)

        subcategories = self.get_subcategories(request, category)
        categories = [category] + subcategories

        queryset = self.get_queryset(request, categories, list_type)

        page = paginate(queryset, page, 24, 6)
        paginator = pagination_dict(page)

        threadstracker.make_threads_read_aware(request.user, page.object_list)
        add_categories_to_threads(categories, page.object_list)

        visible_subcategories = []
        for thread in page.object_list:
            if (thread.top_category and
                    thread.top_category not in visible_subcategories):
                visible_subcategories.append(thread.top_category.pk)

        category.subcategories = []
        for subcategory in subcategories:
            if subcategory.pk in visible_subcategories:
                category.subcategories.append(subcategory)

        extra_context = self.get_extra_context(
            request, category, subcategories, list_type)

        show_toolbar = False
        if paginator['count']:
            if category.subcategories:
                show_toolbar = True
            if request.user.is_authenticated():
                show_toolbar = True

        return render(request, self.template_name, dict(
            category=category,
            show_toolbar=show_toolbar,

            list_type=list_type,
            list_name=LISTS_NAMES.get(list_type),

            threads=page.object_list,
            paginator=paginator,
            count=paginator['count'],

            **extra_context
        ))


class ThreadsList(BaseList):
    template_name = 'misago/threadslist/threads.html'

    def get_extra_context(self, request, category, subcategories, list_type):
        return {
            'is_index': not settings.MISAGO_CATEGORIES_ON_INDEX
        }


class CategoryThreadsList(ThreadsList):
    template_name = 'misago/threadslist/category.html'
    preloaded_data_prefix = 'CATEGORY_'

    def get_category(self, request, **kwargs):
        category = get_object_or_404(Category.objects.select_related('parent'),
            tree_id=CATEGORIES_TREE_ID,
            id=kwargs['category_id'],
        )

        allow_see_category(request.user, category)
        allow_browse_category(request.user, category)

        validate_slug(category, kwargs['category_slug'])

        return category

class PrivateThreadsList(ThreadsList):
    template_name = 'misago/threadslist/private_threads.html'
    preloaded_data_prefix = 'PRIVATE_'

    def get_category(self, request, **kwargs):
        return Category.objects.private_threads()

    def get_subcategories(self, request, category):
        return []