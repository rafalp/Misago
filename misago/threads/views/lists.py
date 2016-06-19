from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render
from django.views.generic import View
from django.utils.translation import ugettext_lazy

from misago.acl import add_acl
from misago.categories.models import Category
from misago.categories.permissions import allow_see_category, allow_browse_category
from misago.categories.serializers import IndexCategorySerializer
from misago.core.shortcuts import paginate, pagination_dict, validate_slug
from misago.readtracker import threadstracker

from misago.threads.mixins.threadslist import ThreadsListMixin
from misago.threads.permissions.privatethreads import allow_use_private_threads
from misago.threads.serializers import ThreadListSerializer
from misago.threads.subscriptions import make_subscription_aware
from misago.threads.utils import add_categories_to_threads


LISTS_NAMES = {
    'all': None,
    'my': ugettext_lazy("Your threads"),
    'new': ugettext_lazy("New threads"),
    'unread': ugettext_lazy("Unread threads"),
    'subscribed': ugettext_lazy("Subscribed threads"),
    'unapproved': ugettext_lazy("Unapproved content"),
}


class BaseList(View):
    template_name = 'misago/threadslist/threads.html'
    preloaded_data_prefix = ''

    def get(self, request, list_type=None, **kwargs):
        try:
            page = int(request.GET.get('page', 0))
        except (ValueError, TypeError):
            raise Http404()

        categories = self.get_categories(request)
        category = self.get_category(request, categories, **kwargs)

        self.allow_see_list(request, category, list_type)
        subcategories = self.get_subcategories(category, categories)

        base_queryset = self.get_base_queryset(request, categories, list_type)

        threads_categories = [category] + subcategories
        threads_queryset = self.get_threads_queryset(base_queryset, threads_categories)

        list_page = paginate(threads_queryset, page, 24, 6)
        paginator = pagination_dict(list_page, include_page_range=False)

        if list_page.number > 1:
            threads = list(list_page.object_list)
        else:
            pinned_threads = self.get_pinned_threads(base_queryset, threads_categories)
            threads = list(pinned_threads) + list(list_page.object_list)

        if list_type in ('new', 'unread'):
            # we already know all threads on list are unread
            threadstracker.make_unread(threads)
        else:
            threadstracker.make_threads_read_aware(request.user, threads)

        add_categories_to_threads(category, categories, threads)

        category.subcategories = []
        visible_subcategories = self.get_visible_subcategories(threads, threads_categories)
        for subcategory in subcategories:
            if subcategory in visible_subcategories:
                category.subcategories.append(subcategory)

        add_acl(request.user, threads)
        make_subscription_aware(request.user, threads)

        request.frontend_context.update({
            'THREADS': dict(
                results=ThreadListSerializer(threads, many=True).data,
                subcategories=[c.pk for c in category.subcategories],
                **paginator),
            'CATEGORIES': IndexCategorySerializer(categories, many=True).data,
        })

        if categories[0].special_role:
            request.frontend_context['CATEGORIES'][0]['special_role'] = True

        self.set_frontend_context(request)

        return render(request, self.template_name, dict(
            category=category,

            list_name=LISTS_NAMES[list_type],
            list_type=list_type,

            threads=threads,
            paginator=paginator,
            count=paginator['count'],

            **self.get_extra_context(request)
        ))

    def get_pinned_threads(self, request, queryset):
        return []

    def get_threads_queryset(self, queryset, threads_categories):
        return queryset.filter(category__in=threads_categories)

    def set_extra_frontend_context(self, request):
        pass


class ThreadsList(BaseList, ThreadsListMixin):
    template_name = 'misago/threadslist/threads.html'

    def get_category(self, request, categories, **kwargs):
        return categories[0]

    def get_pinned_threads(self, queryset, threads_categories):
        return queryset.filter(weight=2)

    def get_threads_queryset(self, queryset, threads_categories):
        return queryset.filter(
            weight__lt=2,
            category__in=threads_categories,
        )

    def get_extra_context(self, request):
        return {
            'is_index': not settings.MISAGO_CATEGORIES_ON_INDEX
        }

    def set_frontend_context(self, request):
        request.frontend_context.update({
            'THREADS_API': reverse('misago:api:thread-list'),
            'MERGE_THREADS_API': reverse('misago:api:thread-merge'),
        })


class CategoryThreadsList(ThreadsList, ThreadsListMixin):
    template_name = 'misago/threadslist/category.html'
    preloaded_data_prefix = 'CATEGORY_'

    def get_category(self, request, categories, **kwargs):
        for category in categories:
            # pylint
            if category.pk == int(kwargs['pk']):
                if not category.level:
                    raise Http404()

                allow_see_category(request.user, category)
                allow_browse_category(request.user, category)

                validate_slug(category, kwargs['slug'])
                return category
        raise Http404()

    def get_pinned_threads(self, queryset, threads_categories):
        return list(queryset.filter(weight=2)) + list(queryset.filter(
            weight=1,
            category__in=threads_categories
        ))

    def get_threads_queryset(self, queryset, threads_categories):
        return queryset.filter(
            weight=0,
            category__in=threads_categories,
        )

    def get_extra_context(self, request):
        return {}


class PrivateThreadsList(ThreadsList):
    template_name = 'misago/threadslist/private_threads.html'
    preloaded_data_prefix = 'PRIVATE_'

    def get_categories(self, request):
        return [Category.objects.private_threads()]

    def get_category(self, request, **kwargs):
        allow_use_private_threads(request.user)
        return Category.objects.private_threads()

    def get_subcategories(self, category, categories):
        return []

    def get_base_queryset(self, request, categories, list_type):
        raise NotImplementedError('Private Threads List is not implemented yet!')

    def get_extra_context(self, request):
        return {}
