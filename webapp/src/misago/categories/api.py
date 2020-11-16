from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import CategoryWithPosterSerializer as CategorySerializer
from .utils import get_categories_tree


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request):
        categories_tree = get_categories_tree(request, join_posters=True)
        return Response(CategorySerializer(categories_tree, many=True).data)
