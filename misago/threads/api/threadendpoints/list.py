from django.http import Http404
from rest_framework.response import Response

from misago.acl import add_acl
from misago.categories.models import CATEGORIES_TREE_ID, Category
from misago.categories.permissions import (
    allow_see_category, allow_browse_category)
from misago.categories.serializers import BasicCategorySerializer
from misago.core.shortcuts import (
    get_int_or_404, get_object_or_404, paginate, pagination_dict)
from misago.readtracker import threadstracker

from misago.threads.mixins.threadslists import ThreadsListMixin
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


class BaseListEndpoint(object):
    serialize_subcategories = True

    def get_final_queryset(self, request, categories, threads_categories,
            category, list_type):
        return self.get_queryset(request, categories, list_type).filter(
            category__in=threads_categories
        )

    def __call__(self, request):
        try:
            page = int(request.query_params.get('page', 0))
        except ValueError:
            raise Http404()

        list_type = request.query_params.get('list') or 'all'
        if list_type not in LIST_TYPES:
            raise Http404()

        categories = self.get_categories(request)
        category = self.get_category(request, categories)

        self.allow_see_list(request, category, list_type)
        subcategories = self.get_subcategories(category, categories)

        queryset = self.get_queryset(request, categories, list_type)

        threads_categories = [category] + subcategories
        rest_queryset = self.get_rest_queryset(
            category, queryset, threads_categories)

        page = paginate(rest_queryset, page, 24, 6,
            allow_explicit_first_page=True
        )
        response_dict = pagination_dict(page, include_page_range=False)

        if page.number > 1:
            threads = list(page.object_list)
        else:
            pinned_threads = self.get_pinned_threads(
                category, queryset, threads_categories)
            threads = list(pinned_threads) + list(page.object_list)

        if list_type in ('new', 'unread'):
            """we already know all threads on list are unread"""
            threadstracker.make_unread(threads)
        else:
            threadstracker.make_threads_read_aware(
                request.user, threads)
        add_categories_to_threads(category, categories, threads)

        visible_subcategories = []
        for thread in threads:
            if (thread.top_category and
                    thread.category in threads_categories and
                    thread.top_category not in visible_subcategories):
                visible_subcategories.append(thread.top_category.pk)

        if self.serialize_subcategories:
            response_dict['subcategories'] = []
            for subcategory in subcategories:
                if subcategory.pk in visible_subcategories:
                    response_dict['subcategories'].append(subcategory.pk)

        add_acl(request.user, threads)
        make_subscription_aware(request.user, threads)

        return Response(dict(
            results=ThreadListSerializer(threads, many=True).data,
            **response_dict))


class ThreadsListEndpoint(ThreadsListMixin, BaseListEndpoint):
    def get_category(self, request, categories):
        if request.query_params.get('category'):
            category_id = get_int_or_404(request.query_params['category'])

            for category in categories:
                if category.pk == category_id:
                    if category.level:
                        break;
                    else:
                        raise Http404() # disallow root category access
            else:
                raise Http404()

            allow_see_category(request.user, category)
            allow_browse_category(request.user, category)

            return category
        else:
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


    def get_rest_queryset(self, category, queryset, threads_categories):
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

    def get_final_queryset(self, request, categories, threads_categories,
            category, list_type):
        queryset = self.get_queryset(request, categories, list_type)

        if category.level:
            announcements = queryset.filter(weight=2)
            pinned = queryset.filter(weight=1, category__in=threads_categories)
            other = queryset.filter(weight=1, category__in=threads_categories)

            return announcements | pinned | other
        else:
            announcements = queryset.filter(weight=2)
            other = queryset.filter(
                weight__lt=2,
                category__in=threads_categories,
            )

            return announcements | other


threads_list_endpoint = ThreadsListEndpoint()