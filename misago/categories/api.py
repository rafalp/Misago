from django.db import transaction

from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from misago.core.shortcuts import get_int_or_404, get_object_or_404
from misago.readtracker.categoriestracker import read_category
from misago.threads.threadtypes import trees_map

from .models import THREADS_ROOT_NAME, Category
from .permissions import allow_browse_category, allow_see_category
from .serializers import CategorySerializer
from .utils import get_categories_tree


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request):
        categories_tree = get_categories_tree(request.user)
        return Response(CategorySerializer(categories_tree, many=True).data)

    @detail_route(methods=['post'])
    @transaction.atomic
    def read(self, request, pk):
        request.user.lock()

        category_id = get_int_or_404(pk)
        threads_tree_id = trees_map.get_tree_id_for_root(THREADS_ROOT_NAME)

        category = get_object_or_404(Category,
            id=category_id,
            tree_id=threads_tree_id,
        )

        if category.level:
            allow_see_category(request.user, category)
            allow_browse_category(request.user, category)

        read_category(request.user, category)

        return Response({'detail': 'ok'})
