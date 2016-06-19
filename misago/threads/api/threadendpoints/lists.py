from django.http import Http404
from rest_framework.response import Response

from misago.acl import add_acl
from misago.categories.models import Category
from misago.categories.permissions import allow_see_category, allow_browse_category
from misago.core.shortcuts import get_int_or_404, paginate, pagination_dict
from misago.readtracker import threadstracker

from misago.threads.mixins.threadslists import ThreadsListMixin
from misago.threads.permissions.privatethreads import allow_use_private_threads
from misago.threads.serializers import ThreadListSerializer
from misago.threads.subscriptions import make_subscription_aware
from misago.threads.utils import add_categories_to_threads


LIST_TYPES = (
    'all',
    'my',
    'new',
    'unread',
    'subscribed',
    'unapproved',
)


class BaseListEndpoint(ThreadsListMixin):
    serialize_subcategories = True

    def __call__(self, request):
        try:
            page_no = int(request.query_params.get('page', 0))
        except (ValueError, TypeError):
            raise Http404()

        list_type = request.query_params.get('list') or 'all'
        if list_type not in LIST_TYPES:
            raise Http404()

        categories = self.get_categories(request)
        category = self.get_category(request, categories)

        self.allow_see_list(request, category, list_type)
        subcategories = self.get_subcategories(category, categories)

        base_queryset = self.get_base_queryset(request, categories, list_type)

        threads_categories = [category] + subcategories
        threads_queryset = self.get_threads_queryset(category, base_queryset, threads_categories)

        page = paginate(threads_queryset, page_no, 24, 6, allow_explicit_first_page=True)
        response_dict = pagination_dict(page, include_page_range=False)

        if page.number > 1:
            threads = list(page.object_list)
        else:
            pinned_threads = self.get_pinned_threads(category, base_queryset, threads_categories)
            threads = list(pinned_threads) + list(page.object_list)

        if list_type in ('new', 'unread'):
            # we already know all threads on list are unread
            threadstracker.make_unread(threads)
        else:
            threadstracker.make_threads_read_aware(request.user, threads)

        add_categories_to_threads(category, categories, threads)

        if self.serialize_subcategories:
            response_dict['subcategories'] = []
            visible_subcategories = self.get_visible_subcategories(threads, threads_categories)
            for subcategory in subcategories:
                if subcategory in visible_subcategories:
                    response_dict['subcategories'].append(subcategory.pk)

        add_acl(request.user, threads)
        make_subscription_aware(request.user, threads)

        response_dict['results'] = ThreadListSerializer(threads, many=True).data
        return Response(response_dict)


class ThreadsListEndpoint(BaseListEndpoint):
    def get_category(self, request, categories):
        if request.query_params.get('category'):
            category_id = get_int_or_404(request.query_params['category'])

            for category in categories:
                if category.pk == category_id:
                    if category.level:
                        allow_see_category(request.user, category)
                        allow_browse_category(request.user, category)

                        return category
                    else:
                        raise Http404() # disallow root category access
            raise Http404()
        return categories[0]

    def get_subcategories(self, category, categories):
        subcategories = []
        for subcategory in categories:
            if category.has_child(subcategory):
                subcategories.append(subcategory)
        return subcategories

    def get_pinned_threads(self, category, queryset, threads_categories):
        if category.level:
            return list(queryset.filter(weight=2)) + list(queryset.filter(
                weight=1,
                category__in=threads_categories
            ))
        else:
            return queryset.filter(weight=2)

    def get_threads_queryset(self, category, queryset, threads_categories):
        if category.level:
            return queryset.filter(
                weight=0,
                category__in=threads_categories,
            )
        else:
            return queryset.filter(
                weight__lt=2,
                category__in=threads_categories,
            )

threads_list_endpoint = ThreadsListEndpoint()


class PrivateThreadsListEndpoint(BaseListEndpoint):
    def get_category(self, request, categories):
        allow_use_private_threads(request.user)
        return Category.objects.private_threads()

    def get_subcategories(self, category, categories):
        return []

    def get_pinned_threads(self, category, queryset, threads_categories):
        return []

    def get_threads_queryset(self, category, queryset, threads_categories):
        return queryset.filter(category__in=threads_categories)

private_threads_list_endpoint = PrivateThreadsListEndpoint()
