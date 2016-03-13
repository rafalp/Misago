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
from misago.threads.utils import add_categories_to_threads


LIST_TYPES = (
    'all',
    'my',
    'new',
    'unread',
    'subscribed',
)


class BaseListEndpoint(object):
    serialize_subcategories = True

    def __call__(self, request):
        try:
            page = int(request.query_params.get('page', 0))
        except ValueError:
            raise Http404()

        list_type = request.query_params.get('list') or 'all'
        if list_type not in LIST_TYPES:
            raise Http404()

        category = self.get_category(request)

        self.allow_see_list(request, category, list_type)

        subcategories = self.get_subcategories(request, category)
        categories = [category] + subcategories

        queryset = self.get_queryset(
            request, categories, list_type).order_by('-last_post_on')

        page = paginate(queryset, page, 24, 6, allow_explicit_first_page=True)
        response_dict = pagination_dict(page, include_page_range=False)

        if list_type in ('new', 'unread'):
            """we already know all threads on list are unread"""
            threadstracker.make_unread(page.object_list)
        else:
            threadstracker.make_threads_read_aware(
                request.user, page.object_list)
        add_categories_to_threads(categories, page.object_list)

        visible_subcategories = []
        for thread in page.object_list:
            if (thread.top_category and
                    thread.top_category not in visible_subcategories):
                visible_subcategories.append(thread.top_category.pk)

        if self.serialize_subcategories:
            response_dict['subcategories'] = []
            for subcategory in subcategories:
                if subcategory.pk in visible_subcategories:
                    response_dict['subcategories'].append(subcategory.pk)

        add_acl(request.user, page.object_list)

        return Response(dict(
            results=ThreadListSerializer(page.object_list, many=True).data,
            **response_dict))


class ThreadsListEndpoint(ThreadsListMixin, BaseListEndpoint):
    def get_category(self, request):
        if request.query_params.get('category'):
            category_id = get_int_or_404(request.query_params['category'])
            category = get_object_or_404(
                Category.objects.select_related('parent'),
                tree_id=CATEGORIES_TREE_ID,
                id=category_id,
            )

            allow_see_category(request.user, category)
            allow_browse_category(request.user, category)

            return category
        else:
            return Category.objects.root_category()


threads_list_endpoint = ThreadsListEndpoint()